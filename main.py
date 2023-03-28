from temp.screencap import Screencap
from temp.pointer import get_cursor_pos
from tkinter import *
from PIL import ImageGrab, ImageTk, Image
import numpy as np
import cv2 as cv
from test import crop_image, crop_image_v2
from temp.mouse_logic import get_region_limits
# from cropgui import CursorCrop


class Mainwindow():

    def __init__(self, main: Tk):
        
        
        self.top_left = ''
        self.bottom_right = ''

        self.var_name = StringVar()

        self.image = ImageGrab.grab()
        self.temp_image = ''

        self.mouse = ImageGrab.grab()
        self.temp_mouse =''


        main.title('Crop assistant')
        main.config(width=500, height=500)
        main.wm_maxsize(width=500, height=500)
        main.wm_minsize(width=500, height=500)
        #def crop_image(x1, y1, x2, y2, np_img) -> ImageTk.PhotoImage:

        self.ss = np.array(ImageGrab.grab())
        self.cropped = crop_image(100,400,100,1000, self.ss)

        #CREATING CANVAS #DON'T ALTER ME PLEASE
        self.canvas = Canvas(root, width=250, height=250)
        self.current_ss = self.canvas.create_image(0, 0, anchor='nw', image=self.cropped)
        self.canvas.grid(row=0, column=0, sticky='w' )

        self.canvas1 = Canvas(root, width=100, height=100)
        self.mouse_ss = self.canvas1.create_image(100,0, anchor='e', image=ImageTk.PhotoImage(self.mouse))
        self.canvas1.grid(row=0,column=2, sticky='w')

        #CREATING FRAME
        self.frame = Frame(main)

        #X,Y Labels (These will be updated to show users current mouse location)
        self.x_label = Label(self.frame)
        self.y_label = Label(self.frame)
        self.x_label.grid(row=0, column=0, sticky='w')
        self.y_label.grid(row=1, column=0, sticky='w')

        #Top left and top right corners of the sub-region.
        self.TL_label = Label(self.frame, text=f"TL: {self.top_left}", font=('Arial', 20))
        self.BR_label = Label(self.frame, text=f"BR: {self.bottom_right}", font=('Arial', 20))
        self.TL_label.grid(row=0, column=1, sticky='w')
        self.BR_label.grid(row=1, column=1, sticky='w')

        #Variable Label and Entry field.
        self.var_label = Label(self.frame, text="Variable name: ", font=('Arial', 15))
        self.var_label.grid(row=2, column=0, sticky='w')
        self.var_entry = Entry(self.frame, bg='yellow', textvariable=self.var_name)
        self.var_entry.grid(row=2, column=1, sticky='w')

        #Area where code will be generated.
        self.code_area = Text(self.frame, width=20, height=3, background='yellow', padx=10)
        self.code_area.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky='w')

        #Button to clear TL&BR as well as Field where code is generated.
        self.reset_button = Button(self.frame, text='Reset')
        self.reset_button.grid(row=4, column=1, sticky='w')

        #Generate code that will crop the subregion the user has selected.
        self.generate_button = Button(self.frame, text='Generate', command=self.generate_sub) #Command
        self.generate_button.grid(row=4, column=0, sticky='w')

        self.test_button = Button(self.frame, text='Test!', command=lambda: self.update_image(self.image))
        self.test_button.grid(row=4, column=2, sticky='w', )
        self.frame.grid(row=1, column=0)
        
        
        #aa
        main.bind("<r>", self.key_pressed_BR)
        main.bind("<e>", self.key_pressed_TL)
        self.update_xy()
        self.update_zoomed_mouse(self.mouse)
    def key_pressed_BR(self, event):
        self.BR_label.config(text=f"{get_cursor_pos()}")

    def key_pressed_TL(self, event):
        self.TL_label.config(text=f"{get_cursor_pos()}")

        
    def generate_sub(self) -> None:
        '''
        Inserts a string of code into a Text field, the code will slice an array, cropping cropping a sub region of the array.
        '''
        tl = self.TL_label.cget('text')
        br = self.BR_label.cget('text')

        if not tl or not br:
            return ## Alert that they need to select a region before generating.

        tl = tl.strip(')(').split(',')
        br = br.strip(")(").split(',')

        tl  = (int(tl[0]), int(tl[1]))
        br = (int(br[0]), int(br[1]))
        v_name = self.var_name.get()

        code = f"{v_name} = screenshot[{tl[1]}:{br[1]}, {tl[0]}:{br[0]}]"
        self.code_area.insert('1.0', code)


    def get_text_fields(self) -> tuple:
        tl = self.TL_label.cget('text')
        br = self.BR_label.cget('text')
        
        if tl != "TL: " and br != "BR: ":

            tl = tl.strip(')(').split(',')
            br = br.strip(")(").split(',')

            tl  = (int(tl[0]), int(tl[1]))
            br = (int(br[0]), int(br[1]))
            return (tl, br)
        else:
            return None



    def update_zoomed_mouse(self, img):
        self.mouse = ImageGrab.grab()
        zoomed = get_region_limits(coords=get_cursor_pos(), im=img)
        zoomed = ImageTk.PhotoImage(image=zoomed)
        self.temp_mouse = zoomed

        self.canvas1.itemconfig(self.mouse_ss, image=self.temp_mouse)

        root.after(10, self.update_zoomed_mouse, self.mouse)



    def update_image(self, img):
        self.image = ImageGrab.grab()
        check = self.get_text_fields()
        tl, br = check[0], check[1]

        ss = img
        p_image_cropped = crop_image_v2(tl, br, ss)
        self.temp_image = p_image_cropped

        self.canvas.itemconfig(self.current_ss, image=self.temp_image)
        

    #DON'T TOUCH, WORKS 
    def update_xy(self) -> None:
        '''
        Updates X&Y label, with mouses current location.
        '''
        x, y = get_cursor_pos()
        self.x_label.config(text=f"X: {x}", font=('Arial', 20))
        self.y_label.config(text=f"Y: {y}", font=('Arial', 20))

        root.after(10, func=self.update_xy)

    
root = Tk()
x = Mainwindow(root)
root.mainloop()

