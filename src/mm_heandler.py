from browser import document as doc, console,  window, alert
from mmverify_on_htlm import start_checker
def file_read(event):

    def onload(event):
        file_content = event.target.result
        # Perform replacements in the loaded file content
        replaced_content = (
            file_content
            .replace("&amp;", "&")
            .replace("<->", "↔")
            .replace("|-", "⊢")
            .replace("-.", "¬")
            .replace("->", "→")
        )

        # Display the modified content
        doc['file_mm_content'].innerHTML = replaced_content
        
        start_checker()

    # Get the selected file as a DOM File object
    file = doc['file_mm_input'].files[0]
    # Create a new DOM FileReader instance
    reader = window.FileReader.new()
    reader.readAsText(file)
    reader.bind("load", onload)

doc["file_mm_input"].bind("input", file_read)

def show_popup(event):
    call_text = '''Chose file and then press "run". 
    Other side will draw file if it has "$=" and "$.". 
    If file has a problem it will be commented else it just say true.
    To move graph push a,w,s,d. Push r to move back to original place.
    
    $c - constant symbols statements
    $v - variable symbols statements
    $p - theorems (and derived rules of inference)statements are written.
    
    '''
    alert(call_text)

doc['Info'].bind('click', show_popup)