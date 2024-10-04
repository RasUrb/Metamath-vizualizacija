from browser import document as doc, window
import browser.html as html
#from test_draw import *

def bind_movement(diagram):

    def onkeydown(event):
        
        dx, dy = 0, 0

        if isinstance(event.target, html.TEXTAREA) or isinstance(event.target, html.INPUT):
            return
        
        if (event.key == 'a') or (event.key == "ArrowLeft"):
            dx = -10
        elif (event.key ==  'd') or (event.key == "ArrowRight"):
            dx = 10
        elif (event.key == 'w') or (event.key == "ArrowUp"):
            dy = -10
        elif (event.key == 's') or (event.key == "ArrowDown"):
            dy = 10
        
        elif (event.key == '=') or (event.key == '+'):
            diagram.zoom_in()
            
        elif (event.key == '-'):
            diagram.zoom_out()

            
        elif event.key == 'r':  # Trigger for moving back to the beginning
            diagram.offset()

        diagram.move_all(dx, dy)
    
    def zoom_in(event):
        diagram.zoom_in()
    def zoom_out(event):
        diagram.zoom_out()
    
    def move_button(event):
        button = event.target.id
        #print(button)
        if button == "move_left":
            diagram.move_all(-10, 0)
        elif button == "move_up":
            diagram.move_all(0, -10)  
        elif button == "move_right":
            diagram.move_all(10, 0)  
        elif button == "move_down":
            diagram.move_all(0, 10)
    
    doc.bind("keydown", onkeydown)
    doc["zoom_in"].bind("click", zoom_in)
    doc["zoom_out"].bind("click",zoom_out)
    
    doc["move_left"].bind("click", move_button)
    doc["move_up"].bind("click", move_button)
    doc["move_right"].bind("click", move_button)
    doc["move_down"].bind("click", move_button)    

def save_img_here(event):
    
    svg = doc['panel']
    svg_data = svg.outerHTML
    canvas = window.document.createElement("canvas")
    ctx = canvas.getContext("2d")

    img = window.Image.new()
    svg_blob = window.Blob.new([svg_data], {"type": "image/svg+xml;charset=utf-8"})
    url = window.URL.createObjectURL(svg_blob)

            
    def onload_func(_):
        canvas.setAttribute('width',svg.clientWidth)
        canvas.setAttribute('height',svg.height)
        ctx.drawImage(img, 0, 0)
        window.URL.revokeObjectURL(url)
        print(f"canvas.width {canvas.width}, canvas.height {canvas.height}")
        canvas.toBlob(lambda blob: (
                link := window.document.createElement('a'),
                setattr(link, "href", window.URL.createObjectURL(blob)),
                setattr(link, "download", "diagram.png"),
                link.click()
        ), "image/png")

    img.onload = onload_func
    img.src = url        

doc["save_img"].unbind("click", save_img_here)   
doc["save_img"].bind("click", save_img_here)  
    
    # <button id="">◄</button>
    #                     <button id="">▲</button>
    #                     <button id="move_right">►</button>
    #                     <button id="move_down">▼</button>
    #<SVGSVGElement id="mySvg" xmlns="null" width="100" height="100"> 