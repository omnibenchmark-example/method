import argparse
import os


def concatenate_input_content(input_files):
    content = ""
    for input_file in input_files:
        with open(input_file, 'r') as file:
            content += file.read() + '\n'
    return content


def main():
    parser = argparse.ArgumentParser(description='Run method on files.')
    parser.add_argument('--output_dir', type=str, help='output directory where method will store results.')
    parser.add_argument('--name', type=str, help='name of the module')
    # api >= 0.8.0: the exact path to write, as `--output methods.mapping=PATH`.
    parser.add_argument('--output', action='append', default=[], help='id=PATH of an output to write')
    parser.add_argument('--process.filtered', type=str, help='optional input file #1.', required=False)
    parser.add_argument('--data.counts', type=str, help='optional input file #1.', required=False)
    parser.add_argument('--data.meta', type=str, help='input file #2.')
    parser.add_argument('--data.data_specific_params', type=str, help='input file #3.', required=False)

    # Anything else on the command line is a method parameter.
    args, parameters = parser.parse_known_args()

    counts = getattr(args, 'process.filtered') or getattr(args, 'data.counts')
    assert counts is not None, "one of --process.filtered or --data.counts is required"
    inputs = [counts, getattr(args, 'data.meta'), getattr(args, 'data.data_specific_params')]
    input_files = [f for f in inputs if f]

    outputs = dict(o.split("=", 1) for o in args.output)
    mapping_file = outputs.get('methods.mapping') or os.path.join(
        args.output_dir, f'{args.name}.model.out.gz'
    )

    content = concatenate_input_content(input_files)
    content += f"\n3. Running method using parameters '{parameters}' into {mapping_file}"

    os.makedirs(os.path.dirname(mapping_file) or ".", exist_ok=True)
    with open(mapping_file, 'w') as file:
        file.write(content)


if __name__ == "__main__":
    main()
