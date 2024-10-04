
import re
#import time
        #get all text between markers
        
Stmttype = [ "$f", "$e", "$a"]
offset_x, offset_y = 0, 0  # Variables to store the mouse offset relative to the element

class Funkcija:  
        def __init__(self, original_text = str):
                #self.mm_text = mm_text
                self.original_text = original_text
                self.modify_text = None
                #self.comments = None
                self.proofs = None
                self.proof_name = None
        
        def __str__(self) -> str:
                return f"proof_names:{self.proof_name}, and proofs:{self.proofs}"

        def get_between_markers(self, start_marker = str, end_marker = str):
                pattern = re.compile(fr'{re.escape(start_marker)}(.*?){re.escape(end_marker)}')
                return pattern.findall(self.modify_text) #matches 
        
        #get all text between markers and even if there are \n
        def get_between_markers_and_enter(self, start_marker = str, end_marker = str):
                pattern = re.compile(re.escape(start_marker) + r'\s*(.*?)\s*'+re.escape(end_marker), re.DOTALL)
                matches = pattern.findall(self.modify_text)

                return matches

        #isvalo komentarus
        def clear_comments(self):
                pattern = re.compile(r'\$\([^$]+\$\)', re.DOTALL)
                self.modify_text = re.sub(pattern, '', self.original_text).strip()
                #self.comments = self.original_text
        
        #Gauna teksta ir istrina , tarpus, '\n'is teksto. Grazina array
        def valyti_enter(self, text):  
                for index, key in enumerate(text):   
                        text[index] = re.split(r'[ ,;\n]+', key)
                        
                return text
        
        #Gauna text. Is teksto isrenka funkcijos irodymus ir vardus. 
        # Grazina dictionary of funkcijos varda ir irodyma.  
        def funkcijos_irodymas(self):
                self.proof_name = self.get_between_markers_and_enter("$p", "$=")
                irodymas = self.get_between_markers_and_enter("$=", "$.")

                self.proofs = self.valyti_enter(irodymas)
        
        def surasti_ir_pakeisti(self, stm, name, change):
                for i, proof in enumerate(self.proofs):
                        for j, func in  enumerate(proof):
                                if name.strip() == func.strip():
                                        self.proofs[i][j] = f"{stm }  {change}" 
        
        # is teksto isrenka funkcijas su ju pavadinimu. Gautas funkciju pavadinimas suligina su proof esamais pavadinimais ir juos pakeicia funkcija
        # Sugrazina proof. Kuris turi parsyta irodyma
        def testinis(self):
                self.clear_comments()
                self.funkcijos_irodymas()

                
                if self.proof_name:

                        for stm in Stmttype:
                                getsName = self.get_between_markers("\n",stm)
                                elemtStr =  self.get_between_markers_and_enter(stm, "$.")

                                for i, name in enumerate(getsName):
                                        self.surasti_ir_pakeisti(stm, name, elemtStr[i])
                                        # for k, proof in enumerate(self.proofs):

                                        #         for j,func in enumerate(proof):
                                        #                 if name.strip() == func.strip():
                                        #                         self.proofs[k][j] = f"{stm }  {elemtStr[i]}" 


