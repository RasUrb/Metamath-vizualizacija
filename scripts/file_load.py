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
    call_text = '''Chose file and then press "run". 
    push to edit file to edit the push to save changes and the diagram will be reupload
    Diagram will draw what is write on "$=" and "$.". 
    $c (constant) is used to declare constant symbols (e.g., operators or keywords).
    $v (variables) is used to declare variables.
    $f (function) is used for floating hypotheses, where a variable and its type are specified. 
    
    $e (example) for essential hypotheses, where an assumption or condition is defined that must be satisfied.
    $a (axiom) for axioms, where a logical axiom or theorem is introduced without proof.
    $p (proof) for proofs, where a theorem or conclusion is provided along with a proof.
    '''
    alert(call_text)
    
how_move = """To move graph push a,w,s,d or arrow. Push r to move back to original place."""



doc['Info'].bind('click', show_popup)




