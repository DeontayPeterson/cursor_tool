from ctypes import windll, Structure, c_long, byref

class POINT(Structure):
    _fields_ = [('x', c_long), ('y', c_long)]


def get_cursor_pos():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y

