# m3py.py (c) 2022 kouichi.matsuda@gmail.com
# version 0.0.1 (4/10/2022)
# (minimal) "Pseudo" Processing API module, based on tkinter, for Python
# This is only for teaching Python.
import tkinter as _tk_
import sys
parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']

_c_ = None
_root_ = None
_fill_color_ = 'whiteh'
_line_width_ = 1 
_line_color_ = 'black' 
_font_ = ('', 10)
_fps_ = 60 
_timer_id_ = -1 # timer for draw()
_mouseX_ = 0
_mouseY_ = 0
_mouseButton_ = 0

from typing import Final
LEFT: Final[int] = 1 # mouse: left button
CENTER: Final[int] = 2 # mouse: middle button
RIGHT: Final[int] = 3 # mouse: right button

def _rgbtohex_(r,g,b):
    if g is None or b is None:
        return f'#{r:02x}{r:02x}{r:02x}'
    else:
        return f'#{r:02x}{g:02x}{b:02x}'

def _callMouseFunc_(func): # common mouse callback
    if func.__code__.co_argcount == 0:
        func()
    else:
        func(_mouseX_, _mouseY_)

def _mouseProcessed_(e, func): # common mouse processed
    global _mouseX_, _mouseY_
    _mouseX_ = e.x
    _mouseY_ = e.y
    _callMouseFunc_(func)
    
def _mouseClicked_1_(e): # LEFT button clicked
    global _mouseButton_
    _mouseButton_ = LEFT
    try:
        if callable(parent_module.mouseClicked):
            _mouseProcessed_(e, parent_module.mouseClicked)
    except AttributeError:
        pass
    _mouseButton_ = 0

def _mouseClicked_2_(e):# CENTER button clicked
    global _mouseButton_
    _mouseButton_ = CENTER
    try:
        if callable(parent_module.mouseClicked):
            _mouseProcessed_(e, parent_module.mouseClicked)
    except AttributeError:
        pass
    _mouseButton_ = 0

def _mouseClicked_3_(e): # RIGHT button clicked
    global _mouseButton_
    _mouseButton_ = RIGHT
    try:
        if callable(parent_module.mouseClicked):
            _mouseProcessed_(e, parent_module.mouseClicked)
    except AttributeError:
        pass
    _mouseButton_ = 0
            
def _mousePressed_1_(e):
    global _mouseButton_
    _mouseButton_ = LEFT
    try:
        if callable(parent_module.mousePressed):
            _mouseProcessed_(e, parent_module.mousePressed)
    except AttributeError:
        pass

def _mousePressed_2_(e):
    global _mouseButton_
    _mouseButton_ = CENTER
    try:
        if callable(parent_module.mousePressed):
            _mouseProcessed_(e, parent_module.mousePressed)
    except AttributeError:
        pass

def _mousePressed_3_(e):
    global _mouseButton_
    _mouseButton_ = RIGHT
    try:
        if callable(parent_module.mousePressed):
            _mouseProcessed_(e, parent_module.mousePressed)
    except AttributeError:
        pass

def _mouseMoved_(e):
    global _mouseButton_
    _mouseButton_ = 0
    try:
        if callable(parent_module.mouseMoved):
            _mouseProcessed_(e, parent_module.mouseMoved)
    except AttributeError:
        pass

def _init_(width = 200, height = 200, color = 'grey80'):
    global _root_, _c_
    _root_ = _tk_.Tk()
    _c_ = _tk_.Canvas(_root_, width = width, height = height, bg = color)
    _c_.pack()
    _c_.bind('<Button-1>', _mousePressed_1_)
    _c_.bind('<Button-2>', _mousePressed_2_)
    _c_.bind('<Button-3>', _mousePressed_3_)
    _c_.bind('<ButtonRelease-1>', _mouseClicked_1_)
    _c_.bind('<ButtonRelease-2>', _mouseClicked_2_)
    _c_.bind('<ButtonRelease-3>', _mouseClicked_3_)
    _c_.bind('<Motion>', _mouseMoved_)

def _setup_():
    if _root_ is None: _init_()
    if callable(parent_module.setup):
       parent_module.setup()

def run():
    if _root_ is None: _init_()
    try:
        _draw_()
    except AttributeError:
        pass
    _root_.mainloop()

def _draw_():
    if callable(parent_module.draw):
        global _timer_id_
        parent_module.draw()
        _timer_id_ = _c_.after(1000//_fps_, _draw_)

# The following APIs are exposed to users
def frameRate(fps):
    global _fps_
    if _root_ is None: _init_()
    if _fps_ != fps and _timer_id_ != -1:
        _c_.after_cancel(_timer_id_)
        _c_.after(1000//fps, _draw_)
    _fps_ = fps
    
def size(w, h):
    if _root_ is None: _init_()
    _c_.config(width=w, height=h)
    
def point(x, y):
    if _root_ is None: _init_()
    _c_.create_line(x, y, x, y, fill=_fill_color_)

def line(x1, y1, x2, y2):
    if _root_ is None: _init_()
    _c_.create_line(x1, y1, x2, y2, 
        fill=_line_color_, width=_line_width_)

def rect(x, y, w, h):
    if _root_ is None: _init_()
    _c_.create_rectangle(x, y, x+w, y+h, 
        fill=_fill_color_, outline=_line_color_, width=_line_width_)

def ellipse(x, y, w, h):
    if _root_ is None: _init_()
    _c_.create_oval(x-w/2, y-h/2, x+w/2, y+h/2, 
        fill=_fill_color_, outline=_line_color_, width=_line_width_)

def triangle(x1, y1, x2, y2, x3, y3):
    if _root_ is None: _init_()
    _c_.create_polygon(x1, y1, x2, y2, x3, y3,
        fill=_fill_color_, outline=_line_color_, width=_line_width_)

def guad(x1, y1, z2, y2, x3, y3, x4, y4):
    if _root_ is None: _init_()
    _c_.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4,
        fill=_fill_color_, outline=_line_color_, width=_line_width_)   
    
def text(t, x, y):
    if _root_ is None: _init_()
    _c_.create_text(x, y, text=str(t), fill=_fill_color_, font=_font_)

def textSize(s):
    global _font_
    if _root_ is None: _init_()
    _font_ = ('', s)

def fill(r, g=-1, b=-1):
    global _fill_color_
    if _root_ is None: _init_()
    _fill_color_ = _rgbtohex_(r, g, b)    
    
def noFill():
    global _fill_color_
    if _root_ is None: _init_()
    _fill_color_ = None

def stroke(r, g=None, b=None):
    global _line_color_
    if _root_ is None: _init_()
    _line_color_ = _rgbtohex_(r, g, b)
    
def strokeWeight(w):
    global _line_width_
    if _root_ is None: _init_()
    _line_width_ = w

def noStroke():
    global _line_width_
    if _root_ is None: _init_()
    _line_width_ = 0

def background(r, g=None, b=None):
    if _root_ is None: _init_()
    _c_.delete('all')
    _c_.config(bg=_rgbtohex_(r, g, b))

def image(img, x, y, w=None, h=None):
    if _root_ is None: _init_()
    if w is None or h is None:
        w = img.width
        h = img.height
    else:
        # print(w/img.width, h/img.height)
        img.zoom(w/img.width, h/img.height)
        img.width = w
        img.height = h
    _c_.create_image(x + w/2, y + h/2, image=img)

# from PIL import Image, ImageTk as _Image_, _ImageTk_
def loadImage(file):
    if _root_ is None: _init_()
    img = _tk_.PhotoImage(file=file)
    # img = _Image_.open(file)
    # return _ImageTk_.PhotoImage(img)
    img.width = img.width()
    img.height = img.height()
    return img

def mouseX():
    return _mouseX_
def mouseY():
    return _mouseY_
def mouseButton():
    return _mouseButton_

# Utilities
def dist(x1, y1, x2, y2):
    d2 = (x1-x2)**2+(y1-y2)**2
    return d2**0.5 # square root

