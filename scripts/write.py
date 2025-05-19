from browser import document as doc, console # type: ignore
import re

textarea = doc['container_textarea']
text_num_div = doc['textarea_num_div']

def work_with_textarea(function):
        
    def scroll_num(event ):
        text_num_div.scrollTop = textarea.scrollTop

        textarea.bind('scroll', scroll_num)
        #update_line_num()  
    
    def insert_tab(event):
        if event.keyCode == 9:  # TAB key
            event.preventDefault()  # sustabdo naršyklės numatytą elgseną (fokusą)
            
            cursor_start = textarea.selectionStart
            cursor_end = textarea.selectionEnd
            
            value = textarea.value
            # Prideda "\t" (galima keisti į '    ' jei nori 4 tarpų vietoj TAB simbolio)
            new_value = value[:cursor_start] + "    " + value[cursor_end:]
            
            textarea.value = new_value
            # Perkelia kursorių po TAB simboliu
            textarea.selectionStart = textarea.selectionEnd = cursor_start + 1

            textarea.focus()
    # Pririšam keydown įvykį
    textarea.bind("keydown", insert_tab)
    
    def on_paste(event):
        event.preventDefault()  # Sulaikome naršyklės įklijavimo elgseną

        pasted_text = event.clipboardData.getData("text")
        replaced_text = pasted_text #replace_math_symbols(pasted_text)

        cursor_start = textarea.selectionStart
        cursor_end = textarea.selectionEnd

        current_value = textarea.value
        new_value = current_value[:cursor_start] + replaced_text + current_value[cursor_end:]

        textarea.value = new_value

        # Kursorių perstumiame po įklijuoto simbolio
        textarea.selectionStart = textarea.selectionEnd = cursor_start + len(replaced_text)

        textarea.focus()

        function.original_text = new_value
        function.update_self()
        text_num_div.html = '<br>'.join(function.line_num)
    textarea.bind("paste", on_paste)
        

    def on_input(event):
        # Save the cursor position
        cursor_pos = textarea.selectionStart - 1

        # Get the current content of the textarea
        current_text = textarea.value

        # Do the replacements
        replaced_content = (
            current_text
            .replace("&amp;", "&")
        )

        tex_len = f"Text length: {len(current_text)}"
        doc["text_length"].text = tex_len

        # Set the replaced text but do it only if it changed (optional optimization)
        if textarea.value != replaced_content:
            textarea.value = replaced_content

            # Restore the cursor position
            textarea.selectionStart = textarea.selectionEnd = cursor_pos

        function.original_text = replaced_content
        function.update_self()
        text_num_div.html = '<br>'.join(function.line_num)
    def replace_math_symbols(simbol):
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
        for sym, repl in replacements.items():
            simbol = simbol.replace(sym, repl)
        return simbol
    
    def input_symbol(event):
        """
                Inserts the symbol associated with the clicked button into the textarea at the user's current cursor position.

                Parameters:
                        event (Event): The event object triggered by the button click.
        """
        if not textarea.disabled:
                        # Get the button that triggered the event
            button = event.target
            replaced_simbol = button.text

            current_text = textarea.value#gauna egzisuojenti teksta is textarea
                        
            cursor_pos = textarea.selectionStart 
                        # gauna esama teksta ideda simboli esamoje vietoje ir taip sukuria nauja teksta ir ji sugrazina atgal
            new_text = current_text[:cursor_pos] + replaced_simbol + current_text[cursor_pos:]
            textarea.value = new_text
                        
            function.original_text = new_text
                        
                        # Move the cursor to just after the inserted symbol
            textarea.selectionStart = textarea.selectionEnd = cursor_pos + len(replaced_simbol)
            textarea.focus()
            function.update_self()
            text_num_div.html ='<br>'.join(function.line_num) 
                        
                        
        # Bind the input event to the textarea
    textarea.bind("input", on_input)
        #doc['edit'].bind('click',highlight_line_num())
        
                
    doc["symbol_+"].bind("click",input_symbol)
    doc["symbol_="].bind("click",input_symbol)
    doc["symbol_↔"].bind("click",input_symbol)
    doc["symbol_⊢"].bind("click",input_symbol)
    doc["symbol_→"].bind("click",input_symbol)
    doc["symbol_¬"].bind("click",input_symbol)
    doc["symbol_⊥"].bind("click",input_symbol)
    doc["symbol_∧"].bind("click",input_symbol)
    doc["symbol_∨"].bind("click",input_symbol)
    doc["symbol_∀"].bind("click",input_symbol)
    doc["symbol_∃"].bind("click",input_symbol)
    doc["symbol_⊆"].bind("click",input_symbol)
    doc["symbol_⊂"].bind("click",input_symbol)
    doc["symbol_∪"].bind("click",input_symbol)
    doc["symbol_∩"].bind("click",input_symbol)
    doc["symbol_∈"].bind("click",input_symbol)
    doc["symbol_∉"].bind("click",input_symbol)
    doc["symbol_&"].bind("click",input_symbol)
    doc["symbol_ℝ"].bind("click",input_symbol)
    doc["symbol_≠"].bind("click",input_symbol)
       
def sync_scroll(ev):
    num_div = doc["textarea_num_div"]
    textarea = doc["container_textarea"]
    num_div.scrollTop = textarea.scrollTop

doc["container_textarea"].bind("scroll", sync_scroll)
