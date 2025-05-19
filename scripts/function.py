# This Python class processes text data by extracting proofs and modifying them based on specific
# criteria, while also handling errors and highlighting them in the text.
import re
from mmverify_on_html import process_metamath_texts
import copy


Stmttype = ["$c", "$v", "$f", "$e", "$a", "$d"] #["$f", "$e", "$a", "$d", "$p"]
#offset_x, offset_y = 0, 0  # Variables to store the mouse offset relative to the element
'''    "f": "#c0c4ff",  # function
    "e": "#ffff80",  # example
    "a": "#d700d7",  # axiom
    "p": "#66ff8c",  # proof'''

class Function:
    def __init__(self, original_text=str):
        # self.mm_text = mm_text
        self.original_text = original_text
        self.modify_text_array = []
        
        self.no_error = None
        self.proof_name = []
        self.proofs_raw = []
        self.proofs_raw_and_comment = []
        self.proof_step_by_step = []
        self.proof_main_only = []
        self.line_count = 0
        self.line_num = []
        self.error_collector = None  # MMErrorCollector()

        self.verify_mm(self.original_text)

    def __str__(self) -> str:
        return f"proof_names:{self.proof_name}, and row proofs:{self.proofs_raw}"
    def count_constant(self,show = False):
        pass
    def count_variables(self,show = False):
        pass
    def count_function(self,show = False):
        pass
    def count_example(self,show = False):
        pass
    def count_axiom(self,show = False):
        pass
    def count_proof(self,show = False):
        pass
    def count_proof(self,show = False):
        pass
    
    def get_between_markers(self, text, start_marker=str, end_marker=str):
        pattern = re.compile(rf"{re.escape(start_marker)}(.*?){re.escape(end_marker)}")
        return pattern.findall(text)  # matches

    # get all text between markers and even if there are \n
    def get_between_markers_and_enter(self, text, start_marker=str, end_marker=str):
        pattern = re.compile(
            re.escape(start_marker) + r"\s*(.*?)\s*" + re.escape(end_marker), re.DOTALL
        )
        matches = pattern.findall(text)

        return matches
    #clear comments from matrix= [[]]
    def remove_comments(self, matrix):
        result = []
        for row in matrix:
            cleaned_row = [token for token in row if not (token.startswith("$(") and token.endswith("$)"))]
            result.append(cleaned_row)
        return result
    # clear comments from text
    def clear_comments(self, text = None):

        pattern = re.compile(r"\$\([^$]+\$\)", re.DOTALL)
        texts = re.sub(pattern, "", self.original_text).strip()
        return texts

    # Clear enter Gauna teksta ir istrina , tarpus, '\n'is teksto. Grazina array
    def clear_enter(self, text):
        for index, key in enumerate(text):
            text[index] = re.split(r"[ ,;\n]+", key)
        return text

    # Gauna text. Is teksto isrenka funkcijos irodymus ir vardus.
    # Grazina dictionary of funkcijos varda ir irodyma.
    # curate all proof code name
    def curate_proofs_code_name(self, text):
        self.proofs_code_name = self.get_between_markers(
        text, "\n", "$p")
        ## print("curted code name", self.proofs_code_name)
        pass
    
    def extract_proof_elements_with_comment(self, text: str):
        #outer_pattern = re.compile(re.escape("$=") + r"\s*(.*?)\s*" + re.escape("$.") , re.DOTALL)
        matches = self.get_between_markers_and_enter(text, "$=", "$.")

        result = []
        token_pattern = re.compile(r"\$\([^$]*?\$\)|\S+")

        for match in matches:
            tokens = token_pattern.findall(match)
            result.append(tokens)

        return result
    
    def get_proofs_and_names(self, text = None):
        """
        This Python function extracts and returns proofs_raw and there names from a given text.
        """
        if text is None:
            text = self.original_text
        no_comments_texts = self.clear_comments()
        self.curate_proofs_code_name(no_comments_texts)

        self.proof_name = self.get_between_markers_and_enter(
            no_comments_texts, "$p", "$="
        )
        proofs = self.get_between_markers_and_enter(no_comments_texts, "$=", "$.")
        print("rew with comments",self.extract_proof_elements_with_comment(self.original_text))
        self.proofs_raw = self.extract_proof_elements_with_comment(self.original_text)#self.clear_enter(proofs)
        ## print(f"row_proofs: {self.proofs_raw}")
        return self.proof_name, self.proofs_raw

    def find_and_change(self, proofs, stm, name, change):
        proof_change = [list(proof) for proof in proofs] 
        name = name.strip()
        #get place and change proof arry
        for i, proof in enumerate(proof_change):
            #get place and functions
            for j, func in enumerate(proof):
                if name == func.strip():
                    # print(f"Match found at proofs[{i}][{j}]: replacing '{func.strip()}' with '{stm}  {change}'")
                    proof_change[i][j] = f"{stm }  {change}"
        return proof_change

    #Find if exect and add it there if need be change
    def find_add_and_change(self, proofs, stm, code_name, proof_name, change):
        code_name=code_name.strip()
        for i, proof in enumerate(proofs):
            # print(f"\n Tikrinamas proof[{i}]: {proof}")
            new_proof = []
            if code_name in proof:
                # print(f"Found '{code_name}' proof[{i}]")
                for j,token in enumerate(proof):
                    if token.strip()== code_name:
                        # print(f"  ↪ Change token[{j}] ('{token}')")
                        new_proof.extend([f"{stm} {proof_name}"] + change)
                    else:
                        new_proof.append(token)
                proofs[i] = new_proof 
        return proofs
        
    def create_proof_step_by_step(self, proofs):
        self.proof_step_by_step = copy.deepcopy(proofs)
        for i, code_name in enumerate(self.proofs_code_name):
            # print(code_name)
            self.proof_step_by_step =  self.find_add_and_change(self.proof_step_by_step,"$p",code_name, self.proof_name[i],self.proof_step_by_step[i])
        return self.proof_step_by_step
    #Irodymas kureme parodomi irodymas, be jo zingsniu
    def create_main_proof(self, proofs):
        self.proof_main_only = copy.deepcopy(proofs)
        ## print("cia",self.proof_main_only)
        for i, name in enumerate(self.proofs_code_name):
            self.proof_main_only = self.find_and_change(self.proof_main_only,"$p",name,self.proof_name[i])
        # print("main proof:", self.proof_main_only )

    """ selects functions from the text with their names. The resulting function names are compared with the existing names in proof and replaced by the function 
    # Returns proof. Which has a parsed proof"""
    def build_internal_proof_structure(self):
        
        no_comments_texts = self.clear_comments()
        self.proof_name, proofs = self.get_proofs_and_names()
        ## print(f"getsName: {self.proof_name}")
        if len(self.proof_name) == len(proofs):
            for stm in Stmttype:
                getsName = self.get_between_markers(no_comments_texts, "\n", stm)
                elemtStr = self.get_between_markers_and_enter(no_comments_texts, stm, "$.")

                if self.proof_name:
                    for i, name in enumerate(getsName):
                        proofs = self.find_and_change(proofs, stm, name, elemtStr[i])
            
        # print(f"end goten proofs: {proofs}")
        self.create_main_proof(proofs)
        ## print(f"end proofs: {proofs}")
        self.create_proof_step_by_step(proofs)
        
    def error_start(self, line_num):
        i = line_num
        num = 0
        while i >= 0:
            check = self.modify_text_array[i].count("$")

            if check > 0 and i != line_num:
                num = i
                break
            elif check >= 2 and check <= 3 and i == line_num:
                num = i
                break
            elif self.modify_text_array[i].count("$.") > 0 and i != line_num:
                num = i + 1
                break
            else:
                i -= 1

        return num

    def find_comment_and_highlight(self):
        pattern = re.compile(r"\$\([^$]+\$\)", re.DOTALL)

    def error_highlight(self, error_lines):
        if not error_lines or error_lines[0] > self.line_count:
            return
        if error_lines[0] <= self.line_count:
            
            for i,line in enumerate(error_lines):
                # idx = line - 1
                # start_idx = self.error_start(idx)

                # self.modify_text_array[start_idx] = (
                #     f'<span class="highlight">{self.modify_text_array[start_idx]}'
                # )

                # print(f"line {self.line_num[line-1]}, eror, place ", self.line_num[line-1])
                self.line_num[line-1] = (
                     f'<span class="highlight">{self.line_num[line-1]} </span>'
                )
                self.modify_text_array[line-1] = f'<span class="highlight"> {self.modify_text_array[line-1]}</span>'
            # print("line_num", self.line_num)

        #self.modify_text_array[idx] = f"{self.modify_text_array[idx]}</span>"
        #self.line_num[idx] = f"{self.line_num[idx]}</span>"
    
    
    def comment_highlight(self, text_array):
        """Fiend if comment"""
        in_comment_block = False
        highlighted = []

        for line in text_array:
            stripped = line.strip()
            
            if "$( " in stripped and not in_comment_block:
                in_comment_block = True
                line = line.replace("$( ", '<span class="highlight_comment">$(')
            
            if " $)" in stripped and in_comment_block:
                in_comment_block = False
                line = line.replace(" $)", '$)</span>')

            highlighted.append(line)
        return highlighted

    def modify_textarea(self, error_lines):
        self.modify_text_array = self.comment_highlight(self.modify_text_array)
        self.error_highlight(error_lines)

    def update_line_count(self):
        for i in self.line_count:
            line_num_str = (
                f"{i+1}<br>"  # [f"{i+1}<br>" for i in range(self.line_count)]
            )
        return line_num_str

    def update_self(self, texts=None):
        if texts is not None:
            self.original_text = texts
        self.modify_text_array = self.replace_to_math_symbols(self.original_text).split("\n")
        # ## print(self.modify_text_array)
        self.line_count = len(self.modify_text_array)
        self.line_num = [f"{i+1}" for i in range(self.line_count)]

    def replace_to_math_symbols(self, text):
        # replacements = {
        #     '/=': '≠',
        #     '|-': '⊢',
        #     '<->': '↔',
        #     '->': '→',
        #     '-.': '¬',
        #     '_|_': '⊥',
        #     '/\\': '∧',
        #     '\\/': '∨',
        #     'A.': '∀',
        #     'E.': '∃',
        #     'RR': 'ℝ',
        #     'C=': '⊆',
        #     'C.': '⊂',
        #     'u.': '∪',
        #     'i.': '∩',
        #     'e.': '∈',
        #     '-e.': '∉'
        # }
        replacements = {
            '≠': '/=',
            '⊢': '|-',
            '↔': '<->',
            '→': '->',
            '¬': ' -.',
            '⊥': '_|_',
            '∧': '/\\',
            '∨': '\\/',
            '∀': 'A.',
            '∃': 'E.',
            'ℝ': 'RR',    # Dažnai naudojamas simbolis realiems skaičiams
            '⊆': 'C=',
            '⊂': 'C.',
            '∪': 'u.',
            '∩': 'i.',
            '∈': 'e.',
            '∉': '-e.'
        }
        # Rūšiuojame pagal ilgį, kad ilgesni simboliai būtų keičiami pirmi
        sorted_keys = sorted(replacements.keys(), key=len, reverse=True)

        # Sukuriam regex iš simbolių
        pattern = re.compile('|'.join(re.escape(k) for k in sorted_keys))

        # Pakeičiam kiekvieną atitikmenį
        return pattern.sub(lambda m: replacements[m.group(0)], text)

    
    def verify_mm(self, texts=None):
        self.update_self(texts)
        text = self.replace_to_math_symbols(self.original_text)
        print(text)
        self.error_collector = process_metamath_texts(text.split("\n"))
        error_lines = self.error_collector.get_all_line_nums()
        self.modify_textarea(error_lines)
        self.original_text = self.original_text
        self.build_internal_proof_structure()
        
        
