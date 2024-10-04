from browser import document as doc, console
import re

textarea = doc['function_write']

def darbas_su_textarea(funkcija):
        def on_input(event):
                # Get the current content of the textarea
                current_text = textarea.value
                # Display the text length in a paragraph
                replaced_content = (
                current_text
                .replace("&amp;", "&")
                .replace("<->", "↔")
                .replace("|-", "⊢")
                .replace("-.", "¬")
                .replace("->", "→")
                )
                text = f"Text length: {len(current_text)}"
                doc["textInfo"].text = text
                #print(text)
                print(replaced_content)
                textarea.value = replaced_content
                
                #funkcija.original_text = replaced_content
                
        def input_symbol(event):
                if not textarea.disabled:
                        button = event.target
                        #print(button)
                        current_text = textarea.value
                        cursor_pos = textarea.selectionStart
                        new_text = current_text[:cursor_pos] + button.text + current_text[cursor_pos:]
                        textarea.value = new_text
                        
                        # Atstatyti kursoriaus poziciją po įterpto simbolio
                        textarea.selectionStart = textarea.selectionEnd = cursor_pos + 1
                        textarea.focus()
                        
        # Bind the input event to the textarea
        textarea.bind("input", on_input)

        doc["symbol_↔"].bind("click",input_symbol)
        doc["symbol_⊢"].bind("click",input_symbol)
        doc["symbol_→"].bind("click",input_symbol)
        doc["symbol_¬"].bind("click",input_symbol)
        doc["symbol_="].bind("click",input_symbol)
        doc["symbol_^"].bind("click",input_symbol)
        doc["symbol_&"].bind("click",input_symbol)

