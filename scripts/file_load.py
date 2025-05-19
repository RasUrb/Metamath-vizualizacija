from io import text_encoding
from browser import document as doc, console,  window, alert # type: ignore
import re
textarea = doc['container_textarea']

def replace_math_symbols(text):
    replacements = {
            '/=': '≠',
            '|-': '⊢',
            '<->': '↔',
            '->': '→',
            '-.': '¬',
            '_|_': '⊥',
            '/\\': '∧',
            '\\/': '∨',
            'A.': '∀',
            'E.': '∃',
            'RR': 'ℝ',
            'C=': '⊆',
            'C.': '⊂',
            'u.': '∪',
            'i.': '∩',
            'e.': '∈',
            '-e.': '∉'
        }
    # replacements = {
    #     '&amp;': '&',
    #     '≠': '/=',
    #     '⊢': '|-',
    #     '↔': '<->',
    #     '→': '->',
    #     '¬': ' -.',
    #     '⊥': '_|_',
    #     '∧': '/\\',
    #     '∨': '\\/',
    #     '∀': 'A.',
    #     '∃': 'E.',
    #     'ℝ': 'RR',
    #     '⊆': 'C=',
    #     '⊂': 'C.',
    #     '∅': '0',
    #     '∪': 'u.',
    #     '∩': 'i.',
    #     '∈': 'e.',
    #     '∉': '-e.'
    # }

    #sort by len
    sorted_keys = sorted(replacements.keys(), key=len, reverse=True)

    # curate regex from simbols
    pattern = re.compile('|'.join(re.escape(k) for k in sorted_keys))

    return pattern.sub(lambda m: replacements[m.group(0)], text)

def file_read(event=None):  
    file = doc['fileMmInput'].files[0]  
    reader = window.FileReader.new()    
    def onload(event):
        content = event.target.result
        replaced_content = replace_math_symbols(content)
        textarea.value = replaced_content
        console.log("Pakeistas tekstas:", replaced_content)

    reader.bind('load', onload)
    reader.readAsText(file)


def show_popup(event):
    call_text = '''call_text = '''
Press "Edit" to modify the file. After making changes, the diagram will automatically update.

The diagram visualizes everything between "$=" and "$." — this is the formal proof content.

Metamath directives and syntax:

- $c (constant): declares constant symbols such as operators or keywords.
  Syntax:           $c symbol1 symbol2 ... $. 

- $v (variable): declares metavariables used in expressions.
  Syntax:           $v var1 var2 ... $. 

- $f (floating hypothesis): links a variable with a syntactic type (like term or wff).
  Syntax:           label $f type variable $. 
  Example:          tt $f term t $.

- $e (essential hypothesis): states assumptions needed to apply an axiom or proof.
  Syntax:           label $e |- statement $. 
  Example:          h1 $e |- t = r $.

- $a (axiom): introduces axioms or definitions without proof.
  Syntax:           label $a |- statement $. 
  Example:          a1 $a |- ( t = r -> ( r = s -> t = s ) ) $.

- $p (proof): defines a theorem with its proof steps.
  Syntax:           label $p |- statement $= proof-steps $. 
  Example:          th1 $p |- t = t $= tt tt weq a1 mp $.

Navigation:
- Use W/A/S/D or arrow keys to move the diagram.
- Press R to reset the view to its original position.

Extras:
- "With comment" checkbox enables display of proof comments.
- "Rectangle resizing" allows custom diagram sizing via `rect_height` and `rect_width`.
Then press "Submit" to apply your changes.
'''

    '''
    alert(call_text)
    
how_move = """To move graph push a,w,s,d or arrow. Push r to move back to original place."""



doc['Info'].bind('click', show_popup)




