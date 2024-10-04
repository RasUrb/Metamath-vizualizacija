from browser import document as doc, window
#import browser.html as html
#import browser.svg as svg
from mmverify_on_htlm import start_checker
#from mm_heandler import *

from funkcija import *
from write import *
from draw import *
from judejimas import *
from write import *



def file_read():
    file = doc['file_mm_input'].files[0]  # Get the selected file
    reader = window.FileReader.new()      # Create FileReader instance
    
    # Define onload function to process the file once loaded
    def onload(event):
        # Perform replacements and update content
        replaced_content = (
            event.target.result
            .replace("&amp;", "&")
            .replace("<->", "↔")
            .replace("|-", "⊢")
            .replace("-.", "¬")
            .replace("->", "→")
        )
        
        textarea.value = replaced_content
        #doc['file_mm_content'].innerHTML = replaced_content  # Update display
        func.original_text = replaced_content#get_new_text(replaced_content)

    reader.readAsText(file)
    reader.bind("load", onload)  # Bind the onload function




def reload(event):
    
    #clear_panel()    # Clear the panel
    graph_draw_function()
    
def read_Patikrina_And_Draw(event): 
    file_read()
    #print(func.original_text)
    # Add a timer to call start_checker() after 1 seconds (1000 ms)
    window.setTimeout(lambda: delayed_checker_and_continue(), 800)

def render_diagram(diagram):
    diagram.offset()
    diagram.clear_panel()
    diagram.draw_all()
    
    #bind_movement(diagram)

def graph_draw_function():
    if func.original_text:
        
        func.testinis()
        #print(func)
        
        if func.proofs:
            
            container = doc["buttons_of_proof"]
            
            container.clear()
            for i, proof in enumerate(func.proofs):
                button = doc.createElement("button")
                button.text = func.proof_name[i]
                diagram = ProofDiagram(panel)

                diagram.draw_graph(proof)  # Draw the graph with modified content
                diagram.clear_panel()
                button.bind("click", lambda event, diagram=diagram: render_diagram(diagram))
                container <= button
                #print(diagram)
            diagram.draw_all()
                
            bind_movement(diagram)
            

def delayed_checker_and_continue():
    start_checker(func.original_text)  # Call the checker function after delay
    #clear_panel()    # Clear the panel
    graph_draw_function()
    

def edit_button(event):
    textarea = doc['function_write']

    func.original_text = textarea.value
    
    if textarea.disabled :
        textarea.disabled  = False
        doc['edit'].text = "Save"
    else:
        textarea.disabled  = True
        doc['edit'].text = "Edit"
            
        start_checker(textarea.value)
        func.testinis()
        graph_draw_function()
    print(f'edit disable:{textarea.disabled }')
    
    
    
example ="""$( irodymas kad ⊢ ¬x → x $)
$c ¬ → ⊢ wff ( ) $. $( zenkldai $)
$v x $. $( simboliai $)
                                    
wx $f wff x $.
                                    
wxn $e ⊢ ( ¬ ¬ x → x ) $.
wxnn $e ⊢ ¬ x $.
wxnp $a ⊢ x $.
                                    
proof1 $p ⊢ x $= wx 
wxn wxnn
wxnp $.
proof2 $p x $= n 
d av
wxnp $."""
if __name__ == '__main__':
    doc['function_write'].disabled = True
    panel = doc['panel']
    doc['function_write'].value = example
    print(panel.viewBox)
    func = Funkcija(example)#doc.getElementById("file_mm_content").textContent)
    start_checker(func.original_text)
    darbas_su_textarea(func)
    doc["file_mm_input"].bind("input", read_Patikrina_And_Draw)

    doc['reload_function'].bind('click', reload)
    doc['edit'].bind('click',edit_button)

    graph_draw_function()

    
# textarea = doc['function_write']

# curront_text =textarea.value
# print(curront_text)


