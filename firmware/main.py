import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.oled import Oled, OledMode

keyboard = KMKKeyboard()

# -------------------------------------------------
# Matrix (4 rows x 3 columns)
# -------------------------------------------------
keyboard.row_pins = (
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
)

keyboard.col_pins = (
    board.GP27,
    board.GP28,
    board.GP29,
)

keyboard.diode_orientation = keyboard.DIODE_COL2ROW

# -------------------------------------------------
# Keymap (row-major)
# -------------------------------------------------
keyboard.keymap = [[
    KC.LCTRL,          KC.LALT,               KC.AUDIO_MUTE,      # Row 1
    KC.MEDIA_SUBTITLE, KC.MEDIA_PLAY_PAUSE,   KC.F11,             # Row 2
    KC.PGUP,           KC.UP,                 KC.PGDN,            # Row 3
    KC.LEFT,           KC.DOWN,               KC.RIGHT,           # Row 4
]]

# -------------------------------------------------
# Encoder (volume control)
# -------------------------------------------------
encoder = EncoderHandler()
encoder.pins = (
    (board.GP26, board.GP0),
)

encoder.map = [
    (
        KC.VOLU,   # Clockwise
        KC.VOLD,   # Counter-clockwise
    ),
]

keyboard.modules.append(encoder)

# -------------------------------------------------
# OLED (vertical)
# -------------------------------------------------
oled = Oled(
    sda=board.GP6,
    scl=board.GP7,
    width=128,
    height=32,
    rotation=270,
    mode=OledMode.TEXT
)

keyboard.modules.append(oled)

def oled_task(oled, keyboard):
    oled.clear()
    oled.write("Panda\nwas\nHere")

oled.task = oled_task

# -------------------------------------------------
# Start
# -------------------------------------------------
if __name__ == "__main__":
    keyboard.go()
