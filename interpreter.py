import re

class EmberClass:
    def __init__(self):
        self._attributes = {}

    def __getattr__(self, name):
        if name in self._attributes:
            value = self._attributes[name]
            return value
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name != '_attributes':
            self._attributes[name] = value
        else:
            super().__setattr__(name, value)

    def __repr__(self):
        return f"EmberClass(attributes={self._attributes})"


class EmberInterpreter:
    def __init__(self):
        self.variables = {}
        self.classes = {}
        self.printed_conditions = set()

    def run(self, code):
        lines = code.split('\n')
        in_python_block = False
        python_code = ""
        attempt_block = False

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line.startswith('print '):
                self._handle_print(line)

            elif re.match(r'^repeat \d+ times:', line):
                i = self._handle_repeat(line, lines, i)

            elif line.startswith('if '):
                i = self._handle_conditions(line, lines, i)

            elif 'attempt' in line:
                attempt_block = True

            elif 'on_error' in line:
                attempt_block = False

            elif'read_file' in line or 'write_file' in line:
                self._handle_file_ops(line)

            elif line.startswith('python:'):
                in_python_block = True

            elif line.startswith('end_python:'):
                if in_python_block:
                    self._handle_python(python_code)
                    python_code = ""
                    in_python_block = False

            elif line.startswith('class '):
                i = self._handle_class(line, lines, i)

            elif attempt_block and line.startswith('python:'):
                try:
                    exec(line[7:], {}, self.variables | self.classes)
                except Exception as e:
                    print(f"An error occurred: {e}")
                attempt_block = False

            elif line.endswith('.varname'):
                self._handle_access(line)

            else:
                if in_python_block:
                    python_code += line + "\n"
                else:
                    self._handle_assignment(line)

            i += 1

    def _handle_print(self, line):
        message = line[len('print '):].strip()
        if '.' in message:
            class_name, attr_name = message.split('.')
            if class_name in self.classes:
                if hasattr(self.classes[class_name], attr_name):
                    value = getattr(self.classes[class_name], attr_name)
                    print(value)
                else:
                    print(f"Error: {attr_name} not found in {class_name}")
            else:
                print(f"Error: Class {class_name} not found")
        else:
            try:
                result = eval(message, {}, self.variables | self.classes)
                if result is not None:
                    print(result)
            except Exception as e:
                print(f"Error in print: {e}")
                
    def _handle_repeat(self, line, lines, i):
        count = int(line.split()[1])
        indent_level = line.count(' ')
        start_i = i + 1

        for j in range(start_i, len(lines)):
            if lines[j].startswith(' ' * (indent_level + 4)):
                continue
            else:
                end_i = j
                break
        else:
            end_i = len(lines)

        for _ in range(count):
            nested_i = start_i
            while nested_i < end_i:
                line = lines[nested_i].strip()
                if line.startswith('print '):
                    self._handle_print(line)
                elif line.startswith('python:'):
                    self._handle_python(line[7:])
                elif'read_file' in line or 'write_file' in line:
                    self._handle_file_ops(line)
                elif line.endswith('.varname'):
                    self._handle_access(line)
                elif line.startswith('if '):
                    nested_i = self._handle_conditions(line, lines, nested_i)
                else:
                    self._handle_assignment(line)
                nested_i += 1

        return end_i

    def _handle_conditions(self, line, lines, i):
        condition = line[3:].strip()
        if condition in self.printed_conditions:
            return i + 1  # Skip printing if already printed

        result = None

        if 'is' in condition:
            var, value = condition.split(' is ')
            var = var.strip()
            value = value.strip().rstrip(':')
            try:
                result = self.variables.get(var) == int(value)
            except ValueError:
                print(f"Error: Could not evaluate condition for {var}")

        elif 'between' in condition:
            var, range_part = condition.split(' between ')
            var = var.strip()
            range_part = range_part.rstrip(':')
            low, high = map(lambda x: int(x.strip().rstrip(':')), range_part.split(' and '))
            result = low <= self.variables.get(var, float('inf')) <= high

        # Print only if the condition evaluates to True
        if result:
            self.printed_conditions.add(condition)
            if 'is' in condition:
                print(f"{var.strip()} is {value.strip().rstrip(':')}")
            elif 'between' in condition:
                print(f"{var.strip()} is between {low} and {high}")

        return i + 1


    def _handle_file_ops(self, line):
        if line.startswith('read_file'):
            filename = re.findall(r'\"(.+?)\"', line)[0]
            with open(filename, 'r') as f:
                print(f.read())
        elif line.startswith('write_file'):
            filename, content = re.findall(r'\"(.+?)\", \"(.+?)\"', line)[0]
            with open(filename, 'w') as f:
                f.write(content)

    def _handle_python(self, python_code):
        try:
            exec(python_code, {}, self.variables | self.classes)
        except Exception as e:
            print(f"Python Execution Error: {e}")

    def _handle_assignment(self, line):
        if '=' in line:
            var, value = line.split('=')
            var = var.strip()
            value = value.strip()

            if '.' in var:
                class_name, attr_name = var.split('.')
                if class_name in self.classes:
                    setattr(self.classes[class_name], attr_name, eval(value, {}, self.variables))
                else:
                    print(f"Error: Class {class_name} not found")
            else:
                self.variables[var] = eval(value, {}, self.variables)

    def _handle_access(self, line):
        var = line.split()[-1]
        if '.' in var:
            class_name, attr_name = var.split('.')
            if class_name in self.classes:
                if hasattr(self.classes[class_name], attr_name):
                    print(getattr(self.classes[class_name], attr_name))
                else:
                    print(f"Error: {attr_name} not found in {class_name}")
            else:
                print(f"Error: Class {class_name} not found")

    def _handle_class(self, line, lines, i):
        class_name = line[len('class '):].strip()

        ember_class = EmberClass()
        self.classes[class_name] = ember_class

        indent_level = line.count('    ')
        start_i = i + 1

        for j in range(start_i, len(lines)):
            if lines[j].startswith(' ' * (indent_level + 4)):
                body_line = lines[j].strip()
                if body_line.startswith('print '):
                    self._handle_print(body_line)
                elif '=' in body_line:
                    var, value = body_line.split('=')
                    var = var.strip()
                    value = value.strip()
                    ember_class.__setattr__(var, eval(value, {}, self.variables))
            else:
                break

        return j

if __name__ == "__main__":
    ember_code = """
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
    """
    interpreter = EmberInterpreter()
    interpreter.run(ember_code)
