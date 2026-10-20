


import moderngl
import numpy as np
from pyrr import Matrix44, Vector3, Quaternion
import glfw
import math
import random
import time
from collections import deque
import noise
import numpy as np
from noise import snoise3  # Perlin noise
from scipy.spatial.transform import Rotation

class Neuron:
    def __init__(self, position, layer):
        self.position = position
        self.base_position = position
        self.layer = layer
        self.radius = 0.015  # Very small fixed size
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        self.pulse_speed = random.uniform(0.8, 1.2)
        self.activity = 0.0
        self.energy_level = 0.0
        self.connections = []
        self.glow_size = 1.0
        self.target_glow_size = 1.0
        self.halo_intensity = 0.0
        
        # Consistent blue color scheme with slight variations
        self.base_hue = 0.6  # Blue hue (0.6 is blue in HSV)
        hue_variation = random.uniform(-0.02, 0.02)  # Very slight hue variation
        self.color = self.hsv_to_rgb(self.base_hue + hue_variation, 0.9, 0.9)
        self.target_color = self.color
        self.current_color = self.color
        
        self.energy_history = deque(maxlen=10)
        self.spark_timer = random.uniform(0, 5)
        self.spark_intensity = 0.0
        self.oscillation_factor = random.uniform(0.9, 1.1)
        self.connection_strengths = {}
        
        # For organic movement
        self.noise_offset = Vector3([
            random.uniform(0, 100), 
            random.uniform(0, 100), 
            random.uniform(0, 100)
        ])
        self.velocity = Vector3([0, 0, 0], dtype='f4')
        self.target_offset = Vector3([
            random.uniform(-0.1, 0.1),
            random.uniform(-0.1, 0.1),
            random.uniform(-0.1, 0.1)
        ])
        
    def hsv_to_rgb(self, h, s, v):
        h_i = int(h * 6)
        f = h * 6 - h_i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        
        if h_i == 0: return (v, t, p)
        elif h_i == 1: return (q, v, p)
        elif h_i == 2: return (p, v, t)
        elif h_i == 3: return (p, q, v)
        elif h_i == 4: return (t, p, v)
        else: return (v, p, q)
        
    def update(self, time, brain_activity):
        # Organic movement with noise
        n = 0.3
        self.velocity.x = noise.snoise3(
            self.noise_offset.x + time * 0.1,
            self.noise_offset.y,
            self.noise_offset.z,
            octaves=2, persistence=0.5
        ) * 0.003 * brain_activity
        
        self.velocity.y = noise.snoise3(
            self.noise_offset.x,
            self.noise_offset.y + time * 0.1,
            self.noise_offset.z,
            octaves=2, persistence=0.5
        ) * 0.003 * brain_activity
        
        self.velocity.z = noise.snoise3(
            self.noise_offset.x,
            self.noise_offset.y,
            self.noise_offset.z + time * 0.1,
            octaves=2, persistence=0.5
        ) * 0.003 * brain_activity
        
        # Move toward target offset
        offset_diff = self.target_offset - (self.position - self.base_position)
        self.velocity += offset_diff * 0.001
        
        self.position += self.velocity
        self.velocity *= 0.92  # Damping
        
        # Occasionally change target offset
        if random.random() < 0.01:
            self.target_offset = Vector3([
                random.uniform(-0.15, 0.15),
                random.uniform(-0.15, 0.15),
                random.uniform(-0.15, 0.15)
            ])
        
        # Record energy history for afterglow effect
        self.energy_history.append(self.energy_level)
        
        # Subtle pulsing animation
        self.pulse_phase += 0.02 * self.pulse_speed * self.oscillation_factor
        pulse_factor = 0.9 + 0.1 * math.sin(self.pulse_phase)  # Very subtle pulse
        
        # Activity-based effects
        energy_input = self.activity * 0.2  # Reduced energy absorption
        self.energy_level = min(1.0, self.energy_level + energy_input)
        self.energy_level *= 0.92  # Energy decay
        
        # Fixed radius with very subtle pulse
        self.current_radius = self.radius * pulse_factor
        
        # Activity decay
        self.activity *= 0.85
        
        # Glow animation - subtle variations
        if random.random() < 0.05:
            self.target_glow_size = random.uniform(0.9, 1.2)
        self.glow_size += (self.target_glow_size - self.glow_size) * 0.05
        
        # Halo effect when receiving energy
        self.halo_intensity = max(self.halo_intensity - 0.04, 0)
        
        # Spark effect
        self.spark_timer -= 0.016
        if self.spark_timer <= 0:
            self.spark_timer = random.uniform(2.0, 5.0)
            self.spark_intensity = random.uniform(0.2, 0.8)
        self.spark_intensity *= 0.9
        
        # Maintain consistent blue color with slight energy variations
        if self.energy_level > 0.1:
            energy_hue_shift = 0.02 * math.sin(time * 0.5) * self.energy_level
            saturation_boost = min(1.0, 0.9 + self.energy_level * 0.2)
            value_boost = min(1.0, 0.9 + self.energy_level * 0.2)
            self.target_color = self.hsv_to_rgb(
                self.base_hue + energy_hue_shift, 
                saturation_boost, 
                value_boost
            )
        else:
            self.target_color = self.color
            
        # Smooth color transition
        color_diff = (
            self.target_color[0] - self.current_color[0],
            self.target_color[1] - self.current_color[1],
            self.target_color[2] - self.current_color[2]
        )
        
        self.current_color = (
            self.current_color[0] + color_diff[0] * 0.1,
            self.current_color[1] + color_diff[1] * 0.1,
            self.current_color[2] + color_diff[2] * 0.1
        )

class EnergyPulse:
    def __init__(self, start_neuron, end_neuron, speed, brain_activity):
        self.start_pos = start_neuron.position
        self.end_pos = end_neuron.position
        self.start_neuron = start_neuron
        self.end_neuron = end_neuron
        self.progress = 0.0
        self.speed = speed * (0.8 + brain_activity * 0.3)  # Reduced speed multiplier
        self.size = 0.02  # Smaller pulse size
        
        # Consistent blue color
        self.base_color = (0.2, 0.5, 1.0, 1.0)
        self.color = list(self.base_color)
        self.alive = True
        self.energy = 1.0
        self.trail_positions = deque(maxlen=10)  # Shorter trail
        self.trail_sizes = deque(maxlen=10)
        self.trail_colors = deque(maxlen=10)
        self.time_offset = random.uniform(0, 100)
        self.spark_positions = []
        self.path_offset = Vector3([
            random.uniform(-0.03, 0.03),
            random.uniform(-0.03, 0.03),
            random.uniform(-0.03, 0.03)
        ])
        
        # Initial trail
        self.trail_positions.append(self.start_pos)
        self.trail_sizes.append(self.size * 0.7)
        self.trail_colors.append(self.color)
    
    def update(self):
        self.progress += self.speed
        self.energy *= 0.95
        
        # Current position with subtle path variation
        t = self.progress
        path_t = t + 0.1 * math.sin(t * math.pi * 4 + self.time_offset)
        current_pos = self.start_pos + (self.end_pos - self.start_pos) * path_t
        
        # Add subtle offset to path
        path_offset = self.path_offset * math.sin(t * math.pi) * 0.3
        current_pos += path_offset
        
        # Add to trail
        self.trail_positions.append(current_pos)
        self.trail_sizes.append(self.size * self.energy)
        self.trail_colors.append(self.color)
        
        # Update sparks
        for spark in self.spark_positions[:]:
            spark['position'] += spark['velocity']
            spark['life'] -= 0.02
            spark['velocity'] *= 0.94
            if spark['life'] <= 0:
                self.spark_positions.remove(spark)
        
        # Add new sparks occasionally
        if random.random() < 0.2 * self.energy:
            velocity = Vector3([
                random.uniform(-0.01, 0.01),
                random.uniform(-0.01, 0.01),
                random.uniform(-0.01, 0.01)
            ])
            # Make sparks move along the path
            velocity += (self.end_pos - self.start_pos).normalized * random.uniform(0.003, 0.01)
            
            self.spark_positions.append({
                'position': current_pos,
                'velocity': velocity,
                'size': random.uniform(0.008, 0.02) * self.energy,
                'life': random.uniform(0.4, 1.2),
                'color': self.base_color
            })
        
        if self.progress >= 1.0:
            self.alive = False
            # Transfer energy to end neuron
            connection_strength = self.start_neuron.connection_strengths.get(id(self.end_neuron), 1.0)
            energy_transfer = min(1.0, 0.5 * connection_strength)
            self.end_neuron.activity = min(1.0, self.end_neuron.activity + energy_transfer)
            self.end_neuron.halo_intensity = 1.0 * connection_strength
            
            # Strengthen the connection
            current_strength = self.start_neuron.connection_strengths.get(id(self.end_neuron), 1.0)
            self.start_neuron.connection_strengths[id(self.end_neuron)] = min(1.5, current_strength + 0.03)
            
            # Weaken other connections slightly
            for neuron_id in self.start_neuron.connection_strengths:
                if neuron_id != id(self.end_neuron):
                    self.start_neuron.connection_strengths[neuron_id] = max(0.5, 
                        self.start_neuron.connection_strengths[neuron_id] - 0.005)
    
    def get_current_position(self):
        """Returns the current position of the pulse along its path"""
        t = self.progress + 0.1 * math.sin(self.progress * math.pi * 4 + self.time_offset)
        current_pos = self.start_pos + (self.end_pos - self.start_pos) * t
        current_pos += self.path_offset * math.sin(self.progress * math.pi) * 0.3
        return current_pos

class Spark:
    def __init__(self, position, color=None, size=None):
        self.position = position
        self.velocity = Vector3([
            random.uniform(-0.02, 0.02),
            random.uniform(-0.02, 0.02),
            random.uniform(-0.02, 0.02)
        ])
        self.size = size if size else random.uniform(0.008, 0.02)  # Smaller sparks
        self.life = random.uniform(0.5, 1.5)
        
        if color:
            self.color = color
        else:
            # Blue color with slight variation
            hue = 0.6 + random.uniform(-0.05, 0.05)
            saturation = 0.8 + random.uniform(-0.1, 0.1)
            value = 0.9 + random.uniform(-0.1, 0.1)
            self.color = self.hsv_to_rgba(hue, saturation, value)
        
        self.rotation = Quaternion.from_eulers((
            random.uniform(0, math.pi * 2),
            random.uniform(0, math.pi * 2),
            random.uniform(0, math.pi * 2)
        ))
        self.angular_velocity = Vector3([
            random.uniform(-0.1, 0.1),
            random.uniform(-0.1, 0.1),
            random.uniform(-0.1, 0.1)
        ])
    
    def hsv_to_rgba(self, h, s, v):
        rgb = self.hsv_to_rgb(h, s, v)
        return (rgb[0], rgb[1], rgb[2], 1.0)
        
    def hsv_to_rgb(self, h, s, v):
        h_i = int(h * 6)
        f = h * 6 - h_i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        
        if h_i == 0: return (v, t, p)
        elif h_i == 1: return (q, v, p)
        elif h_i == 2: return (p, v, t)
        elif h_i == 3: return (p, q, v)
        elif h_i == 4: return (t, p, v)
        else: return (v, p, q)
    
    def update(self):
        self.position += self.velocity
        self.velocity *= 0.95
        self.life -= 0.02
        self.size *= 0.96
        
        # Update rotation
        rot = Quaternion.from_eulers(self.angular_velocity)
        self.rotation = rot * self.rotation

class AIVisualizer:
    def __init__(self):
        # Initialize GLFW
        if not glfw.init():
            raise Exception("GLFW initialization failed")
        
        # Configure window
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.SAMPLES, 8)  # 8x MSAA
        
        self.window = glfw.create_window(1600, 900, "Advanced Neural Network Visualization", None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window creation failed")
        
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  # Enable vsync
        
        # Create ModernGL context
        self.ctx = moderngl.create_context()
        
        # Enable features
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.BLEND | moderngl.PROGRAM_POINT_SIZE)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE
        self.ctx.blend_equation = moderngl.FUNC_ADD
        
        # Initialize components
        self.neurons = []
        self.connections = []
        self.pulses = []
        self.sparks = []
        self.brain_activity_level = 0.5
        self.energy_flow_direction = 1
        self.brain_layers = []
        
        # Initialize star positions
        self.star_positions = []
        self.init_stars(800)  # More stars for better background
        
        # Camera parameters
        self.camera_pos = Vector3([0, 0, 4], dtype='f4')
        self.camera_target = Vector3([0, 0, 0], dtype='f4')
        self.camera_up = Vector3([0, 1, 0], dtype='f4')
        self.camera_rotation = Quaternion()
        self.camera_distance = 4.0
        self.camera_angle_x = 0.0
        self.camera_angle_y = 0.0
        
        # Animation parameters
        self.time = 0.0
        self.last_time = time.time()
        self.global_glow_factor = 1.0
        self.global_pulse_factor = 0.0
        self.brain_outer_glow = 0.0
        
        # Initialize the brain structure with more neurons
        
        
        # Load shaders
        self.load_shaders()
        self.init_brain()
        
        # Create vertex buffers
        self.create_buffers()
        
        # Setup input handling
        self.setup_input()

    def init_stars(self, count):
        for _ in range(count):
            # Create stars in a spherical distribution
            theta = random.uniform(0, math.pi * 2)
            phi = math.acos(random.uniform(-1, 1))
            r = random.uniform(8, 20)  # Larger sphere for stars
            
            x = r * math.sin(phi) * math.cos(theta)
            y = r * math.sin(phi) * math.sin(theta)
            z = r * math.cos(phi)
            
            size = random.uniform(0.003, 0.015)  # Smaller stars
            brightness = random.uniform(0.2, 0.8)  # More subtle brightness
            
            self.star_positions.append((x, y, z, size, brightness))
    
    def setup_input(self):
        glfw.set_key_callback(self.window, self.on_key)
        glfw.set_mouse_button_callback(self.window, self.on_mouse_button)
        glfw.set_cursor_pos_callback(self.window, self.on_mouse_move)
        glfw.set_scroll_callback(self.window, self.on_scroll)
        
        self.mouse_pressed = False
        self.last_mouse_pos = (0, 0)
    
    def on_key(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        elif key == glfw.KEY_UP and (action == glfw.PRESS or action == glfw.REPEAT):
            self.brain_activity_level = min(1.0, self.brain_activity_level + 0.05)
        elif key == glfw.KEY_DOWN and (action == glfw.PRESS or action == glfw.REPEAT):
            self.brain_activity_level = max(0.0, self.brain_activity_level - 0.05)
        elif key == glfw.KEY_SPACE and action == glfw.PRESS:
            self.trigger_activity_burst()
    
    def on_mouse_button(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT:
            self.mouse_pressed = action == glfw.PRESS
            if self.mouse_pressed:
                self.last_mouse_pos = glfw.get_cursor_pos(window)
    
    def on_mouse_move(self, window, xpos, ypos):
        if self.mouse_pressed:
            dx = xpos - self.last_mouse_pos[0]
            dy = ypos - self.last_mouse_pos[1]
            self.camera_angle_y += dx * 0.01
            self.camera_angle_x += dy * 0.01
            self.camera_angle_x = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.camera_angle_x))
            self.last_mouse_pos = (xpos, ypos)
    
    def on_scroll(self, window, xoffset, yoffset):
        self.camera_distance = max(2.0, min(8.0, self.camera_distance - yoffset * 0.2))
    
    def trigger_activity_burst(self):
        self.brain_activity_level = min(1.0, self.brain_activity_level + 0.3)
        self.brain_outer_glow = 0.8
        
        # Spawn multiple pulses
        for _ in range(int(15 + self.brain_activity_level * 20)):
            self.spawn_pulse()
        
        # Add extra sparks
        for _ in range(int(20 + self.brain_activity_level * 30)):
            neuron = random.choice(self.neurons)
            self.sparks.append(Spark(neuron.position))
        
        # Randomly change energy flow direction
        if random.random() < 0.3:
            self.energy_flow_direction *= -1
    
    def init_brain(self):
        """Initialize a realistic 3D brain structure with proper anatomy"""
        # First ensure shaders are loaded
        if not hasattr(self, 'neuron_shader'):
            self.load_shaders()

        # Generate brain point cloud
        brain_points = self._generate_brain_point_cloud(num_points=2000)
        
        # Create neurons from point cloud
        self.neurons = []
        for pos in brain_points:
            neuron = Neuron(Vector3(pos, dtype='f4'), 0.0)
            neuron.radius = 0.015  # Match original size
            neuron.base_position = Vector3(pos, dtype='f4')  # For animation
            self.neurons.append(neuron)

        # Create organic connections
        self._create_brain_connections()

        # Initialize layers
        self.brain_layers = [self.neurons]

    

    def _generate_brain_point_cloud(self, num_points=2000):
        """Generate anatomically accurate brain point cloud"""
        points = []
        
        # Hemisphere parameters
        hemisphere_scale = 1.5
        fissure_depth = 0.3
        lobe_asymmetry = 0.15
        
        # Generate points for each hemisphere
        for hemisphere in [-1, 1]:  # Left/right
            for _ in range(num_points // 2):
                # Base spherical coordinates with noise
                theta = np.random.uniform(0, 2*np.pi)
                phi = np.random.uniform(0, np.pi)
                
                # Core brain shape (ellipsoid)
                r = 0.8 + 0.2*snoise3(theta*3, phi*3, hemisphere, octaves=2)
                
                # Add longitudinal fissure
                fissure = (1 - fissure_depth * np.abs(np.sin(theta*2)))
                
                # Lobe-specific shaping
                if theta < np.pi:  # Frontal lobe
                    lobe_shape = 1.0 + lobe_asymmetry * snoise3(theta*5, 0, 0)
                else:  # Occipital/temporal
                    lobe_shape = 0.9 + 0.1 * snoise3(0, phi*5, hemisphere)
                
                # Cortical folding with multi-scale noise
                fold1 = 0.12 * snoise3(theta*8, phi*8, hemisphere, octaves=1)
                fold2 = 0.08 * snoise3(theta*20, phi*20, hemisphere+100, octaves=1)
                
                # Final position calculation
                x = hemisphere * fissure * lobe_shape * r * np.sin(phi) * np.cos(theta)
                y = (0.7 + 0.3*np.cos(phi*2)) * r * np.cos(phi)  # Flattened superior-inferior
                z = lobe_shape * r * np.sin(phi) * np.sin(theta)
                
                # Add folding
                x += fold1 + 0.5*fold2
                y += 0.7*fold1 + 0.3*fold2
                z += 0.6*fold1 + 0.4*fold2
                
                # Scale to fit animation space
                pt = np.array([x, y, z]) * hemisphere_scale
                points.append(pt)
        
        return np.array(points)

    def _create_brain_connections(self):
        """Create anatomically inspired neural connections"""
        from scipy.spatial import KDTree
        
        self.connections = []
        positions = np.array([n.position.xyz for n in self.neurons])
        kdtree = KDTree(positions)
        
        # Connection parameters
        local_connections = 6
        long_range_prob = 0.1
        
        for i, neuron in enumerate(self.neurons):
            # Local connections (gray matter)
            _, local_indices = kdtree.query(positions[i], k=local_connections+1)
            
            for j in local_indices[1:]:  # Skip self
                if j not in neuron.connections:
                    self._add_connection(i, j, strength=0.9)
            
            # Long-range connections (white matter tracts)
            if np.random.random() < long_range_prob:
                # Find distant point in same hemisphere
                same_hemisphere = np.sign(positions[i][0]) == np.sign(positions[:,0])
                distant_points = np.where(same_hemisphere & 
                                        (np.linalg.norm(positions - positions[i], axis=1) > 1.0))[0]
                
                if len(distant_points) > 0:
                    j = np.random.choice(distant_points)
                    if j not in neuron.connections:
                        self._add_connection(i, j, strength=0.7)
        
        # Corpus callosum connections
        midline_neurons = [i for i, n in enumerate(self.neurons) 
                        if abs(n.position.x) < 0.2]
        for i in midline_neurons:
            mirror_pos = positions[i].copy()
            mirror_pos[0] *= -1  # Mirror across midline
            _, j = kdtree.query(mirror_pos, k=1)
            if j != i and j not in self.neurons[i].connections:
                self._add_connection(i, j, strength=0.85)

    def _add_connection(self, i, j, strength):
        """Helper to add connection with strength"""
        self.connections.append((i, j))
        self.neurons[i].connections.append(j)
        self.neurons[j].connections.append(i)
        self.neurons[i].connection_strengths[id(self.neurons[j])] = strength
        self.neurons[j].connection_strengths[id(self.neurons[i])] = strength
    
    def load_shaders(self):
        try:
            # Neuron shader - simplified for small, consistent neurons
            self.neuron_shader = self.ctx.program(
                vertex_shader=''' #version 330
                uniform mat4 model;
                uniform mat4 view;
                uniform mat4 projection;
                uniform float time;
                uniform float global_glow;
                uniform float global_pulse;
                uniform vec3 camera_pos;

                in vec3 in_position;
                in float in_radius;
                in vec3 in_color;
                in float in_activity;
                in float in_glow_size;
                in float in_halo_intensity;
                in float in_spark_intensity;

                out vec3 v_color;
                out float v_radius;
                out float v_activity;
                out float v_glow_size;
                out float v_halo_intensity;
                out float v_spark_intensity;
                out float v_global_pulse;
                out float v_camera_dist;

                float clamp(float value, float min, float max) {
                    return max(min, min(value, max));
                }

                void main() {
                    vec4 world_pos = model * vec4(in_position, 1.0);
                    gl_Position = projection * view * world_pos;
                    v_camera_dist = distance(world_pos.xyz, camera_pos);
                    
                    v_color = in_color;
                    v_radius = in_radius;
                    v_activity = in_activity;
                    v_glow_size = in_glow_size;
                    v_halo_intensity = in_halo_intensity;
                    v_spark_intensity = in_spark_intensity;
                    v_global_pulse = global_pulse;
                    
                    // Very subtle movement
                    float pulse_x = sin(time * 2.0 + in_position.x * 10.0) * 0.002;
                    float pulse_y = cos(time * 1.8 + in_position.y * 8.0) * 0.002;
                    float pulse_z = sin(time * 2.2 + in_position.z * 6.0) * 0.001;
                    
                    gl_Position.x += pulse_x * (1.0 + in_activity);
                    gl_Position.y += pulse_y * (1.0 + in_activity);
                    gl_Position.z += pulse_z * (1.0 + in_activity);
                    
                    // Clamp the point size
                    float base_size = in_radius * 2000.0 / gl_Position.w;
                    float size_mod = global_glow * (1.0 + in_activity * 0.5);
                    gl_PointSize = clamp(base_size * size_mod, 1.0, 40.0); // Clamping point size
                }
                ''',
                fragment_shader=''' #version 330
                    in vec3 v_color;
                    in float v_radius;
                    in float v_activity;
                    in float v_glow_size;
                    in float v_halo_intensity;
                    in float v_global_pulse;
                    in float v_spark_intensity;
                    in float v_camera_dist;
                    
                    out vec4 f_color;
                    
                    float hash(vec2 p) {
                        vec3 p3 = fract(vec3(p.xyx) * 0.1031);
                        p3 += dot(p3, p3.yzx + 33.33);
                        return fract((p3.x + p3.y) * p3.z);
                    }
                    
                    void main() {
                        vec2 coord = gl_PointCoord - vec2(0.5);
                        float dist = length(coord);
                        if (dist > 0.5) discard;
                        
                        // Subtle noise for organic feel
                        float noise = hash(gl_FragCoord.xy) * 0.3;
                        
                        // Core glow
                        float core = smoothstep(0.8, 0.3, dist);
                        float intensity = 1.2 - smoothstep(0.2, 0.5, dist);
                        intensity += noise * 0.5;
                        
                        // Outer glow - subtle
                        float outer_glow = (1.0 - smoothstep(0.0, 0.7, dist)) * 0.8;
                        outer_glow *= v_glow_size;
                        
                        // Activity effects - subtle
                        float pulse = v_activity * 0.8 * (1.0 - dist * 1.2);
                        
                        // Halo effect - subtle
                        float halo = v_halo_intensity * max(0.0, 0.6 - dist) * 1.5;
                        
                        // Spark effect - subtle
                        float spark = v_spark_intensity * (1.0 - smoothstep(0.2, 0.5, dist)) * 1.5;
                        
                        // Combine all effects
                        intensity = (intensity + pulse) * 1.2 + outer_glow + halo + spark;
                        
                        // Final color - maintain blue hue
                        vec3 final_color = v_color * intensity;
                        final_color += vec3(0.2, 0.5, 1.0) * pulse * 0.8;
                        final_color += vec3(0.0, 0.7, 1.0) * halo;
                        final_color += vec3(0.3, 0.8, 1.0) * spark;
                        
                        // Subtle fade with distance
                        float fade = smoothstep(12.0, 8.0, v_camera_dist);
                        
                        f_color = vec4(final_color, intensity * 0.7 * fade);
                    }
                '''
            )

            # Connection shader - simplified for cleaner lines
            self.connection_shader = self.ctx.program(
                vertex_shader='''#version 330
                    uniform mat4 model;
                    uniform mat4 view;
                    uniform mat4 projection;
                    uniform float time;
                    uniform float global_pulse;

                    in vec3 in_position;
                    in vec3 in_color;
                    in float in_pulse;

                    out vec3 v_color;
                    out float v_pulse;
                    out float v_global_pulse;

                    void main() {
                        // Very subtle movement
                        float wave_x = sin(time * 3.0 + in_position.x * 8.0) * 0.002;
                        float wave_y = cos(time * 2.8 + in_position.y * 6.0) * 0.002;
                        float wave_z = sin(time * 3.5 + in_position.z * 4.0) * 0.001;
                        
                        vec3 pos = in_position;
                        pos.x += wave_x;
                        pos.y += wave_y;
                        pos.z += wave_z;
                        
                        gl_Position = projection * view * model * vec4(pos, 1.0);
                        v_color = in_color;
                        v_pulse = in_pulse;
                        v_global_pulse = global_pulse;
                    }
                ''',
                fragment_shader='''#version 330
                    in vec3 v_color;
                    in float v_pulse;
                    in float v_global_pulse;

                    out vec4 f_color;

                    void main() {
                        // Subtle glow with pulse effects
                        float alpha = 0.15 + 0.2 * (v_pulse + v_global_pulse * 0.5);
                        vec3 glow_color = v_color * (1.2 + (v_pulse + v_global_pulse) * 2.0);
                        
                        // Subtle energy flow effect
                        float flow = sin(gl_FragCoord.x * 40.0) * 0.2 + 0.2;
                        glow_color += vec3(0.2, 0.6, 0.8) * flow * (0.5 + v_pulse + v_global_pulse);
                        
                        f_color = vec4(glow_color, alpha);
                    }
                    '''
                    )
            # Pulse shader - simplified for cleaner pulses
            self.pulse_shader = self.ctx.program(
                vertex_shader=''' #version 330
                    uniform mat4 model;
                    uniform mat4 view;
                    uniform mat4 projection;
                    uniform float time;
                    uniform vec3 camera_pos;

                    in vec3 in_position;
                    in float in_size;
                    in vec4 in_color;

                    out vec4 v_color;
                    out float v_time;
                    out float v_camera_dist;

                    float clamp(float value, float min, float max) {
                        return max(min, min(value, max));
                    }

                    void main() {
                        vec4 world_pos = model * vec4(in_position, 1.0);
                        gl_Position = projection * view * world_pos;
                        v_color = in_color;
                        v_time = time;
                        v_camera_dist = distance(world_pos.xyz, camera_pos);
                        
                        // Clamp the point size
                        gl_PointSize = clamp(in_size * 1500.0 / gl_Position.w, 1.0, 40.0); // Clamping point size
                    }
                ''',
                fragment_shader='''#version 330
                    in vec4 v_color;
                    in float v_time;
                    in float v_camera_dist;
                    
                    out vec4 f_color;
                    
                    float hash(vec2 p) {
                        vec3 p3 = fract(vec3(p.xyx) * 0.1031);
                        p3 += dot(p3, p3.yzx + 33.33);
                        return fract((p3.x + p3.y) * p3.z);
                    }
                    
                    void main() {
                        vec2 coord = gl_PointCoord - vec2(0.5);
                        float dist = length(coord);
                        if (dist > 0.5) discard;
                        
                        // Subtle noise
                        float noise = hash(gl_FragCoord.xy) * 0.5;
                        
                        // Core intensity
                        float intensity = 2.0 - smoothstep(0.1, 0.4, dist);
                        intensity += noise * 0.8;
                        
                        // Subtle ripple effect
                        float ripple = sin(v_time * 15.0 + dist * 30.0) * 0.2 + 0.2;
                        
                        // Outer glow
                        float outer_glow = (1.0 - smoothstep(0.0, 0.6, dist)) * 1.5;
                        
                        // Combine effects
                        intensity = intensity * 1.5 + outer_glow + ripple * smoothstep(0.3, 0.5, dist);
                        
                        // Final color - maintain blue hue
                        vec3 final_color = v_color.rgb * intensity;
                        
                        // Subtle fade with distance
                        float fade = smoothstep(12.0, 8.0, v_camera_dist);
                        
                        f_color = vec4(final_color, v_color.a * intensity * 0.7 * fade);
                    }
                '''
            )

            # Spark shader - simplified
            self.spark_shader = self.ctx.program(
                vertex_shader='''#version 330
                    uniform mat4 model;
                    uniform mat4 view;
                    uniform mat4 projection;
                    uniform float time;
                    uniform vec3 camera_pos;
                    
                    in vec3 in_position;
                    in float in_size;
                    in vec4 in_color;
                    
                    out vec4 v_color;
                    out float v_time;
                    out float v_camera_dist;
                    
                    void main() {
                        vec4 world_pos = model * vec4(in_position, 1.0);
                        gl_Position = projection * view * world_pos;
                        v_color = in_color;
                        v_camera_dist = distance(world_pos.xyz, camera_pos);
                        gl_PointSize = in_size * 1200.0 / gl_Position.w;
                        v_time = time;
                    }
                ''',
                fragment_shader='''#version 330
                    in vec4 v_color;
                    in float v_camera_dist;
                    
                    out vec4 f_color;
                    
                    void main() {
                        vec2 coord = gl_PointCoord - vec2(0.5);
                        float dist = length(coord);
                        if (dist > 0.5) discard;
                        
                        // Simple glow
                        float intensity = 2.0 - smoothstep(0.1, 0.5, dist);
                        
                        // Radial gradient
                        float radial = smoothstep(0.7, 0.3, dist) * 0.6;
                        
                        // Combine effects
                        intensity = (intensity + radial) * 1.8;
                        
                        // Final color
                        vec3 final_color = v_color.rgb * intensity;
                        
                        // Subtle fade with distance
                        float fade = smoothstep(12.0, 8.0, v_camera_dist);
                        
                        f_color = vec4(final_color, v_color.a * intensity * 0.6 * fade);
                    }
                '''
            )

            # Star shader - simplified
            self.star_shader = self.ctx.program(
                vertex_shader='''#version 330
                    uniform mat4 view;
                    uniform mat4 projection;
                    uniform float time;
                    
                    in vec3 in_position;
                    in float in_size;
                    in float in_brightness;
                    
                    out float v_brightness;
                    
                    void main() {
                        mat4 inv_view = inverse(view);
                        vec4 world_pos = inv_view * vec4(in_position, 1.0);
                        
                        // Subtle twinkle
                        float twinkle = sin(time * 1.5 + in_position.x * 50.0) * 0.05 + 0.95;
                        
                        gl_Position = projection * view * world_pos;
                        gl_PointSize = in_size * 800.0 / gl_Position.w * twinkle;
                        v_brightness = in_brightness * twinkle;
                    }
                ''',
                fragment_shader='''#version 330
                    in float v_brightness;
                    
                    out vec4 f_color;
                    
                    void main() {
                        vec2 coord = gl_PointCoord - vec2(0.5);
                        float dist = length(coord);
                        if (dist > 0.5) discard;
                        
                        float intensity = 1.0 - smoothstep(0.3, 0.5, dist);
                        vec3 color = vec3(0.8, 0.9, 1.0) * intensity * v_brightness;
                        
                        f_color = vec4(color, intensity * 0.6);
                    }
                '''
            )

            # Glow shader - simplified
            self.glow_shader = self.ctx.program(
                vertex_shader='''#version 330
                    uniform mat4 model;
                    uniform mat4 view;
                    uniform mat4 projection;
                    uniform float time;
                    uniform float glow_intensity;
                    
                    in vec3 in_position;
                    
                    out float v_glow;
                    
                    void main() {
                        vec3 pos = in_position * (1.0 + glow_intensity * 0.2);
                        gl_Position = projection * view * model * vec4(pos, 1.0);
                        v_glow = (sin(time * 0.5 + in_position.x * 5.0) * 0.1 + 0.9) * glow_intensity;
                    }
                ''',
                fragment_shader='''#version 330
                    in float v_glow;
                    
                    out vec4 f_color;
                    
                    void main() {
                        vec3 color = vec3(0.3, 0.5, 1.0) * v_glow * 0.4;
                        f_color = vec4(color, 0.15 * v_glow);
                    }
                '''
            )

        except Exception as e:
            print(f"Shader compilation error: {e}")
            glfw.terminate()
            raise
    
    def create_buffers(self):
        # Neuron buffer (updated each frame)
        self.neuron_buffer = self.ctx.buffer(reserve=len(self.neurons) * 11 * 4)
        
        # Connection buffer (static)
        connection_data = []
        for i, j in self.connections:
            start_pos = self.neurons[i].position
            end_pos = self.neurons[j].position
            # Use consistent blue color for connections
            color = (0.3, 0.6, 1.0)
            connection_data.extend(start_pos)
            connection_data.extend(color)
            connection_data.append(0.0)  # Initial pulse value
            connection_data.extend(end_pos)
            connection_data.extend(color)
            connection_data.append(0.0)  # Initial pulse value
        
        self.connection_buffer = self.ctx.buffer(np.array(connection_data, dtype='f4'))
        
        # VAOs
        self.neuron_vao = self.ctx.vertex_array(
            self.neuron_shader,
            [
                (self.neuron_buffer, '3f 1f 3f 1f 1f 1f 1f', 
                 'in_position', 'in_radius', 'in_color', 'in_activity', 'in_glow_size', 'in_halo_intensity', 'in_spark_intensity')
            ]
        )
        
        self.connection_vao = self.ctx.vertex_array(
            self.connection_shader,
            [
                (self.connection_buffer, '3f 3f 1f', 'in_position', 'in_color', 'in_pulse')
            ]
        )
        
        # Pulse buffer (dynamic)
        self.pulse_buffer = self.ctx.buffer(reserve=4096 * 8 * 4)
        self.pulse_vao = self.ctx.vertex_array(
            self.pulse_shader,
            [
                (self.pulse_buffer, '3f 1f 4f', 'in_position', 'in_size', 'in_color')
            ]
        )
        
        # Spark buffer (dynamic)
        self.spark_buffer = self.ctx.buffer(reserve=2048 * 8 * 4)
        self.spark_vao = self.ctx.vertex_array(
            self.spark_shader,
            [
                (self.spark_buffer, '3f 1f 4f', 'in_position', 'in_size', 'in_color')
            ]
        )
        
        # Star buffer (static)
        star_data = []
        for star in self.star_positions:
            star_data.extend(star[:3])  # position
            star_data.append(star[3])   # size
            star_data.append(star[4])   # brightness
        
        self.star_buffer = self.ctx.buffer(np.array(star_data, dtype='f4'))
        self.star_vao = self.ctx.vertex_array(
            self.star_shader,
            [
                (self.star_buffer, '3f 1f 1f', 'in_position', 'in_size', 'in_brightness')
            ]
        )
        
        # Glow sphere buffer
        glow_sphere = []
        num_segments = 24  # Lower resolution for performance
        for i in range(num_segments + 1):
            theta1 = math.pi * i / num_segments
            theta2 = math.pi * (i + 1) / num_segments
            
            for j in range(num_segments + 1):
                phi = 2 * math.pi * j / num_segments
                
                x1 = math.sin(theta1) * math.cos(phi)
                y1 = math.cos(theta1)
                z1 = math.sin(theta1) * math.sin(phi)
                
                x2 = math.sin(theta2) * math.cos(phi)
                y2 = math.cos(theta2)
                z2 = math.sin(theta2) * math.sin(phi)
                
                glow_sphere.extend([x1, y1, z1])
                glow_sphere.extend([x2, y2, z2])
        
        self.glow_buffer = self.ctx.buffer(np.array(glow_sphere, dtype='f4'))
        self.glow_vao = self.ctx.vertex_array(
            self.glow_shader,
            [
                (self.glow_buffer, '3f', 'in_position')
            ]
        )

    def spawn_pulse(self):
        if len(self.connections) > 0:
            # Choose connection based on activity and connection strength
            conn_idx = random.randint(0, len(self.connections) - 1)
            i, j = self.connections[conn_idx]
            
            # Alternate direction based on global flow direction
            if self.energy_flow_direction > 0:
                start, end = i, j
            else:
                start, end = j, i
                
            speed = 0.008 + random.uniform(0, 0.02) * self.brain_activity_level
            self.pulses.append(EnergyPulse(self.neurons[start], self.neurons[end], speed, self.brain_activity_level))
            
            # Activate starting neuron
            self.neurons[start].activity = min(1.0, self.neurons[start].activity + 0.7)
            self.neurons[start].halo_intensity = 1.2
            
            # Occasionally spawn sparks
            if random.random() < 0.3 * self.brain_activity_level:
                self.sparks.append(Spark(self.neurons[start].position))

    def update(self):
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time
        self.time += delta_time
        
        # Update brain outer glow
        self.brain_outer_glow = max(0.0, self.brain_outer_glow - delta_time * 0.3)
        
        # Global glow pulsation with subtle variation
        self.global_glow_factor = 0.9 + 0.1 * math.sin(self.time * 0.5)
        
        # Global pulse effect that syncs with activity
        self.global_pulse_factor = math.sin(self.time * 2.5) * 0.5 * self.brain_activity_level
        
        # Occasionally change energy flow direction
        if random.random() < 0.005:
            self.energy_flow_direction *= -1
        
        # Update neurons with organic movement
        for neuron in self.neurons:
            neuron.update(self.time, self.brain_activity_level)
            
            # Occasionally spawn sparks from active neurons
            if neuron.activity > 0.2 and random.random() < 0.02 * self.brain_activity_level:
                self.sparks.append(Spark(
                    neuron.position,
                    color=neuron.current_color,
                    size=random.uniform(0.008, 0.02)
                ))
        
        # Update pulses
        for pulse in self.pulses[:]:
            pulse.update()
            if not pulse.alive:
                self.pulses.remove(pulse)
        
        # Spawn new pulses based on activity level
        spawn_prob = 0.05 * self.brain_activity_level
        if random.random() < spawn_prob:
            self.spawn_pulse()
        
        # Update sparks
        for spark in self.sparks[:]:
            spark.update()
            if spark.life <= 0:
                self.sparks.remove(spark)
        
        # Add random sparks occasionally
        if random.random() < 0.02 * self.brain_activity_level:
            neuron = random.choice(self.neurons)
            self.sparks.append(Spark(
                neuron.position,
                color=neuron.current_color,
                size=random.uniform(0.008, 0.02)
            ))
        
        # Update camera position with smooth rotation
        target_rot_x = self.camera_angle_x
        target_rot_y = self.camera_angle_y
        
        rot_x = Quaternion.from_x_rotation(target_rot_x)
        rot_y = Quaternion.from_y_rotation(target_rot_y)
        self.camera_rotation = rot_y * rot_x
        
        # Add subtle automatic rotation
        auto_rot_y = Quaternion.from_y_rotation(self.time * 0.03)
        self.camera_rotation = auto_rot_y * self.camera_rotation
        
        self.camera_pos = self.camera_rotation * Vector3([0, 0, self.camera_distance], dtype='f4')
        
        # Update neuron buffer
        neuron_data = []
        for neuron in self.neurons:
            neuron_data.extend(neuron.position)
            neuron_data.append(neuron.current_radius)
            neuron_data.extend(neuron.current_color)
            neuron_data.append(neuron.activity)
            neuron_data.append(neuron.glow_size)
            neuron_data.append(neuron.halo_intensity)
            neuron_data.append(neuron.spark_intensity)
        
        self.neuron_buffer.write(np.array(neuron_data, dtype='f4'))
        
        # Update pulse buffer with trails
        pulse_data = []
        for pulse in self.pulses:
            # Main pulse
            pos = pulse.get_current_position()
            pulse_data.extend(pos)
            pulse_data.append(pulse.size)
            pulse_data.extend(pulse.color)
            
            # Trail points
            for i, (trail_pos, trail_size, trail_color) in enumerate(zip(
                pulse.trail_positions, pulse.trail_sizes, pulse.trail_colors
            )):
                pulse_data.extend(trail_pos)
                pulse_data.append(trail_size)
                pulse_data.extend(trail_color)
            
            # Spark particles
            for spark in pulse.spark_positions:
                pulse_data.extend(spark['position'])
                pulse_data.append(spark['size'])
                pulse_data.extend(spark['color'])
        
        if pulse_data:
            self.pulse_buffer.write(np.array(pulse_data, dtype='f4'))
        
        # Update spark buffer
        spark_data = []
        for spark in self.sparks:
            spark_data.extend(spark.position)
            spark_data.append(spark.size)
            spark_data.extend(spark.color)
        
        if spark_data:
            self.spark_buffer.write(np.array(spark_data, dtype='f4'))

    def render(self):
        self.ctx.clear(0.02, 0.03, 0.05, 1.0)  # Dark blue background
        
        # Calculate matrices
        width, height = glfw.get_framebuffer_size(self.window)
        aspect_ratio = width / height
        projection = Matrix44.perspective_projection(
            45.0, aspect_ratio, 0.1, 100.0
        )
        
        view = Matrix44.look_at(
            self.camera_pos.xyz,
            self.camera_target.xyz,
            self.camera_up.xyz
        )
        
        model = Matrix44.identity()
        
        # Draw stars first (background)
        self.star_shader['view'].write(view.astype('f4').tobytes())
        self.star_shader['projection'].write(projection.astype('f4').tobytes())
        self.star_shader['time'].value = self.time
        self.star_vao.render(moderngl.POINTS, vertices=len(self.star_positions))
        
        # Draw brain outer glow if active
        if self.brain_outer_glow > 0:
            self.ctx.enable(moderngl.BLEND)
            self.glow_shader['model'].write(model.astype('f4').tobytes())
            self.glow_shader['view'].write(view.astype('f4').tobytes())
            self.glow_shader['projection'].write(projection.astype('f4').tobytes())
            self.glow_shader['time'].value = self.time
            self.glow_shader['glow_intensity'].value = self.brain_outer_glow
            self.glow_vao.render(moderngl.TRIANGLE_STRIP, vertices=self.glow_buffer.size // (3 * 4))
        
        # Draw connections FIRST (before neurons)
        self.connection_shader['model'].write(model.astype('f4').tobytes())
        self.connection_shader['view'].write(view.astype('f4').tobytes())
        self.connection_shader['projection'].write(projection.astype('f4').tobytes())
        self.connection_shader['time'].value = self.time
        self.connection_shader['global_pulse'].value = self.global_pulse_factor
        self.connection_vao.render(moderngl.LINES, vertices=len(self.connections)*2)  # Note: *2 for line segments
        
        # Draw neurons with glow effects
        self.neuron_shader['model'].write(model.astype('f4').tobytes())
        self.neuron_shader['view'].write(view.astype('f4').tobytes())
        self.neuron_shader['projection'].write(projection.astype('f4').tobytes())
        self.neuron_shader['time'].value = self.time
        self.neuron_shader['global_glow'].value = self.global_glow_factor
        self.neuron_shader['global_pulse'].value = self.global_pulse_factor
        self.neuron_shader['camera_pos'].value = self.camera_pos.xyz
        self.neuron_vao.render(moderngl.POINTS, vertices=len(self.neurons))
        
        # Draw pulses with glow effects
        if self.pulses:
            self.pulse_shader['model'].write(model.astype('f4').tobytes())
            self.pulse_shader['view'].write(view.astype('f4').tobytes())
            self.pulse_shader['projection'].write(projection.astype('f4').tobytes())
            self.pulse_shader['time'].value = self.time
            self.pulse_shader['camera_pos'].value = self.camera_pos.xyz
            self.pulse_vao.render(moderngl.POINTS, vertices=self.pulse_buffer.size // (8 * 4))
        
        # Draw sparks
        if self.sparks:
            self.spark_shader['model'].write(model.astype('f4').tobytes())
            self.spark_shader['view'].write(view.astype('f4').tobytes())
            self.spark_shader['projection'].write(projection.astype('f4').tobytes())
            self.spark_shader['time'].value = self.time
            self.spark_shader['camera_pos'].value = self.camera_pos.xyz
            self.spark_vao.render(moderngl.POINTS, vertices=self.spark_buffer.size // (8 * 4))
        
        glfw.swap_buffers(self.window)


    def run(self):
        while not glfw.window_should_close(self.window):
            self.update()
            self.render()
            glfw.poll_events()
        
        glfw.terminate()

if __name__ == "__main__":
    visualizer = AIVisualizer()
    visualizer.run()





