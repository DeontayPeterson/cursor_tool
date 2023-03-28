from temp.screencap import Screencap
from temp.pointer import get_cursor_pos
from tkinter import *
from PIL import ImageGrab, ImageTk, Image
import numpy as np
import cv2 as cv
from test import crop_image, crop_image_v2
# from cropgui import CursorCrop


top_left = ''
bottom_right = ''



##CREATING WINDOW
window = Tk()
var_name = StringVar()


window.title('Crop assistant')
window.config(width=500, height=500)
window.wm_maxsize(width=500, height=500)
window.wm_minsize(width=500, height=500)
#def crop_image(x1, y1, x2, y2, np_img) -> ImageTk.PhotoImage:

ss = np.array(ImageGrab.grab())
cropped = crop_image(100,400,100,1000, ss)

#CREATING CANVAS
canvas = Canvas(window, width=250, height=250)
current_ss = canvas.create_image(0, 0, anchor='nw', image=cropped)
canvas.grid(row=0, column=0, sticky='w' )

#CREATING FRAME
frame = Frame(window)

#X,Y Labels (These will be updated to show users current mouse location)
x_label = Label(frame)
y_label = Label(frame)
x_label.grid(row=0, column=0, sticky='w')
y_label.grid(row=1, column=0, sticky='w')

#Top left and top right corners of the sub-region.
TL_label = Label(frame, text=f"TL: {top_left}", font=('Arial', 20))
BR_label = Label(frame, text=f"BR: {bottom_right}", font=('Arial', 20))
TL_label.grid(row=0, column=1, sticky='w')
BR_label.grid(row=1, column=1, sticky='w')

#Variable Label and Entry field.
var_label = Label(frame, text="Variable name: ", font=('Arial', 15))
var_label.grid(row=2, column=0, sticky='w')
var_entry = Entry(frame, bg='yellow', textvariable=var_name)
var_entry.grid(row=2, column=1, sticky='w')

#Area where code will be generated.
code_area = Text(frame, width=20, height=3, background='yellow', padx=10)
code_area.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky='w')

#Button to clear TL&BR as well as Field where code is generated.
reset_button = Button(frame, text='Reset')
reset_button.grid(row=4, column=1, sticky='w')

def generate_sub() -> None:
    '''
    Inserts a string of code into a Text field, the code will slice an array, cropping cropping a sub region of the array.
    '''
    tl = TL_label.cget('text')
    br = BR_label.cget('text')

    if not tl or not br:
        return ## Alert that they need to select a region before generating.

    tl = tl.strip(')(').split(',')
    br = br.strip(")(").split(',')

    tl  = (int(tl[0]), int(tl[1]))
    br = (int(br[0]), int(br[1]))
    v_name = var_name.get()

    code = f"{v_name} = screenshot[{tl[1]}:{br[1]}, {tl[0]}:{br[0]}]"
    code_area.insert('1.0', code)


def get_text_fields() -> tuple:
    tl = TL_label.cget('text')
    br = BR_label.cget('text')
    
    if tl != "TL: " and br != "BR: ":

        tl = tl.strip(')(').split(',')
        br = br.strip(")(").split(',')

        tl  = (int(tl[0]), int(tl[1]))
        br = (int(br[0]), int(br[1]))
        return (tl, br)
    else:
        return None


##TODO*************************************************************************
def update_image():
    check = get_text_fields()
    if check:
        tl = check[0]
        br = check[1]
        ss = ImageGrab.grab()
        to_display = crop_image_v2(tl, br, ss)

        # canvas.itemconfig(current_ss, anchor='nw', image=to_display)
        image_on_canvas = canvas.create_image(0,0, anchor='nw', image=to_display)
        # canvas.configure(image_on_canvas, image=to_display)
        canvas.configure( image=to_display)
        
        


#Generate code that will crop the subregion the user has selected.
generate_button = Button(frame, text='Generate', command=generate_sub ) #Command
generate_button.grid(row=4, column=0, sticky='w')

test_button = Button(frame, text='Test!', command=lambda: update_image())
test_button.grid(row=4, column=2, sticky='w', )


def key_pressed_TL(event):
    TL_label.config(text=f"{get_cursor_pos()}")

window.bind("<e>", key_pressed_TL)

def key_pressed_BR(event):
    BR_label.config(text=f"{get_cursor_pos()}")

window.bind("<r>", key_pressed_BR)












frame.grid(row=1, column=0)

#DON'T TOUCH, WORKS 
def update_xy() -> None:
    '''
    Updates X&Y label, with mouses current location.
    '''
    x, y = get_cursor_pos()
    x_label.config(text=f"X: {x}", font=('Arial', 20))
    y_label.config(text=f"Y: {y}", font=('Arial', 20))

    window.after(10, func=update_xy)

update_xy()

window.mainloop()

