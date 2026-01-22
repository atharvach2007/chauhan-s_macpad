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

# -------------------------------------------------
# Keymap (row-major order)
# -------------------------------------------------
keyboard.keymap = [[
    KC.LCTRL,              KC.MEDIA_PLAY_PAUSE, KC.LALT,        # Row 1
    KC.MEDIA_REWIND,       KC.F11,               KC.MEDIA_FAST_FORWARD,  # Row 2
    KC.AUDIO_MUTE,         KC.UP,                KC.MEDIA_SUBTITLE,       # Row 3
    KC.LEFT,               KC.DOWN,              KC.RIGHT,               # Row 4
]]

# -------------------------------------------------
# Encoder gating keys (matrix indices)
# -------------------------------------------------
ENC_BRIGHTNESS_KEY = 0   # (Row 1, Col 1)
ENC_VOLUME_KEY     = 2   # (Row 1, Col 3)

# -------------------------------------------------
# Encoder setup (A/B shared)
# -------------------------------------------------
encoder = EncoderHandler()
encoder.pins = (
    (board.GP26, board.GP0),
)

def enc_cw(keyboard):
    if keyboard.key_states[ENC_BRIGHTNESS_KEY]:
        keyboard.tap_key(KC.BRIGHTNESS_UP)
    elif keyboard.key_states[ENC_VOLUME_KEY]:
        keyboard.tap_key(KC.VOLU)

def enc_ccw(keyboard):
    if keyboard.key_states[ENC_BRIGHTNESS_KEY]:
        keyboard.tap_key(KC.BRIGHTNESS_DOWN)
    elif keyboard.key_states[ENC_VOLUME_KEY]:
        keyboard.tap_key(KC.VOLD)

encoder.map = [
    (enc_cw, enc_ccw),
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
