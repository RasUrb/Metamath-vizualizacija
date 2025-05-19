from browser import document as doc, timer # type: ignore
import browser.html as html # type: ignore

svg = doc['panel']
intervals = {}
viewBox = {'x':0,'y':0, 'width':500, 'height':500}
viewbox = svg.getAttribute("viewBox").split()
bounding_box = svg.getBoundingClientRect()
viewbox[2] = bounding_box.width
viewbox[3] = bounding_box.height

DEBUG = False

def log(msg):
    if DEBUG:
        print(msg)
        
log(f"svg_width: {viewbox[2]}, svg_height: {viewbox[3]}")

def get_viewBox():
    """
    The function `get_viewBox` converts the `viewbox` values into integers and stores them in a
    dictionary `viewBox`.
    """
    global viewBox, viewbox 
    viewBox = {'x':int(viewbox[0]),
                'y':int(viewbox[1]), 
                'width':int(viewbox[2]), 
                'height':int(viewbox[3])}
    log(f"viewbox: {viewBox}")

    """
    The function `update_viewBox` updates the viewBox attribute of an SVG element with new values.
    """
def update_viewBox():
    new_viewBox = f"{viewBox['x']} {viewBox['y']} {viewBox['width']} {viewBox['height']}"
    svg.setAttribute("viewBox",new_viewBox)
    log(f"update_viewBox: {new_viewBox}")
    
def reset(event):
    get_viewBox()
    update_viewBox()
    #log(viewBox)
    

    
def zoom_in():
    """
    The `zoom_in` function decreases the width and height of the viewBox by 100 units and updates the
    viewBox accordingly.
    """
    global viewBox
    if viewBox['width']- 100 > 100:
        viewBox['width'] -= 100
        viewBox['height'] -= 100
        viewBox['x'] += 50
        update_viewBox()
    log(f"[zoom] New dimensions: {viewBox['width']}x{viewBox['height']} at x={viewBox['x']}")


def zoom_out():
    global viewBox
    viewBox['width'] += 100
    viewBox['height'] += 100
    viewBox['x'] -= 50
    update_viewBox()
    log(f"[zoom] New dimensions: {viewBox['width']}x{viewBox['height']} at x={viewBox['x']}")

    
def move_left():
    global viewBox
    viewBox['x'] += 10
    update_viewBox()
    #log(f"move_left:{viewBox['x']}")
    
def move_right():
    global viewBox
    viewBox['x'] -= 10
    update_viewBox()
    #log(f"move_right:{viewBox['x']}")

def move_up():
    global viewBox
    viewBox['y'] += 10
    update_viewBox()
    #log(f"move_up:{viewBox['y']}")
    
def move_down():
    global viewBox
    viewBox['y'] -= 10
    update_viewBox()
    #log(f"move_down:{viewBox['y']}")
    
def start_move(event, direction_func):
    """Start the movement for a given direction."""
    global intervals
    if event.target.id not in intervals:
        intervals[event.target.id] = timer.set_interval(direction_func, 60)  # Call every 50ms
    log(f"[start_move] Starting move: {event.target.id}")
    


def stop_move(event):
    """Stop the movement for a button."""
    global intervals
    button_id = event.target.id
    if button_id in intervals:
        timer.clear_interval(intervals[button_id])
        del intervals[button_id]
    log(f"[stop_move] Stopped move: {button_id}")

""" Keyboard button processing for SVG movement and zooming. WASD or arrows – movement, /- – zoom in / out, R – reset. """
def onkeydown(event):
    log(f"[keydown] Key pressed: {event.key}")
    #Make sure if it in "TEXTAREA" or "INPUT" tke SVG doesn't move
    if event.target.tagName in ("TEXTAREA", "INPUT"):
        return
    key = event.key    
    if key in ["A", "a", "ArrowLeft"]:
        #event.preventDefault()
        move_left()
        
    elif key in ["D", "d", "ArrowRight"]:
        #event.preventDefault()
        move_right()
        
    elif key in ["W", "w", "ArrowUp"]:
        #event.preventDefault()
        move_up()
        
    elif key in ["S", "s", "ArrowDown"]:
        #event.preventDefault() 
        move_down()
        
    elif key in ["=", "+"]:
        #event.preventDefault()
        zoom_in()
            
    elif (event.key == '-'):
       # event.preventDefault()
        zoom_out()
            
    elif event.key == 'r':  # Trigger for moving back to the beginning
       # event.preventDefault()
        reset(event)
        
    log(f"[move] x={viewBox['x']}, y={viewBox['y']}")

get_viewBox()  
doc.bind("keydown", onkeydown)

doc["move_right"].bind("mousedown", lambda ev: start_move(ev, move_right))
doc["move_left"].bind("mousedown", lambda ev: start_move(ev, move_left))
doc["move_up"].bind("mousedown", lambda ev: start_move(ev, move_up))
doc["move_down"].bind("mousedown", lambda ev: start_move(ev, move_down))

doc["move_right"].bind("mouseup", stop_move)
doc["move_left"].bind("mouseup", stop_move)
doc["move_up"].bind("mouseup", stop_move)
doc["move_down"].bind("mouseup", stop_move)

doc["move_right"].bind("mouseleave", stop_move)
doc["move_left"].bind("mouseleave", stop_move)
doc["move_up"].bind("mouseleave", stop_move)
doc["move_down"].bind("mouseleave", stop_move)

doc["zoom_in"].bind("mousedown", lambda ev: start_move(ev, zoom_in))
doc["zoom_out"].bind("mousedown", lambda ev: start_move(ev, zoom_out))

doc["zoom_in"].bind("mouseup", stop_move)
doc["zoom_out"].bind("mouseup",stop_move)

doc["zoom_in"].bind("mouseleave", stop_move)
doc["zoom_out"].bind("mouseleave",stop_move)

doc["reload_function"].bind("click",reset)




