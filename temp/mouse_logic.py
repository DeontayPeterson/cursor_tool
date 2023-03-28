import numpy as np
import keyboard
import time
import cv2 as cv
from temp.pointer import get_cursor_pos
from PIL import Image, ImageGrab

#        queue_position = screenshot[self.user_queue_position_TL[1]:self.user_queue_position_BR[1], self.user_queue_position_TL[0]:self.user_queue_position_BR[0]]

def get_region_limits(coords: tuple, im: Image) -> Image:
    x,y = coords[0], coords[1]
    
    lower_x = x - 50
    upper_x = x + 50
    lower_y = y - 50
    upper_y = y + 50

    if x <= 50:
        lower_x = 0
    elif x >= 1870:
        upper_x = 1870

    if y <= 50:
        lower_y = 0
    elif y >= 1030:
        upper_y = 1030
    # im = ImageGrab.grab()
    

    #left, upper, right, lower
    zoomed = im.crop((lower_x, lower_y, upper_x, upper_y))
    zoomed = np.array(zoomed)
    zoomed = Image.fromarray(zoomed)
    return zoomed




if __name__ == "__main__":
    while True:
        
        cropped = get_region_limits(get_cursor_pos())
        cv.imshow('hello', cropped)
        
        waitkey = cv.waitKey(1)

        if waitkey == ord('q'):
            cv.destroyAllWindows()


        if keyboard.is_pressed('e'):
            quit()