# Ember

Welcome to the **Ember**, a simple and dynamic programming language built for a simpler version of **Python**. This Language supports basic operations like printing, variable declarations, loops, conditions, file operations, error handling, and Python code execution. It also allows for dynamic class creation with getters and setters.



## Supported Operating Systems

### Current Support
- Mac - Full Support
- Windows - Partial Support - Only through python using ember.py
- Linux - No Support - Experimental and Untested - May Break Often - Uses the ember.py file

## Features

### 1. Print Statements
In **Ember**, you can print without using parentheses. You can print variables and custom messages.

**Example:**
```
print "Hello, Ember"
```

### 2. Variable Declaration
Declare variables using the `=` sign, just like in Python.

**Example:**
```
x = 5
y = 10
print x
```
### 3. Repeat Loops
Ember supports loops through the `repeat N times:` syntax, where `N` is the number of repetitions.

**Example:**
```
repeat 3 times:
    print "Looping"
```

### 4. Conditions (if statements)
Conditional statements in Ember can check for equality or whether a value is within a range.

- **Equality check:** `if x is 5:`
- **Range check:** `if y between 5 and 15:`

**Example:**
```
if x is 5:
    print "x is 5"

if y between 5 and 15:
    print "y is between 5 and 15"
```

### 5. Python Block Execution
Ember is directly compatibel with python code !
You can embed Python code inside an Ember script. The code inside the `python:` block is executed as standard Python code.

**Example:**
```
python:
    x = 100
end_python:
print x  # Output will be 100
```

### 6. File Operations
File operations are a lot simpler in ember using the `read_file` and `write_file` commands.

- **write_file**: Writes content to a file.
- **read_file**: Reads content from a file.

**Example:**
```
write_file "test.txt", "This is a test file!"
read_file "test.txt"
```

### 7. Custom Error Handling
Ember Uses `attempt` and `on_error` blocks to handle errors gracefully.

**Example:**
```
attempt:
    python: raise Exception("Oops!")
on_error:
    print "An error occurred"
```

### 8. Dynamic Class Creation
Ember gives you the ability to create classes dynamically and assign attributes using Ember syntax.

**Example:**
```
class MyClass
    x = 5
    print "Inside MyClass"
    print x
```

### Example Ember Code
Below is a full example showcasing all features of the **Ember**:

```
# Print without parentheses
print "Hello, Ember"

# Variable declaration
x = 5
y = 10

# Print a variable
print x

# Repeat loops
repeat 3 times:
    print "Looping"

# Conditions
if x is 5:
    print "x is 5"

if y between 5 and 15:
    print "y is between 5 and 15"

# Python block execution
python:
    x = 100
end_python:

# File Operations
write_file "test.txt", "This is a test file!"
read_file "test.txt"

# Custom Error Handling
attempt:
    python: raise Exception("Oops!")
on_error:
    print "An error occurred"

# Class with dynamic getter and setter
class MyClass
    x = 5
    print "Inside MyClass"
    print x
```

## Installation and Usage

To Install the Ember language:

- **For Mac** - [Go to install-mac.md](install-mac.md)
- **For Windows** - [Go to install-windows.md](install-windows.md)


```
python3 interpreter.py
```

## License
This project is licensed under the MIT License.

---

Created by **The-UnknownHacker - AKA CyberZenDev**
