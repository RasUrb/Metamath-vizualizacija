from browser import document as doc, window # type: ignore

from function import *
from write import *
from draw import *

from svg_viewbox_controller import *  
from file_load import *
from download_svg import *

diagrams = []

def switch_diagram(diagram):
    diagram.panel.clear()
    diagram.draw_all()
    bind_download_buttons(diagram)


def get_panel_height_and_width(svg_size =  doc['panel']):

    panel_height= svg_size.height
    panel_width = svg_size.width
    
    return panel_height, panel_width
def curate_diagram_main_steps( width = None, height = None):
    #if not doc["show_comment"].checked:
    #panel = doc['panel']
    panel_height, panel_width = get_panel_height_and_width()
    container = doc["buttons_of_proof"]
    container.clear()
    coment = doc["comment_mode"].checked
    print(not coment)
        #cheak if need comment
    if not coment:
        proof_main_only = func.remove_comments(func.proof_main_only)
    else:
        proof_main_only = func.proof_main_only
        
    if proof_main_only:
        

        diagrams = []

        for i, proof in enumerate(proof_main_only):
            button = doc.createElement("button")
            button.text = func.proof_name[i]

                    # Sukuriame diagramos objektą su tuo pačiu panel
            diagram = ProofDiagram(panel, panel_height, panel_width)
            diagram.draw_graph(proof, func.proof_name[i], width, height)
                    
                    # Iš pradžių nerodome (arba rodom tik pirmąją)
            if i != 0:
                diagram.clear_panel()

            # Saugojam diagramą (jei vėliau reikia)
            diagrams.append(diagram)

            # Pririšam mygtuką prie diagramos
            button.bind("click", lambda event, d=diagram: switch_diagram(d))

            container <= button

                # Pradžioje rodom pirmą diagramą (nebūtina jei jau parodyta)
        if diagrams:
            switch_diagram(diagrams[0])
            tex_len = f"Text length: {len(func.original_text)}"
            doc["text_length"].text = tex_len

def curate_diagram_step_by_step( width = None, height = None):
    #if doc["show_comment"].checked:
    container = doc["buttons_of_proof"]
    container.clear()
    panel = doc['panel']
    panel_height= panel.height
    panel_width = panel.width
    if func.proof_step_by_step:
        
        
        #get cheaker if need show comments
        coment = doc["comment_mode"].checked
        print(not coment)
        #cheak if need comment
        if not coment:
            step_by_step = func.remove_comments(func.proof_step_by_step)
        else:
            step_by_step =func.proof_step_by_step
        diagrams = [] 
        
        for i, proof in enumerate(step_by_step):
            button = doc.createElement("button")
            button.text = func.proof_name[i]

                    # Sukuriame diagramos objektą su tuo pačiu panel
            diagram = ProofDiagram(panel, panel_height, panel_width)
            diagram.draw_graph(proof, func.proof_name[i], width, height)
                    
                    # Iš pradžių nerodome (arba rodom tik pirmąją)
            if i != 0:
                diagram.clear_panel()

            # Saugojam diagramą (jei vėliau reikia)
            diagrams.append(diagram)

            # Pririšam mygtuką prie diagramos
            button.bind("click", lambda event, d=diagram: switch_diagram(d))

            container <= button

                # Pradžioje rodom pirmą diagramą (nebūtina jei jau parodyta)
        if diagrams:
            switch_diagram(diagrams[0])
            tex_len = f"Text length: {len(func.original_text)}"
            doc["text_length"].text = tex_len


def graph_draw_function(width = None, height = None):
    panel = doc['panel']
    panel.clear() 
    panel_height= panel.height
    panel_width = panel.width
    output_error = doc['output_mmverify']
    #print("print",)
    if doc["use_custom_rect"].checked:
        height, width = get_custom_rect_dimensions()
    get_width = width if width is not None else None
    get_height = height if height is not None else None
    if func.original_text:
        func.verify_mm(func.original_text)
        doc['textarea_num_div'].html = '<br>'.join(func.line_num)
        #print(func.error_collector)
        output_error.text = func.error_collector
    elif output_error.text  is not None:
        output_error.clear()
        


    if not doc["diagram_mode"].checked:
        curate_diagram_main_steps(get_width,get_height)
    else:
        curate_diagram_step_by_step(get_width,get_height)

def edit_button(event):
    reset(event)
    #func.original_text = textarea.value    
    if textarea.disabled :
        textarea.disabled  = False
        doc['edit'].text = "Edit"
        doc["modify_text"].html  =  "<br>".join(func.modify_text_array)
        sync_scroll(event)
    else:
        textarea.disabled  = True
        doc['edit'].text = "Edit"
        sync_scroll(event)
        func.verify_mm( textarea.value)
        doc["modify_text"].html  =  "<br>".join(func.modify_text_array)
        doc['textarea_num_div'].html= '<br>'.join(func.line_num) 
        

    graph_draw_function()

doc['edit'].bind('click',edit_button)
doc['edit'].bind('click',edit_button)

def delayed_checker_and_continue():
    global textarea
    func.verify_mm( textarea.value)
    doc["modify_text"].html  =  "<br>".join(func.modify_text_array)


def read_Check_And_Draw(event):
    #global textarea
    file_read()
    
    #func.original_text =  textarea.value
    window.setTimeout(lambda: delayed_checker_and_continue(), 800)


def get_custom_rect_dimensions():
    if doc["use_custom_rect"].checked:
        try:
            height = float(doc["rect_height"].value)
            width = float(doc["rect_width"].value)
            if height > 0 and width > 0:
                return height, width
        except ValueError:
            pass
    return None, None

def handle_submit_custom_size(event):
    height, width = get_custom_rect_dimensions()
    graph_draw_function(width, height)

doc["submit_rect_height_and_width"].bind("click", handle_submit_custom_size)

def maybe_run_graph_draw(event=None):
    reset(event)
    if doc["use_custom_rect"].checked:
        height, width = get_custom_rect_dimensions()
        if height is not None or width is not None:
            graph_draw_function(width, height)
    else:
        graph_draw_function()
doc["use_custom_rect"].bind("change", maybe_run_graph_draw)

def choose_diagram_mode(event = None):
    if not doc["diagram_mode"].checked:
        curate_diagram_main_steps()
    else:
        curate_diagram_step_by_step()


doc["diagram_mode"].bind("change", maybe_run_graph_draw)
doc["comment_mode"].bind("change", maybe_run_graph_draw)

example = """$( Konstantų apibrėžimas $)
$c 0 1 2 3 4 5 + = ( ) ⊢ $.

$( Kintamųjų apibrėžimas $)
$v x y z $.


$( Aksiomos $)
a1 $a ⊢ 1 $.

${ $( 1 + 1 = 2 $)
  h1 $e ⊢ 1 $.
  h2 $e ⊢ 1 $.
  add1 $a ⊢ ( 1 + 1 ) = 2 $.
$}
t-1p1e2 $p ⊢ ( 1 + 1 ) = 2 $= a1 a1 add1 $.


${ $( Iš lygybės gauname reikšmę: jei ⊢ (1 + 1) = 2, tai ⊢ 2 $)
  h3 $e ⊢ ( 1 + 1 ) = 2 $.
  convert $a ⊢ 2 $.
$}
t-conv2 $p ⊢ 2 $= t-1p1e2 convert $.

${ $( 1 + 2 = 3 $)
  h4 $e ⊢ 1 $.
  h5 $e ⊢ 2 $.
  add2 $a ⊢ ( 1 + 2 ) = 3 $.
$}

t-1p2e3 $p ⊢ ( 1 + 2 ) = 3 $= a1 t-conv2 add2 $.

${ $( Iš lygybės gauname reikšmę: jei ⊢ (1 + 2) = 3, tai ⊢ 3 $)
  h6 $e ⊢ ( 1 + 2 ) = 3 $.
  convert3 $a ⊢ 3 $.
$}
t-conv3 $p ⊢ 3 $= t-1p2e3 convert3 $.

${ $( 2 + 3 = 5 $)
  h7 $e ⊢ 2 $.
  h8 $e ⊢ 3 $.
  add3 $a ⊢ ( 2 + 3 ) = 5 $.
$}

t-2p3e5 $p ⊢ ( 2 + 3 ) = 5 $= t-conv2 t-conv3 add3 $.

${ $( Iš lygybės gauname reikšmę: jei ⊢ (1 + 2) = 3, tai ⊢ 3 $)
  h9 $e ⊢ ( 2 + 3 ) = 5 $.
  convert5 $a ⊢ 5 $.
$}
t-conv5 $p ⊢ 5 $= t-2p3e5 convert5 $."""

#setset =  iset_mm + "t-1p1e2 $p ⊢ ( 1 + 1 ) = 2 $= a1 a1 add1 $."
#print(setset)
if __name__ == '__main__':
    textarea = doc['container_textarea']

    panel = doc['panel']
    reset(None)
    func = Function(example)
    doc["modify_text"].html  =  "<br>".join(func.modify_text_array)

    #print(func.original_text)
    textarea.value = func.original_text

    work_with_textarea(func)
    
    graph_draw_function()
    
    doc["fileMmInput"].bind("input", read_Check_And_Draw)

