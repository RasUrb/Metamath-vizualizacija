#from typing import Self
from browser import document as doc
import browser.html as html
import browser.svg as svg
#from test_judejimas import *
#import re
#from funkcija import * 
        
#  # Variables to store the mouse offset relative to the element

class ProofDiagram:
        def __init__(self, panel):
                self.rectangle = [] #hold all rectangle class
                self.text = []#hold all Text class
                self.panel = panel
                self.offset_x = 0
                self.offset_y = 0
                self.offset_height = 0
                self.offset_width = 0
                self.offset_font_size = 0
                self.scale_factor = 1
                

        def __repr__(self) -> str:
                return f"Rectangle:{self.rectangle}\n Contend:{self.text}\n"
        
        def move_all_rect(self, dx, dy):
                if self.rectangle:
                        for rect in self.rectangle:
                                rect.move(dx, dy)
                                
        def move_all_text(self, dx, dy):
                if self.text:
                        for text in self.text:
                                text.move(dx, dy)        
        
        def move_all(self, dx, dy):
                self.offset_x += dx
                self.offset_y += dy
                self.move_all_rect(dx, dy)                       
                self.move_all_text(dx, dy)
        
        def size_all(self, width, height, font_size):
                self.offset_height += height
                self.offset_width += width
                self.offset_font_size += font_size
                if (width != 0) or (height != 0):
                        #print(f"all: {width, height}")
                        for i, rect in enumerate(self.rectangle):
                                rect.size(width, height)
                                
                                if i != 0:
                                        rect.move(0,height*i)


                                #rect.move(0, height)
                        for i,text in enumerate(self.text):
                                text.size(width, height, font_size)
                                #text.move(0,height)
                                text.move(width,0)
                                if i != 0:
                                        text.move(0,height*i)
                        
        def draw_all_rectangle(self):
                for rect in self.rectangle:
                        rect.draw_Rect()
        
        def draw_all_text(self):
                for text in self.text:
                        text.text_write()
        
        def draw_all(self):
                self.draw_all_rectangle()
                self.draw_all_text()
        
        def offset(self):
                if (self.offset_x != 0) or (self.offset_y != 0):
                        self.move_all(-self.offset_x,-self.offset_y)
                if (self.offset_height != 0) or (self.offset_width != 0):
                        self.size_all(-self.offset_width, -self.offset_height, -self.offset_font_size)
                self.offset_x = 0
                self.offset_y = 0
                self.offset_font_size=0
                self.offset_height = 0
                self.offset_width = 0
                self.zoom_offset()
        
        def update_viewbox(self):
                new_viewbox = f"{(1 - self.scale_factor) * 250} {(1 - self.scale_factor) * 250} {500 * self.scale_factor} {500 * self.scale_factor}"
                self.panel.setAttribute("viewBox",new_viewbox)
        def zoom_offset(self):
                self.scale_factor = 1 
                transform_value = f"scale({self.scale_factor})"
                print(transform_value)
                self.update_viewbox()
                #self.panel.setAttribute("transform", transform_value)        

        def zoom_in(self):
                if (self.scale_factor - 0.1) > 0.25:
                        self.scale_factor -= 0.1
                        transform_value = f"scale({self.scale_factor})"
                        print(transform_value)
                        self.update_viewbox()
                       # self.panel.setAttribute("viewBox", transform_value)
        def zoom_out(self):
                if (self.scale_factor +0.1) < 2:
                        self.scale_factor += 0.1
                        transform_value = f"scale({self.scale_factor})"
                        print(transform_value)
                        self.update_viewbox
                        #self.panel.setAttribute("viewBox", transform_value)    
        # def clear_all(self):
        #         self.rectangle.clear_panel
        #         self.text.clear_panel
        
        def clear_panel(self):
                while self.panel.firstChild:
                        self.panel.removeChild(self.panel.firstChild)
        def draw_graph(self, proofs):
                width = 250
                font_size = 16
                height = font_size + 10
                x_position = width
                y_position = 0
                stroke_width = 2
                
                for func in proofs:

                        func_len = len(func)
                        if func_len < stroke_width*2:
                                width = func_len*(16+10)
                        elif func_len > 8:
                                width = func_len*(16/2)
                        else:
                                width = func_len*(16-2)
                        
                        x_pos = x_position - (width/2)
                        if func[:2] == '$e':
                                rect = Rectangle(self.panel, x_pos, y_position, width, height, stroke_width, "black", "#a1eefff0")
                        elif func[:2] == "$a":
                                rect = Rectangle(self.panel, x_pos, y_position, width, height, stroke_width, "black", "#9fffb7")
                        else:
                                rect = Rectangle(self.panel, x_pos, y_position, width, height)
                        rect.draw_Rect()
                        tex = Text(self.panel, x_pos, y_position, width, height, func)
                        tex.text_write()
                        self.rectangle.append(rect)
                        self.text.append(tex)
                        

                        y_position += height #+ stroke_width
                        #print(x_position)
                
class Rectangle:
        def __init__(self, panel, dx = 0, dy = 0, width = 10, height = 10, stroke_width = 2, stroke_color="black", color = "#c0c4ff" ):
                self.panel = panel
                self.dx = dx
                self.dy = dy
                self.width = width
                self.height = height
                self.stroke_width = stroke_width
                self.stroke_color = stroke_color
                self.color = color
                self.rect = None
                
        def __repr__(self) -> str:
                if self.rect:
                        return f"""rect = {self.rect}"""
                else:
                        return f"dx = {self.dx}, dy = {self.dy}, width = {self.width}, height = {self.height}, color = {self.color}"
        
        def draw_Rect (self):
                self.rect =  svg.rect(x = self.dx, y = self.dy, 
                                width = self.width, height = self.height,
                                stroke=self.stroke_color,
                                stroke_width = self.stroke_width, fill = self.color)
                self.panel <= self.rect
                #return rect
                
        def clear_panel(self):
                while self.panel.firstChild:
                        self.panel.removeChild(self.panel.firstChild)
                self.rect = None
        
       
        def size(self, width, height):
                # print(f"rect: {width, height}")
                self.width += width
                self.height += height
                self.rect.setAttribute('width', self.width)
                self.rect.setAttribute('height', self.height)
                
                
        def move(self, dx, dy):
                self.dx += dx
                self.dy += dy
                self.rect.setAttribute('x', self.dx)
                self.rect.setAttribute('y', self.dy)
        
        def change_color(self,color):
                self.color = color
                self.rect.setAttribute('color', self.color)

class Text:
        def __init__(self, panel, dx = 0, dy = 0, width = 0, height = 0, text = str, font_size = 16, color = "black"):
                self.panel = panel
                self.dx = dx
                self.dy = dy
                self.width = width/2
                self.height = height/1.5
                self.text = text
                self.font_size = font_size
                self.color = color
                self.text_element = None
        
        def __repr__(self) -> str:
                pass
        
        def text_write (self):
                self.text_element = svg.text(
                        self.text,
                        x = self.dx + self.width,
                        y = self.dy + self.height,
                        text_anchor = "middle",
                        alignment_baseline = "middle",
                        font_size = self.font_size,
                        fill= self.color
                )
                # Set the text content using the text element's `text` property
                self.panel <= self.text_element
        
        def clear_panel(self):
                while self.panel.firstChild:
                        self.panel.removeChild(self.panel.firstChild)
                self.text_element = None
                
        def size(self, width, height, font_size):
                #print(width," ", height," ", font_size)
                if (width != 0) or (height != 0):
                        self.width += width
                        self.height += height
                        self.font_size += font_size
                        self.text_element.setAttribute('x', self.dx + self.width/2)
                        self.text_element.setAttribute('y', self.dy + self.height/2)
                        self.text_element.setAttribute('font-size', self.font_size)
                        self.text_element.setAttribute('text-anchor', "middle")# self.text_element.setAttribute({
                        self.text_element.setAttribute('alignment-baseline', "middle")# self.text_element.setAttribute({
                        print("text: ", self.width)
                        # 'width': self.width,
                        # 'height': self.height,
                        # 'font-size': self.font_size
                        # })
                        
        def move(self, dx, dy):
                self.dx += dx
                self.dy += dy
                self.text_element.setAttribute('x', self.dx + self.width)
                self.text_element.setAttribute('y', self.dy + self.height)




# def clear_panel():
#         while panel.firstChild:
#                 panel.removeChild(panel.firstChild)