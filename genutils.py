import argparse
import importlib
import sys

# Examples (Move this comment to a more suitable location):
# Regular Example:
# python genutils.py <module> <function> <args*>
# python genutils.py imageutils.py load_image_and_resize imgs/dogs/Dog1.png 100 100
# Pipe Example:
# python genutils.py <module> <function> <args*> --pipe <module> <function>
# python genutils.py imageutils.py load_images imgs/dogs --pipe classification.py find_image_cosine_similarities

def parse_command_line_params():
    parser = argparse.ArgumentParser(description='Execute a function from a given script with optional arguments.')
    # Required
    parser.add_argument('script', help='The script containing the function to execute.')
    parser.add_argument('function_name', help='The name of the function to execute.')
    parser.add_argument('func_args', nargs='*', help='The arguments to pass to the function.')
    # Optional for piping
    parser.add_argument('--pipe', nargs=2, help='Module and function to pipe the result to.', default=None)
    args = parser.parse_args()

    # Splitting pipe into script and function if provided
    pipe_script = None
    pipe_function_name = None
    if args.pipe:
        pipe_script, pipe_function_name = args.pipe

    return args.script, args.function_name, args.func_args, pipe_script, pipe_function_name

def convert_args(func_args):
    converted_args = []
    for arg in func_args:
        try:
            converted_args.append(int(arg))
        except ValueError:
            converted_args.append(arg)
    return converted_args

if __name__ == '__main__':
    script, function_name, func_args, pipe_script, pipe_function_name = parse_command_line_params()
    
    try:
        module_name = script.replace('.py', '')
        module = importlib.import_module(module_name)
        function_to_call = getattr(module, function_name)
        
        converted_args = convert_args(func_args)
        result = function_to_call(*converted_args)

        if pipe_function_name:
            # Import the module for the piped function
            pipe_module_name = pipe_script.replace('.py', '') if pipe_script else module_name
            pipe_module = importlib.import_module(pipe_module_name)
            pipe_function = getattr(pipe_module, pipe_function_name)
            
            # Execute the piped function
            piped_result = pipe_function(result)
            print(f"Piped function {pipe_function_name} executed with result:\n{piped_result}")
        else:
            print(f"Function {function_name} executed with result:\n{result}")
    except Exception as e:
        print(f"Failed to execute function {function_name} in {script}: {e}", file=sys.stderr)