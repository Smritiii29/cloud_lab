
import Pyro4

name_server = Pyro4.locateNS()
calc_uri = name_server.lookup("ex2.calculator")

calculator = Pyro4.Proxy(calc_uri)

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

print("Addition:", calculator.add(num1, num2))
print("Subtraction:", calculator.sub(num1, num2))
print("Multiplication:", calculator.mul(num1, num2))

if num2 == 0:
    print("Division: Cannot divide by zero")
else:
    print("Division:", calculator.div(num1, num2))
