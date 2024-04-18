import argparse
import os

def concatenate_input_content(input_files):
    concatenated_content = ""  # Initialize an empty string to hold the concatenated content
    
    # Iterate over each input file
    for input_file in input_files:
        # Open each input file in read mode and read its content
        with open(input_file, 'r') as file:
            # Read the content of the input file and append it to the concatenated_content string
            concatenated_content += file.read()
            # Optionally, you can add a newline between the content of each file
            concatenated_content += '\n'

    return concatenated_content


def run_method(output_dir, name, input_files, parameters):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    content = concatenate_input_content(input_files)

    method_mapping_file = os.path.join(output_dir, f'{name}.model.out.gz')
    content += f"\n3. Running method using parameters '{parameters}' into {method_mapping_file}"

    with open(method_mapping_file, 'w') as file:
        file.write(content)


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Run method on files.')

    # Add arguments
    parser.add_argument('--output_dir', type=str, help='output directory where method will store results.')
    parser.add_argument('--name', type=str, help='name of the dataset')
    parser.add_argument('--input_files', type=str, help='input files required by the method.')

    # Parse arguments
    args, extra_arguments = parser.parse_known_args()

    input_files = args.input_files.split(',')

    run_method(args.output_dir, args.name, input_files, extra_arguments)


if __name__ == "__main__":
    main()