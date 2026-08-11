# # Take two numbers from the user
# first_value = float(input("Enter first value: "))
# second_value = float(input("Enter second value: "))

# # Take the operation from the user
# operation = input("Enter operation (+, -, *, /, //, %, **): ")

# # Perform the selected operation
# if operation == "+":
#     result = first_value + second_value

# elif operation == "-":
#     result = first_value - second_value

# elif operation == "*":
#     result = first_value * second_value

# elif operation == "/":
#     if second_value != 0:
#         result = first_value / second_value
#     else:
#         result = "Cannot divide by zero"

# elif operation == "//":
#     if second_value != 0:
#         result = first_value // second_value
#     else:
#         result = "Cannot divide by zero"

# elif operation == "%":
#     if second_value != 0:
#         result = first_value % second_value
#     else:
#         result = "Cannot divide by zero"

# elif operation == "**":
#     result = first_value ** second_value

# else:
#     result = "Invalid operation"

# print("Result:", result)


                # calculator using functions

      # Function for addition
def add(a, b):
    return a + b


# Function for subtraction
def subtract(a, b):
    return a - b


# Function for multiplication
def multiply(a, b):
    return a * b


# Function for division
def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Cannot divide by zero"


# Function for floor division
def floor_divide(a, b):
    if b != 0:
        return a // b
    else:
        return "Cannot divide by zero"


# Function for modulus
def modulus(a, b):
    if b != 0:
        return a % b
    else:
        return "Cannot divide by zero"


# Function for power
def power(a, b):
    return a ** b


# Take two numbers from the user
first_value = float(input("Enter first value: "))
second_value = float(input("Enter second value: "))


# Take the operation from the user
operation = input("Enter operation (+, -, *, /, //, %, **): ")


# Perform the selected operation
if operation == "+":
    result = add(first_value, second_value)

elif operation == "-":
    result = subtract(first_value, second_value)

elif operation == "*":
    result = multiply(first_value, second_value)

elif operation == "/":
    result = divide(first_value, second_value)

elif operation == "//":
    result = floor_divide(first_value, second_value)

elif operation == "%":
    result = modulus(first_value, second_value)

elif operation == "**":
    result = power(first_value, second_value)

else:
    result = "Invalid operation"


# Display the result
print("Result:", result)