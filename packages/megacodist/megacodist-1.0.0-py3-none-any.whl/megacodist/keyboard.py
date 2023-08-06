from enum import IntEnum, IntFlag


class Modifiers(IntFlag):
    """Specifies modifiers for Key event. The 'state' attribute of Key event
    is an integer (actually a bit mask) which every bit specifies a modifier
    such as Alt, Num Lock, Button-1 (left mouse button) ans so on.
    """
    SHIFT = 0x0001
    CAPS_LOCK = 0x0002
    CONTROL = 0x0004
    NUM_LOCK = 0x0008
    SCROLL_LOCK = 0x0020
    BUTTON_1 = 0x0100
    BUTTON_2 = 0x0200
    BUTTON_3 = 0x0400
    ALT = 0x20000


class KeyCodes(IntEnum):
    DELETE = 46
    A = 65
    B = 66
    I = 73
    K = 75
    L = 76
    N = 78
    O = 79
    P = 80
    S = 83
    U = 85
    V = 86
    F5 = 116