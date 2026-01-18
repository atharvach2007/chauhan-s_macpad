import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.oled import Oled, OledMode

keyboard = KMKKeyboard()

# -----------------------
# Matrix
# -----------------------
keyboard.row_pins = (
    board.GP1,   # Row 1
    board.GP2,   # Row 2
    board.GP3,   # Row 3
    board.GP4,   # Row 4
)

keyboard.col_pins = (
    board.GP27,  # Col 1
    board.GP28,  # Col 2
    board.GP29,  # Col 3
)

keyboard.diode_orientation = keyboard.DIODE_COL2ROW

# -----------------------
# Keymap
# -----------------------
keyboard.keymap = [
    [
        KC.LCTRL,              KC.MEDIA_PLAY_PAUSE, KC.LALT,        # Row 1
        KC.MEDIA_REWIND,       KC.F11,               KC.MEDIA_FAST_FORWARD,  # Row 2
        KC.AUDIO_MUTE,         KC.UP,                KC.MEDIA_SUBTITLE,       # Row 3
        KC.LEFT,               KC.DOWN,              KC.RIGHT,               # Row 4
    ]
]

# -----------------------
# Encoders
# -----------------------
encoder = EncoderHandler()

encoder.pins = (
    (board.GP26, board.GP0),  # Encoder A & B
)

encoder.map = [
    (
        KC.BRIGHTNESS_UP,     # Encoder A CW
        KC.BRIGHTNESS_DOWN,   # Encoder A CCW
    ),
    (
        KC.VOLU,              # Encoder B CW
        KC.VOLD,              # Encoder B CCW
    ),
]

keyboard.modules.append(encoder)

# -----------------------
# OLED
# -----------------------
oled = Oled(
    sda=board.GP6,
    scl=board.GP7,
    width=128,
    height=32,
    rotation=270,     # vertical
    mode=OledMode.TEXT
)

keyboard.modules.append(oled)

def oled_task(oled, keyboard):
    oled.clear()
    oled.write("Panda\nwas\nHere")

oled.task = oled_task

if __name__ == '__main__':
    keyboard.go()