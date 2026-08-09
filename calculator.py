# Take two numbers from the user
first_value = float(input("Enter first value: "))
second_value = float(input("Enter second value: "))

# Take the operation from the user
operation = input("Enter operation (+, -, *, /, //, %, **): ")

# Perform the selected operation
if operation == "+":
    result = first_value + second_value

elif operation == "-":
    result = first_value - second_value

elif operation == "*":
    result = first_value * second_value

elif operation == "/":
    if second_value != 0:
        result = first_value / second_value
    else:
        result = "Cannot divide by zero"

elif operation == "//":
    if second_value != 0:
        result = first_value // second_value
    else:
        result = "Cannot divide by zero"

elif operation == "%":
    if second_value != 0:
        result = first_value % second_value
    else:
        result = "Cannot divide by zero"

elif operation == "**":
    result = first_value ** second_value

else:
    result = "Invalid operation"

print("Result:", result)