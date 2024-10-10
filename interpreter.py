import re


class EmberClass:
    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __getattr__(self, name):
        return self.__dict__[name]


class EmberInterpreter:
    def __init__(self):
        self.variables = {}
        self.classes = {}
        self.printed_conditions = set()

    def _handle_print(self, line):
        message = line[len('print '):].strip()

        if message.startswith('"') and message.endswith('"'):
            print(message.strip('"'))
        elif '.' in message:
            parts = message.split('.')
            if len(parts) == 2:  
                class_name, attr_name = parts
                if class_name in self.classes and hasattr(self.classes[class_name], attr_name):
                    print(getattr(self.classes[class_name], attr_name))
                else:
                    print(f"Error: Class '{class_name}' or attribute '{attr_name}' not found")
            else:  
                self._handle_expression(message)
        else:  
            self._handle_expression(message)

    def _handle_expression(self, message):
        try:
            result = eval(message, {}, self.variables | self.classes)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"An error occurred while executing Python code: {str(e)}")
            
    def _handle_repeat(self, line, lines, i):
        repeat_count = int(line.split(' ')[1])
        indent_level = line.count('    ')
        start_i = i + 1

        for _ in range(repeat_count):  # Repeat loop body 'repeat_count' times
            for j in range(start_i, len(lines)):
                if lines[j].startswith(' ' * (indent_level + 4)):
                    body_line = lines[j].strip()
                    if body_line.startswith('print '):
                        self._handle_print(body_line)
                else:
                    break

        return start_i + 1  # Return the index after the repeat loop

    def _handle_conditions(self, line, lines, i):
        condition = line[3:].strip()
        if condition in self.printed_conditions:
            return i + 1

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

        if result:
            self.printed_conditions.add(condition)
            if 'is' in condition:
                print(f"{var.strip()} is {value.strip().rstrip(':')}")
            elif 'between' in condition:
                print(f"{var.strip()} is between {low} and {high}")

        return i + 1


    def _handle_class(self, line, lines, i):
        class_name = line[len('class '):].strip()

        ember_class = EmberClass()
        self.classes[class_name] = ember_class

        print(f"Inside {class_name}, attributes initialized.")

        indent_level = line.count('    ')
        start_i = i + 1

        for j in range(start_i, len(lines)):
            if lines[j].startswith(' ' * (indent_level + 4)):
                body_line = lines[j].strip()
                if '=' in body_line:
                    var, value = body_line.split('=')
                    var = var.strip()
                    value = value.strip()
                    ember_class.__setattr__(var, eval(value, {}, self.variables))
                    print(f"{var} is set to {ember_class.__getattr__(var)}")
                elif body_line.startswith('print '):
                    message = body_line[6:].strip()
                    if '"' in message:
                        print(message.strip('"'))
                    else:
                        var = message
                        if hasattr(ember_class, var):
                            print(ember_class.__getattr__(var))
            else:
                break

        return j

    def _handle_file_ops(self, line):
        parts = line.split(', ')
        
        if len(parts) == 2:  # read_file operation
            operation, filename = parts
            filename = filename.strip('"')
            
            if operation == 'read_file':
                try:
                    with open(filename, 'r') as f:
                        print(f.read())
                except FileNotFoundError:
                    print(f"Error: File {filename} not found")
                    
        elif len(parts) == 2 and parts[0].startswith('write_file'):  # write_file operation
            operation, rest = parts
            filename, content = rest.split('"')
            filename = filename.replace('write_file ', '').strip()
            content = content.strip('"')
            
            with open(filename, 'w') as f:
                f.write(content)

    def run(self, code):
        lines = code.split('\n')
        in_python_block = False
        python_code = ""
        attempt_block = False
        python_code_attempt = ''

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
                python_code_attempt = ''

            elif 'on_error' in line:
                attempt_block = False
                if python_code_attempt:
                    try:
                        exec(python_code_attempt, {}, self.variables | self.classes)
                    except Exception as e:
                        print(f"An error occurred while executing Python code: {str(e)}")
                python_code_attempt = ''

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
                python_code_attempt += line[7:] + '\n'

            elif line.startswith('read_file') or line.startswith('write_file'):
                self._handle_file_ops(line)

            else:
                if in_python_block:
                    python_code += line + "\n"
                else:
                    if '=' in line:
                        var, value = line.split('=')
                        var = var.strip()
                        value = value.strip()
                        self.variables[var] = eval(value, {}, self.variables)

            i += 1


    def _handle_python(self, code):
        try:
            exec(code, {}, self.variables | self.classes)
        except Exception as e:
            print(f"Error executing Python code: {str(e)}")


def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python ember.py <script.em>")
        return

    with open(sys.argv[1], 'r') as f:
        code = f.read()

    interpreter = EmberInterpreter()
    interpreter.run(code)


if __name__ == "__main__":
    main()
