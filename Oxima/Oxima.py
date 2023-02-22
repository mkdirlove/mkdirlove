import keyword

print("List of Python keywords:")
for keyword in keyword.kwlist:
    print(keyword, end=", ")

print("\n\n")
# Boolean variables
a = True
b = False

# None variable
c = None

# Conditional statement
if a and not b:
    print("a is true and b is false")

# Defining a function with a conditional statement and a loop
def count_down(start):
    assert start >= 0, "start must be non-negative"
    for i in range(start, -1, -1):
        if i == 4:
            continue
        elif i % 2 == 0:
            print(i, end=' ')
        else:
            break
    print("Done counting down!")
    return

# Exception handling with finally block and raise keyword
try:
    count_down(0)
except AssertionError as err:
    print(err)
    raise ValueError("Invalid start value. Must be non-negative.") from err
finally:
    print("The program has finished running.")

# Defining a class with a method and an instance variable
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

# Using the class
p = Person("Mark Jade", 22)
p.say_hello()

# Defining a function that uses the global keyword
x = 10

def print_global():
    global x
    x = 5
    print(x)

print_global()
print(x)

# Defining a lambda function
square = lambda x: x**2
print(square(5))

# Defining a function that uses the nonlocal keyword
def outer():
    x = 1
    def inner():
        nonlocal x
        x += 1
        print(x)
    inner()

outer()

# Defining a function that uses the with keyword
with open('example.txt', 'w') as f:
    f.write('Hello, world!')

# Defining a generator function that uses the yield keyword
def countdown(start):
    while start > 0:
        yield start
        start -= 1

for i in countdown(5):
    print(i)

# Deleting a variable
x = 5
print(x)
del x
print("Variable x was deleted\nAnd the error below was caused by del keyword\n")
print(x)  # This line will cause a NameError
try:
    print(x)
except NameError:
    print("The variable does not exist!")
    #print(__peg_parser__)
