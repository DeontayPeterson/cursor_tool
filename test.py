from PIL import ImageGrab, ImageTk, Image
from temp.pointer import get_cursor_pos

import cv2 as cv
import numpy as np


'''
def crop_image(tl: tuple, br: tuple, np_img: np) -> ImageTk.PhotoImage:
cropped = np_img[tl[1]:br[1], tl[2]:br[2]]
Change function below after testing..
'''


##TODO*************************************************************************
def crop_image(x1, y1, x2, y2, np_img) -> ImageTk.PhotoImage:
    cropped = np_img[x1:y1, x2:y2]
    pil_img = Image.fromarray(cropped)
    photo_image = ImageTk.PhotoImage(pil_img)
    return photo_image
tl = (100,100)
br = (1000,400)
#100,400,100,1000
#tl[y] = 100 ||| br[y] = 400 ||| tl[x] = 100, br[x] = 1000

def crop_image_v2(TL, BR, img):

    img = np.array(img)
    cropped = img[TL[1]:BR[1], TL[0]:BR[0]]

    p_img = Image.fromarray(cropped)
    photo_image = ImageTk.PhotoImage(p_img)
    return photo_image


def get_subregion_code(top_left: tuple, bottom_right: tuple) -> str:
    '''
    Returns a string containing relevant code to crop a subregion out of a numpy array.

    params: 'top_left' (x,y) top left box of the region that you want to capture
            'bottom_right' (x,y) bottom right coordinates for the box of the region that you want to capture
    '''
    #queue_position = screenshot[self.user_queue_position_TL[1]:self.user_queue_position_BR[1], self.user_queue_position_TL[0]:self.user_queue_position_BR[0]]

    code = f"sub_region = screenshot[{top_left[1]}:{bottom_right[1]}, {top_left[0]}:{bottom_right[0]}]"
    return code


##TODO: *************************************************************************
def area_around_mouse():
    mouse_x, mouse_y = get_cursor_pos()

    if 1930 > mouse_x > 50:
        pass
        

if __name__ == '__main__':
    ss = ImageGrab.grab()
    ss = np.array(ss)

    cropped_version = ss[100:500, 100:500]
    cropped_version = cv.cvtColor(cropped_version, cv.COLOR_BGR2RGB)

    pil_form = Image.fromarray(cropped_version)
