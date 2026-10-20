from flask import Flask, request, jsonify
from PIL import Image
import base64
import io
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration

# Flask app
app = Flask(__name__)

# Load model (first time download ~13GB, then cached)
MODEL_NAME = "llava-hf/llava-1.5-7b"
print("🔄 Loading model, please wait...")
processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = LlavaForConditionalGeneration.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    low_cpu_mem_usage=True,
    device_map="auto"
)
print("✅ Model loaded successfully!")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        image_b64 = data.get("image")
        question = data.get("question", "Describe the image.")

        if not image_b64:
            return jsonify({"error": "Image not provided"}), 400

        # Decode base64 image
        image = Image.open(io.BytesIO(base64.b64decode(image_b64))).convert("RGB")

        # Prepare inputs
        inputs = processor(images=image, text=question, return_tensors="pt").to(model.device)

        # Generate answer
        output = model.generate(**inputs, max_new_tokens=200)
        answer = processor.decode(output[0], skip_special_tokens=True)

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
