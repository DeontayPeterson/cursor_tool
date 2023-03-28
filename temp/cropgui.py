from temp.screencap import Screencap
from pointer import get_cursor_pos
from tkinter import *



class CursorCrop(Tk):
    def __init__(self):
        self.xpos = ''
        self.ypos = ''
        self.TL = ''
        self.BR = ''
        self.var_name = ''
        
        super().__init__()
        
        CursorCrop.title(self, "Region Cropper")
        CursorCrop.configure(self, width=750, height=750)
        CursorCrop.wm_minsize(self, width=750, height=750)
        CursorCrop.wm_maxsize(self, width=750, height=750)

        #TL, BR, var_name, xpos, ypos LABELS

        self.top_left_label = Label(self, text=f'TL: {self.TL}')
        self.bottom_right_label = Label(self, text=f'BR: {self.BR}')

        self.var_name_label = Label(self, text='Variable Name:')

        self.x_label = Label(self, text=f'X: {self.xpos}')
        self.y_label = Label(self, text=f'Y: {self.ypos}')

        self.var_name_entry = Entry(self)
        

        app = Frame(CursorCrop)

        self.mainloop()

    @staticmethod
    def get_subregion_code(top_left: tuple, bottom_right: tuple) -> str:
        '''
        Returns a string containing relevant code to crop a subregion out of a numpy array.

        params: 'top_left' (x,y) top left box of the region that you want to capture
                'bottom_right' (x,y) bottom right coordinates for the box of the region that you want to capture
        '''
        #queue_position = screenshot[self.user_queue_position_TL[1]:self.user_queue_position_BR[1], self.user_queue_position_TL[0]:self.user_queue_position_BR[0]]

        code = f"sub_region = screenshot[{top_left[1]}:{bottom_right[1]}, {top_left[0]}:{bottom_right[0]}]"
        return code




