"""
LaTeX Align Generator for Proofs (and simple math equations)
Cynthia Wang 2023
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Features:
    - Generates align* environments from strings and dictionary
        - Update: Loads strings from .txt files and dictionaries from .json
        - Start lines with ` to comment it out
    - Automatically numbers right column
    - Cross-referencing: When right column inserts a number in this format:
        "{i-<n>}"   Example: "We are referencing step {i-1}, the previous step"
      the parser inserts the appropriate number in this format
        "(<number>) "Example: "3. We are referencing step (2), the previous step"
      Note that this only works for past steps as it is unreasonable to reference future steps
    - Change all $\\LaTeX$ expressions into \\LaTeX\\text{ expressions}
To implement:
    - Load from generated LaTeX string (for sometimes you change something in LaTeX and want to feed it back)
    - Command-Line Interface
Known bugs:
    - Spaces sometimes fail to be detected
        - kind of fixed by workaround in `swap_latex_text()`
    - Single-character latex segments at the end of string cause `Match.start(0)` and `Match.end(0)` to behave funny
        - Also fixed by workaround
    - Sometimes texts at the end of a string is omitted for some reason
        - Not fixed (yet)
"""
import os
import json
import regex as re
import pyperclip
import argparse
from colorama import Fore, Style

class CutableString(str):
    def cut(self, marker: str, to: int):
        s_segments = self.split(marker)
        if len(s_segments) == 1:  # No marker found
            raise ValueError('Substring not found')
        if to == 0:
            return s_segments[0]
        cut_s = marker.join(s_segments[1:])
        if to == -1:
            return CutableString(cut_s)
        else:
            return CutableString(cut_s[:to-len(s_segments[0])])

    def before(self, marker):
        return self.cut(marker, 0)

    def after(self, marker):
        return self.cut(marker, -1)
    
    def after_nth(self, marker, n):
        s = self
        for i in range(n):
            s = s.cut(marker, -1)
        return s
    
    def before_and_after(self, marker):
        s_segments = self.split(marker)
        return CutableString(s_segments[0]), CutableString(marker.join(s_segments[1:]))

DEFAULT_OUTPUT_DIR = './output_files/'

def main(default_out_file='./output_files/result.txt'):
    arg_parser = argparse.ArgumentParser(
        prog="latex_align_generator.py",
        description="LaTeX align environment generator for two-column proofs. Made in 2023 by Cynthia.",
        epilog="See latex_align_generator.py for more info"
    )
    arg_parser.add_argument('--no-json',
        help='Do not generate an intermediate JSON file in the output folder. By default, JSON is generated only when input file is a .txt file.',
        action='store_true'
    )
    arg_parser.add_argument('--force-json',
        help='Always generate an intermediate JSON file, even when the input file is already in JSON.',
        action='store_true'
    )
    arg_parser.add_argument('--output-dir',
        help=f'The output directory. If out-file is not specified, an output file will be automatically created in this directory. Default is {DEFAULT_OUTPUT_DIR}',
        default=DEFAULT_OUTPUT_DIR,
        metavar='DIR'
    )
    arg_parser.add_argument('in_file',
        help=f'Input file to be converted. See latex_align_generator.py for syntax specification.'
    )
    arg_parser.add_argument('out_file',
        help=f'Output file to write generated align environment to. Generated text will also be automatically copied to clipboard. By default, an output file with the same name as the input file is generated in output directory.',
        default=default_out_file,
        nargs='?'
    )

    args = arg_parser.parse_args()
    output_dir = args.output_dir
    in_file = args.in_file
    out_file = args.out_file if args.out_file else os.path.join(output_dir, os.path.basename(in_file))

    load_file(in_file, out_file, args.force_json, args.no_json)

def load_file(input_path: str, output_path: str=None, force_save_json=False, force_no_json=False):
    raw_file_content = None
    input_file_name, input_file_ext = os.path.splitext(os.path.basename(input_path))
    assert input_file_ext in ('.json', '.txt'), "Only txt and json files are supported."

    if output_path is None:
        output_path = os.path.join(DEFAULT_OUTPUT_DIR, input_file_name+'.txt')
    if not os.path.exists(os.path.dirname(output_path)):
        os.mkdir(os.path.dirname(output_path))

    with open(input_path) as in_f:
        raw_file_lines = []
        for line in in_f.readlines():
            if line:
                if not line.startswith('`'):  # Comments
                    raw_file_lines.append(line.strip())
        raw_file_content = '\n'.join(raw_file_lines)

    generated_align, parsed_source = generate_proof_align(raw_file_content) if input_path.endswith('.txt') else generate_proof_align(json.loads(raw_file_content))
    pyperclip.copy(generated_align)

    with open(output_path, 'w') as out_f:
        out_f.write(generated_align)
        print('Your align* environment has been generated and copied to clipobard. It is also written into', output_path)
    
    if not force_no_json:
        if force_save_json or input_file_ext == '.txt':
            json_path = os.path.splitext(output_path)[0] + '.json'
            with open(json_path, 'w') as out_json:
                json.dump(parsed_source, out_json, indent=4)
                print('The parsed file is saved in JSON format to', json_path)

def generate_proof_align(src):
    if isinstance(src, str):  # Load string into structured dictionary
        # Parse string
        parsed_src = {}
        for line in src.split("\n"):
            if line:
                line = CutableString(line)
                parsed_src[line.before('; ')] = line.after('; ')
    elif isinstance(src, dict):
        parsed_src = src    
    else:
        raise TypeError(f"Unrecognized data type: {type(src)}")

    aligned_str = "\\begin{align*}\n"
    for i, (left, right) in enumerate(parsed_src.items()):
        i = i+1
        right = f'{i}. {right}'
        left, right = CutableString(left), CutableString(right)
        right = format_cross_references(right, i)
        left, right = swap_latex_text(left), swap_latex_text(right)
        aligned_str += f'\t& {left} && {right} \\\\\n'
    aligned_str += "\\end{align*}"

    return aligned_str, parsed_src

def format_cross_references(s, current_enum):
    while "{i-" in s:
            # Parse cross-references
            s_pieces = s.before_and_after('{i-')
            offset, remaining = s_pieces[1].before_and_after('}')
            offset = int(offset)
            s = CutableString(f"{s_pieces[0]}({current_enum-offset}){remaining}")
    return s

def swap_latex_text(s: CutableString):
    if '$' not in s:
        return CutableString('\\text{'+s+'}')
    LATEX_PATTERN = "\\$[^\\$]*\\$"
    # First, split s into latex and non-latex segments
    s_segments = []
    for match in re.finditer(LATEX_PATTERN, s):
        latex_part = match.group(0)
        before_this_latex = s[:match.start(0)]
        if before_this_latex:  # Something before latex
            if '$' in before_this_latex:  # Strange bug where single-character latex like $k$ are still included in strings
                s_segments.append(CutableString(before_this_latex).before('$'))
            else:
                s_segments.append(before_this_latex)
        s_segments.append(latex_part)
        s = s[match.end(0)+1:]  # Remove parsed part
    if s: s_segments.append(s)  # Add remaining string

    swapped_segments = []
    for i, segment in enumerate(s_segments):
        if segment.startswith('$'):
            inner_text = segment[1:-1]
            swapped_segments.append(inner_text)
        else:
            space_before = ' ' if i != 0 else ''
            space_after = ' ' if i != len(s_segments) else ''
            # Brute solution for missing space problem in non-latex segments
            # Prevent extra spaces at the start and end of a line
            swapped_segments.append("\\text{"+space_before+segment+space_after+"}")
    return CutableString(''.join(swapped_segments))
        
if __name__ == "__main__":
    # load_file('./input_files/in.txt', './output_files/result.txt')
    main()