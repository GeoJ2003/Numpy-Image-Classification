import argparse
import importlib
import numpy as np

def parse_command_line_params():
    parser = argparse.ArgumentParser(description='Execute a function from a given script with optional arguments.')
    # Required
    parser.add_argument('script', help='The script containing the function to execute.')
    parser.add_argument('function_name', help='The name of the function to execute.')
    parser.add_argument('func_args', nargs='*', help='The arguments to pass to the function.')
    # Optional
    parser.add_argument('--pipe', help='Function to pipe the result to.', default=None)
    args = parser.parse_args()

    return args.script, args.function_name, args.func_args, args.pipe

if __name__ == '__main__':
    script, function_name, func_args, pipe_function_name = parse_command_line_params()
    
    try:
        module_name = script.replace('.py', '')
        module = importlib.import_module(module_name)
        function_to_call = getattr(module, function_name)
        
        # Convert arguments to int if possible
        converted_args = []
        for arg in func_args:
            try:
                converted_args.append(int(arg))
            except ValueError:
                converted_args.append(arg)
        
        result = function_to_call(*converted_args)

        np.set_printoptions(threshold=np.inf)
        
        if pipe_function_name:
            # Assuming the pipe function is in the same module for simplicity
            pipe_function = getattr(module, pipe_function_name)
            piped_result = pipe_function(result)
            print(f"Piped function {pipe_function_name} executed with result: {piped_result}")
        else:
            print(f"Function {function_name} executed with result: {result}")
    except Exception as e:
        print(f"Failed to execute function {function_name} in {script}: {e}")