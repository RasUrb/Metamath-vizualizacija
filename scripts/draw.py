from browser import window  # type: ignore
from browser import document as doc  # type: ignore
import browser.html as html  # type: ignore
import browser.svg as svg  # type: ignore
import json

DEBUG = False

def log(msg):
    if DEBUG:
        print(msg)

default_color_rect = {
    "f": "#c0c4ff",  # function
    "e": "#ffff80",  # example
    "a": "#d700d7",  # axiom
    "p": "#66ff8c",  # proof
    "com": "#80ffff"     #comment
}
default_color_text = {
    "f": "#000000",  # function
    "e": "#000000",  # example
    "a": "#000000",  # axiom
    "p": "#000000",  # proof
    "com": "#000000"     #comment
}
default_color_stroke = {
    "f": "#000000",  # function
    "e": "#000000",  # example
    "a": "#000000",  # axiom
    "p": "#000000",  # proof
    "com": "#000000"     #comment
}
panel = doc["panel"]
def setup_color_configurations():
    global stroke_colors, text_colors, rect_colors
    try:
        if "stroke_colors" in window.localStorage:
            stroke_colors = json.loads(window.localStorage["stroke_colors"])
            if not isinstance(stroke_colors, dict):
                raise ValueError("stroke_colors in localStorage is not a dict. Resetting to default.")
        else:
            raise KeyError
    except (KeyError, ValueError, json.JSONDecodeError):
        stroke_colors = default_color_stroke.copy()
        window.localStorage["stroke_colors"] = json.dumps(stroke_colors)
        
    try:
        if "text_colors" in window.localStorage:
            text_colors = json.loads(window.localStorage["text_colors"])
            if not isinstance(text_colors, dict):
                raise ValueError("text_colors in localStorage is not a dict. Resetting to default.")
        else:
            raise KeyError
    except (KeyError, ValueError, json.JSONDecodeError):
        text_colors = default_color_text.copy()
        window.localStorage["text_colors"] = json.dumps(text_colors)
        
    try:
        if "rect_colors" in window.localStorage:
            rect_colors = json.loads(window.localStorage["rect_colors"])
            if not isinstance(rect_colors, dict):
                raise ValueError("rect_colors in localStorage is not a dict. Resetting to default.")
        else:
            raise KeyError
    except (KeyError, ValueError, json.JSONDecodeError):
        rect_colors = default_color_rect.copy()
        window.localStorage["rect_colors"] = json.dumps(rect_colors)
setup_color_configurations()      

class ProofDiagram:
    def __init__(self, panel = doc['panel'], svg_height = 700, svg_width = 550):
        self.panel = panel
        self.svg_height = svg_height
        self.svg_width  = svg_width
        self.rectangle = []
        self.ovals = []
        self.text = []
        
    def __str__(self) -> str:
        size = f"svg height: {self.svg_height} and width: {self.svg_width}\n"
        if hasattr(self, 'rect_colors'):
            colors = "".join(f"{color}: {self.rect_colors[color]}\n" for color in self.rect_colors)
        else:
            colors = "No rect_colors defined\n"
        texts = "".join(f"{text}," for text in self.text)
        return size + colors + texts
    def get_total_bounds(self):
        if not self.rectangle:
            log("Warning: no rectangles to calculate bounds.")
            return 0, 0, 0, 0
        else:
            min_x = min(rect.dx for rect in self.rectangle)
            max_x = max(rect.dx + rect.width for rect in self.rectangle)
            min_y = min(rect.dy for rect in self.rectangle)
            max_y = max(rect.dy + rect.height for rect in self.rectangle)

            total_width = max_x - min_x
            total_height = max_y - min_y

        return min_x, min_y, total_width, total_height

    def clear_panel(self):
        while self.panel.firstChild:
            self.panel.removeChild(self.panel.firstChild)
        
    def draw_all_rectangle(self):
        if not self.rectangle:
            log("No rectangles to draw.")
        for i, rect in enumerate(self.rectangle):
            log(f"Drawing rectangle #{i}: class {rect.class_name}, position ({rect.dx}, {rect.dy}), color: {rect.color}")
            self.panel <= rect.draw_rect()
                        
    def draw_all_text(self):
        if not self.text:
            log("No text to draw.")
        for i, text in enumerate(self.text):
            #log(f"Drawing text #{i}: class {text.class_name}, position ({text.dx}, {text.dy})")
            self.panel <= text.curate_text()
    
    def rect_to_oval(self):
        pass    
    
    def oval_to_rect(self):
        # self.clear_panel(self)
        # for oval in self.ovals:
        #     self.panel <= oval 
        pass    
    
    def draw_all(self):
        log("Redrawing all rectangles and texts...")
        self.change_color_rect()
        self.change_color_text()
        self.draw_all_rectangle()
        self.draw_all_text()
                
    def rect_width(self, func_len, font_size, stroke_width):
        avg_char_width = font_size * 0.6

        text_width = func_len * avg_char_width
        total_width = text_width + 10 * 2
        return total_width + stroke_width #width
        
    def change_color_rect(self):
        for rect in self.rectangle:
            for symbol in rect_colors:
                if rect.class_name == symbol:
                    new_color = rect_colors[symbol]
                    if rect.color != new_color:
                        log(f"Changing color of class '{symbol}' from {rect.color} to {new_color}")
                        rect.change_color_rect(rect_colors[symbol])
    
    def change_color_text(self):
        for text in self.text:
            for symbol in rect_colors:
                if text.class_name == symbol:
                    new_color = text_colors[symbol]
                    if text.color != new_color:
                        log(f"Changing color of class '{symbol}' from {text.color} to {new_color}")
                        text.change_color(text_colors[symbol])
        
    def rect_height(self, stroke_width, font_size, padding):
        stroke_and_witdh_height = font_size + stroke_width + padding
        return stroke_and_witdh_height
    #Draw main proof
    def _main_header(self, name, y_pos,width, height, stroke_width, font_size, padding):
        if  width is None:
            x_pos = 0 #(self.svg_width / 4)
            rect_w = self.svg_width
        else:
            rect_w = width    
            x_pos =  self.svg_width /2  - rect_w / 2
        rect_h = self.rect_height(stroke_width, font_size, padding)  if height is None else height
        
        color_rect = rect_colors.get("p", "#ffffff")
        stroke_color = stroke_colors.get("p","#000000")
        rect = Rectangle(x_pos, y_pos, rect_w, rect_h, stroke_width, stroke_color, color_rect, "p")
        self.rectangle.append(rect)

        color_text = text_colors.get("p", "#ffffff")
        text = Text(x_pos, y_pos, rect_w, rect_h, f"$p {str(name)}", color_text, font_size,"p")
        self.text.append(text)
        return y_pos + rect_h
    #Draw proof body
    def _draw_single_proof(self, func, x_pos, y_pos, width, height, stroke_width, font_size, padding):
        rect_w = self.rect_width(len(func), font_size, stroke_width) if width is None else width
        rect_h = self.rect_height(stroke_width, font_size, padding)  if height is None else height
        
        log(f" -> Rectangle width: {rect_w}, x: {x_pos}, y: {y_pos}")
            
        x_pos = self.svg_width /2  - rect_w / 2
        if func[0] =="$":
            color_key = "com" if func[1:2] =='(' else  func[1:2]
        else:
            color_key = ""
        color = rect_colors.get(color_key, "white")
        stroke_color = stroke_colors.get(color_key,"#000000")
            
        color_text = "#000000" if func == '(' or func == ')' else text_colors.get(color_key, "#000000")
        
        rect = Rectangle(x_pos, y_pos, rect_w, rect_h, stroke_width, stroke_color, color, color_key)
        text = Text(x_pos, y_pos, rect_w, rect_h, func, font_size, color_text, color_key)

        self.rectangle.append(rect)
        self.text.append(text)
            
        return y_pos + rect_h#height
    
    def draw_graph(self, proofs, proofs_name, width = None, height= None, x_pos=0, y_pos=0, stroke_width=2, font_size=20, padding = 10):
        log(f"Drawing graph for proof: {proofs_name}")
        y_pos += self._main_header(proofs_name, y_pos, width, height, stroke_width, font_size, padding)#height
        log(f"y_pos:{y_pos}")
        for i, func in enumerate(proofs):
            log(f"Adding proof #{i}: {func}")
            y_pos =  self._draw_single_proof( func, x_pos, y_pos, width, height, stroke_width, font_size, padding) 
            log(f"y_pos:{y_pos}")
        self.draw_all()
        
class Rectangle:
    def __init__(self, dx=0, dy=0, width=10, height=10, stroke_width=2, stroke_color="black", color="#c0c4ff", class_name="f"):
        self.dx = float(dx)
        self.dy = float(dy)
        self.width = float(width)
        self.height = float(height)
        self.stroke_width = float(stroke_width)
        self.stroke_color = stroke_color
        self.color = color 
        self.class_name = class_name

        self.rect_svg = self.draw_rect()
        
    def __str__(self):
        return f"class: {self.class_name}\n dx: {self.dx} dy: {self.dy}\n size: {self.width}x{self.height}\n stroke width: {self.stroke_width} stroke color: {self.stroke_color} color: {self.color}"
        
    def draw_rect(self):
        self.rect_svg = svg.rect(
            x=self.dx,
            y=self.dy,
            width=self.width,
            height=self.height,
            stroke=self.stroke_color,
            stroke_width=self.stroke_width,
            fill=self.color,
            )
        self.rect_svg.attrs["class"] = self.class_name
        return self.rect_svg
    
    def draw_oval(self):
        ellipse = svg.ellipse(
            cx=self.dx + self.width / 2,
            cy=self.dy + self.height / 2,
            rx=self.width / 2,
            ry=self.height / 2,
            stroke=self.stroke_color,
            stroke_width=self.stroke_width,
            fill=self.color
        )
        ellipse.attrs["class"] = self.class_name
        return ellipse
    def change_class(self, new_class):
        self.class_name = new_class
        self.rect_svg.attrs["class"] = new_class

    def change_stroke_color(self, color):
                self.stroke_color = color
                self.rect_svg.setAttribute("stroke_color", self.stroke_color)

    def change_color(self, color):
                self.color = color
                # self.curate_Rect()
                # self.draw_Rect()
                self.rect_svg.setAttribute("fill", self.color)
                

    def change_position(self, x, y):
                self.dx = x
                self.dy = y
                self.rect_svg.setAttribute("x", self.dx)
                self.rect_svg.setAttribute("y", self.dy)

    def size(self, width, height):
                # log(f"rect_svg: {width, height}")
                self.width = width
                self.height = height
                self.rect_svg.setAttribute("width", self.width)
                self.rect_svg.setAttribute("height", self.height)

class Text:
    def __init__(self, dx=0, dy=0, width=0, height=0, text: str = "", font_size=16, color="black", class_name="f"):
        self.dx = dx
        self.dy = dy
        self.width = width / 2
        self.height = height / 1.5
        self.text = text
        self.font_size = font_size
        self.color = color
        self.class_name = class_name
        self.text_svg = self.curate_text()
        
    def __str__(self):
        return self.text
    def change_class(self, new_class):
        self.class_name = new_class
        self.text_svg.attrs["class"] = new_class

    def change_color(self, color):
        self.color = color
        self.text_svg.setAttribute("fill", self.color)

    def curate_text(self):
        self.text_svg = svg.text(
            self.text,
            x=self.dx + self.width,
            y=self.dy + self.height,
            text_anchor="middle",
            alignment_baseline="middle",
            font_size=self.font_size,
            fill=self.color,
            )
        self.text_svg.attrs["class"] = self.class_name
        return self.text_svg

#Ractengle
def save_rect_colors():
    window.localStorage["rect_colors"] = json.dumps(rect_colors)
    
def change_rect_colors(color, rect_class):
    key = rect_class.lstrip(".")  # pašalinti tašką, jei buvo CSS stiliaus klasė
    rect_colors[key] = color
    window.localStorage["rect_colors"] = json.dumps(rect_colors)

    selector = f"rect.{key}, ellipse.{key}"  # pasirenkame tik <rect> elementus su ta klase
    shapes = doc.select(selector)

    for shape in shapes:
        shape.setAttribute("fill", color)
        log(f"Updated <rect> with class '{key}' to color {color}")
 

    
def change_f_rect_color(event):
    chosen_color = doc["colorF_rect"].value
    change_rect_colors(chosen_color, "f")

doc["colorF_rect"].bind("input", change_f_rect_color)

def change_e_rect_color(event):
    chosen_color = doc["colorE_rect"].value
    change_rect_colors(chosen_color, "e")

doc["colorE_rect"].bind("input", change_e_rect_color)

def change_a_rect_color(event):
    chosen_color = doc["colorA_rect"].value
    change_rect_colors(chosen_color, "a")

doc["colorA_rect"].bind("input", change_a_rect_color)

def change_p_rect_color(event):
    chosen_color = doc["colorP_rect"].value
    change_rect_colors(chosen_color, "p")

doc["colorP_rect"].bind("input", change_p_rect_color)

def change_com_rect_color(event):
    chosen_color = doc["colorCom_rect"].value
    change_rect_colors(chosen_color, "com")

doc["colorCom_rect"].bind("input", change_com_rect_color)

def show_color_rect():
    #global rect_colors
    log(f"rect colors:{rect_colors}")
    doc["colorF_rect"].value = rect_colors['f']
    doc["colorE_rect"].value = rect_colors['e']
    doc["colorA_rect"].value = rect_colors['a']
    doc["colorP_rect"].value = rect_colors['p']
    doc["colorCom_rect"].value = rect_colors['com']

def return_default_color_rect(event):
    global default_color_rect
    rect_colors.clear()
    rect_colors.update(default_color_rect)

    #log(rect_colors)
    for symbol in default_color_rect:
        #log(f"return_color:{symbol}")
        selector = f"{symbol}"  
        change_rect_colors(rect_colors[symbol], selector)
    show_color_rect()
    
doc["change_color_rect_back"].bind("click", return_default_color_rect)


#Text
def change_text_colors(color, text_class):
    key = text_class.lstrip(".")  # pašalinti tašką, jei buvo klasės CSS formai
    text_colors[key] = color
    window.localStorage["text_colors"] = json.dumps(text_colors)

    selector = f"text.{key}"  # užtikrinti, kad pasirenkame tik <text> elementus
    texts = doc.select(selector)
    #log("texts",texts)
    for t in texts:
        t.setAttribute("fill", color)
        log(f"Updated text '{t.text}' with class '{key}' to color {color}")

def change_f_text_color(event):
    chosen_color = doc["colorF_text"].value
    change_text_colors(chosen_color, "f")

doc["colorF_text"].bind("input", change_f_text_color)

def change_e_text_color(event):
    chosen_color = doc["colorE_text"].value
    change_text_colors(chosen_color, "e")

doc["colorE_text"].bind("input", change_e_text_color)

def change_a_text_color(event):
    chosen_color = doc["colorA_text"].value
    change_text_colors(chosen_color, "a")

doc["colorA_text"].bind("input", change_a_text_color)


def change_p_text_color(event):
    #log("text p color")
    chosen_color = doc["colorP_text"].value
    change_text_colors(chosen_color, "p")

doc["colorP_text"].bind("input", change_p_text_color)

def change_com_text_color(event):
   # log("text p color")
    chosen_color = doc["colorCom_text"].value
    change_text_colors(chosen_color, "com")

doc["colorCom_text"].bind("input", change_com_text_color)

def return_default_color_text(event):
    global default_color_text
    text_colors.clear()
    text_colors.update(default_color_text)
    log(text_colors)
    for symbol in text_colors:
        #log(f"return_color:{symbol}")
        selector = f"{symbol}"  
        change_text_colors(text_colors[symbol], selector)
    show_color_text()

doc["change_color_text_back"].bind("click", return_default_color_text)

def show_color_text():
    #log(f"rect colors:{text_colors}")
    doc["colorF_text"].value = text_colors['f']
    doc["colorE_text"].value = text_colors['e']
    doc["colorA_text"].value = text_colors['a']
    doc["colorP_text"].value = text_colors['p']
    doc["colorCom_text"].value = text_colors['com']

#Stroke
def change_rect_stroke_colors(color, stroke_class):
    key = stroke_class.lstrip(".")  # pašalinti tašką, jei buvo CSS stiliaus klasė
    log(f"Stroke class: {key}, old color: {stroke_colors[key]}, new color{color}")
    stroke_colors[key] = color
    window.localStorage["stroke_colors"] = json.dumps(stroke_colors)

    selector = f"rect.{key}, ellipse.{key}"  # pasirenkame tik <stroke> elementus su ta klase
    shapes = doc.select(selector)
    #log
    for shape in shapes:
        shape.setAttribute("stroke", color)
        log(f"Updated <stroke> with class '{key}' to color {color}")

def change_f_stroke_color(event):
    chosen_color = doc["colorF_stroke"].value
    change_rect_stroke_colors(chosen_color, "f")

doc["colorF_stroke"].bind("input", change_f_stroke_color)

def change_e_stroke_color(event):
    chosen_color = doc["colorE_stroke"].value
    change_rect_stroke_colors(chosen_color, "e")

doc["colorE_stroke"].bind("input", change_e_stroke_color)

def change_a_stroke_color(event):
    chosen_color = doc["colorA_stroke"].value
    change_rect_stroke_colors(chosen_color, "a")

doc["colorA_stroke"].bind("input", change_a_stroke_color)

def change_p_stroke_color(event):
    chosen_color = doc["colorP_stroke"].value
    change_rect_stroke_colors(chosen_color, "p")

doc["colorP_stroke"].bind("input", change_p_stroke_color)

def change_com_stroke_color(event):
    chosen_color = doc["colorCom_stroke"].value
    change_rect_stroke_colors(chosen_color, "c")

doc["colorCom_stroke"].bind("input", change_com_stroke_color)

def return_default_color_stroke(event):
    global default_color_stroke
    stroke_colors.clear()
    stroke_colors.update(default_color_stroke)
    #log(stroke_colors)
    for symbol in default_color_stroke:
        #log(f"return_color:{symbol}")
        selector = f"{symbol}"  
        change_rect_stroke_colors(stroke_colors[symbol], selector)
    show_color_stroke()
    
doc["change_color_stroke_back"].bind("click", return_default_color_stroke)

def show_color_stroke():
    log(f"rect colors:{stroke_colors}")
    doc["colorF_stroke"].value = stroke_colors['f']
    doc["colorE_stroke"].value = stroke_colors['e']
    doc["colorA_stroke"].value = stroke_colors['a']
    doc["colorP_stroke"].value = stroke_colors['p']
    doc["colorCom_stroke"].value = stroke_colors['com']


def return_default_color_all(event):
    return_default_color_rect(event)
    return_default_color_text(event)
    return_default_color_stroke(event)

doc["change_all_back"].bind("click", return_default_color_text)

def bind_color_input(input_id, change_func, symbol):
    # Randa HTML elementą pagal ID
    input_element = doc[input_id]
    
    # Pririša "input" įvykio klausytoją
    input_element.bind("input", lambda ev: change_func(input_element.value, symbol))


def show_color_all_svg():
    log(f"Rectangle colors:")
    show_color_rect()
    log(f"Text colors:")
    show_color_text()
    log(f"rect stroke colors:")
    show_color_stroke()
show_color_all_svg()       

# diagram = ProofDiagram(panel)

# log(diagram)
