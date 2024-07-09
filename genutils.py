import argparse

def parse_command_line_params(required_params, optional_params):
    parser = argparse.ArgumentParser()
    for param in required_params:
        parser.add_argument(param)
    for param, default in optional_params.items():
        parser.add_argument(param, nargs='?', default=default)
    args = parser.parse_args()
    
    parsed_params = {}
    for param in required_params:
        parsed_params[param] = getattr(args, param)
    for param, default in optional_params.items():
        parsed_params[param] = getattr(args, param, default)

    return parsed_params

def append_file_contents(source_file, target_file):
    with open(source_file, 'r') as src:
        contents = src.read()
    with open(target_file, 'a') as tgt:
        tgt.write(contents)

# Example usage:
if __name__ == '__main__':
    required_params = ['arg1']
    optional_params = {'--optional1': 'default_value1', '--optional2': 'default_value2'}
    
    parsed_params = parse_command_line_params(required_params, optional_params)
    if parsed_params:
        script_path = parsed_params['arg1']
        try:
            with open(script_path, 'r') as file:
                script_content = file.read()
            exec(script_content)
            print(f"Executed script in {script_path}")
        except Exception as e:
            print(f"Failed to execute script in {script_path}: {e}")
    else:
        print("Invalid command-line arguments. Usage: python genutils.py <arg1> [--optional1 <value>] [--optional2 <value>]")