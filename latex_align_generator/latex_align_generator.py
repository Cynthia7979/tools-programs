"""
LaTeX Align Generator for Proofs (and simple math equations)
Cynthia Wang 2023
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Features:
    - Generates align* environments from strings and dictionary
    - Automatically numbers right column
    - Cross-referencing: When right column inserts a number in this format:
        "@i-<n>@"   Example: "We are referencing step @i-1@, the previous step"
      the parser inserts the appropriate number in this format
        "(<number>)"Example: "3. We are referencing step (2), the previous step"
      Note that this only works for past steps as it is unreasonable to reference future steps
    - Change all $\\LaTeX$ expressions into \\LaTeX\\text{ expressions}
To implement:
    - Load from generated LaTeX string (for sometimes you change something in LaTeX and want to feed it back)
"""
import regex as re
import pyperclip

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
    
    def before_and_after(self, marker):
        s_segments = self.split(marker)
        return CutableString(s_segments[0]), CutableString(marker.join(s_segments[1:]))

# align_this = {
#     "$x+y$ is even": "Given"
# }

# align_this_string = """
# $x+y$ is even; Given
# $x+y=2k$ for some integer $k$; Definition of even integers
# $(x+y)(x-y) = 2k(x-y)$; Multiply both sides by $(x-y)$ in {i-1}
# $y(x+y)(x-y) = 2ky(x-y)$; Multiply both sides by $y$ in {i-1}
# $y(x^2-y^2) = 2ky(x-y)$; Difference of two squares law
# $y(x^2-y^2)+2 = 2ky(x-y)+2$; Add 2 to both sides in {i-1}
# $x^2y-y^2y+2 = 2ky(x-y+2)$; Distributive law of algebra
# $x^2y-y^3+2 = 2ky(x-y+2)$; Product of powers law of algebra
# $x^2y-y^3+2 = 2(ky(x-y)+1)$; Factor 2 from RHS of {i-1}
# $ky(x-y)+1 = m$ for some integer $m$; Closure of addition and multiplication under integers
# $x^2y-y^3+2 = 2m$; Substitution of {i-1} into {i-2}
# $x^2y-y^3+2$ is even; Definition of even
# """

align_this_string = """
$n$ is even; Given
$n = 2k$ for some integer k; Definition of even integers
$n^2 = (2k)^2$; Raise both sides in {i-1} to a power of 2
$n^2+2n = (2k)^2+4k$; Add 2 times both sides in {i-2} to {i-1}
$n^2+2n+10 = (2k)^2+4k+10$; Add 10 to both sides in {i-1}
$n^2+2n+10 = 4k^2+4k+10$; Use distributive law of exponents on RHS in {i-1}
$n^2+2n+10 = 2(2k^2+2k+5)$; Factor 2 from RHS of {i-1}
$2k^2+2k+5=m$ for some integer $m$; Closure of addition and multiplication under integers
$n^2+2n+10 = 2m$; Substitution of {i-1} into {i-2}
$n^2+2n+10$ is even; Definition of even integers
"""

def generate_proof_align(src):
    if isinstance(src, str):
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

    pyperclip.copy(aligned_str)
    return aligned_str

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
    print(generate_proof_align(align_this_string))