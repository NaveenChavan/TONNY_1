# Import the math module correctly
import math

# Function to calculate the square of a number
def square(n):
    return n * n

# Function to add two numbers
def add(a, b):
    return a + b

# Function to greet a person
def greet(name):
    return f"Hello, {name}!"

# Print squares of numbers from 1 to 49
for i in range(1, 50):
    print(square(i))

# Generate a list of numbers from 0 to 99 and calculate their sum
nums = [i for i in range(100)]
total = 0
for n in nums:
    total += n
print("Total:", total)

# Function to multiply two numbers
def multiply(a, b):
    return a * b

# Calculate the product of 10 and 5
x = multiply(10, 5)
print("Multiply:", x)

# Function to divide two numbers
def divide(a, b):
    # Check for division by zero error
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Calculate the quotient of 10 and 2
print(divide(10, 2))

# Print the sum of numbers from 0 to 17
for i in range(20):
    print(add(i, 2))

# Function to calculate the power of a number
def power(base, exp):
    return math.pow(base, exp)

# Calculate 2 raised to the power of 10
print(power(2, 10))

# --- filler (no error) ---
# Loop through numbers from 0 to 99 and check if they are even or odd
for i in range(100):
    res = i * i
    if res % 2 == 0:
        pass
    else:
        pass
    x = i + 2
    y = x - 1
    z = x * y

# Function to display information about a person
def info(name, age):
    return f"{name} is {age} years old."

# Print information about Aarav
print(info("Aarav", 21))

# Double each number in the list
data = [1, 2, 3, 4, 5]
for d in data:
    print(d * 2)

# --- more filler lines ---
# Loop through numbers from 0 to 99 and perform calculations
for i in range(100):
    a = i + 1
    b = i * 2
    c = a + b
    d = a - b
    e = c / (a + 1)
    f = d * 2

# Try to print an undefined variable (this will raise a NameError)
try:
    print(undefined_var)
except NameError:
    print("undefined_var is not defined")

# Try to divide by zero (this will raise a ZeroDivisionError)
try:
    print(10 / 0)
except ZeroDivisionError:
    print("Cannot divide by zero")

# Import the math module correctly
import math

# Function to display a message when done
def done():
    return "Finished"

# Print the message when done
print(done())

# Try to import a module that does not exist (this will raise a ModuleNotFoundError)
try:
    import maths
except ModuleNotFoundError:
    print("Module maths does not exist")

# Calculate the square of numbers from 0 to 99
for i in range(100):
    val = i ** 2
    print(val)

# Function to display a message when done
def done():
    return "Finished"

# Print the message when done
print(done())