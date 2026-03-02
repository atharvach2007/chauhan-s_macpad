import board
import busio
import adafruit_ssd1306
import adafruit_framebuf
import time
import rtc
import supervisor
import json
import sys

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.mouse_keys import MouseKeys


i2c = busio.I2C(board.D5, board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C)
buf = bytearray(32)
fb = adafruit_framebuf.FrameBuffer(buf, 32, 8, adafruit_framebuf.MVLSB)


def draw_scaled_text(text, x, y, scale=1):
    fb.fill(0)
    fb.text(text, 0, 0, 1)
    char_w = len(text) * 8
    for px in range(char_w):
        for py in range(8):
            if fb.pixel(px, py):
                for sx in range(scale):
                    for sy in range(scale):
                        nx = x + (px * scale) + sx
                        ny = y + (py * scale) + sy
                        if 0 <= nx < 128 and 0 <= ny < 32:
                            display.pixel(nx, ny, 0)


def show_panda():
    display.fill(1)
    draw_scaled_text("PANDA", 22, 6, scale=3)
    display.show()


class ClockDisplay:
    def __init__(self):
        self.display = display
        self.fb = fb
        self._last_second = -1
        self._synced = False
        self._serial_buf = ""
        self._r = rtc.RTC()
        show_panda()

    def _draw_rotated_text(self, text, x, y, scale=1):
        self.fb.fill(0)
        self.fb.text(text, 0, 0, 1)
        char_w = len(text) * 8
        for px in range(char_w):
            for py in range(8):
                if self.fb.pixel(px, py):
                    for sx in range(scale):
                        for sy in range(scale):
                            nx = x + (py * scale) + sx
                            ny = y + ((char_w - 1 - px) * scale) + sy
                            if 0 <= nx < 128 and 0 <= ny < 32:
                                self.display.pixel(nx, ny, 1)

    def _try_sync(self):
        if supervisor.runtime.serial_bytes_available:
            char = sys.stdin.read(1)
            if char == '\n':
                try:
                    t = json.loads(self._serial_buf.strip())
                    self._r.datetime = time.struct_time(
                        (t[0], t[1], t[2], t[3], t[4], t[5], t[6], -1, -1)
                    )
                    self._synced = True
                except:
                    pass
                self._serial_buf = ""
            else:
                self._serial_buf += char

    def during_bootup(self, keyboard): pass

    def before_matrix_scan(self, keyboard):
        if not self._synced:
            self._try_sync()
            return

        now = time.localtime()
        second = now.tm_sec
        if second != self._last_second:
            self._last_second = second
            hour = now.tm_hour
            minute = now.tm_min
            period = "AM"
            if hour >= 12:
                period = "PM"
            hour = hour % 12
            if hour == 0:
                hour = 12
            self.display.fill(0)
            self._draw_rotated_text("{:02d}".format(hour),   16, -16, scale=3)
            self._draw_rotated_text("{:02d}".format(minute), 42, -16, scale=3)
            self._draw_rotated_text("{:02d}".format(second), 68,  -5, scale=2)
            self._draw_rotated_text(period,                  88,   6, scale=1)
            self.display.show()

    def after_matrix_scan(self, keyboard): pass
    def before_hid_send(self, keyboard): pass
    def after_hid_send(self, keyboard): pass
    def on_powersave_enable(self, keyboard): pass
    def on_powersave_disable(self, keyboard): pass


keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(ClockDisplay())
keyboard.modules.append(MouseKeys())


keyboard.row_pins = (board.D7, board.D8, board.D9, board.D10)
keyboard.col_pins = (board.D1, board.D2, board.D3)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymap = [
    [
        KC.LALT, KC.LCTRL,  KC.AUDIO_MUTE,
        KC.LALT(KC.S),    KC.LALT(KC.X),    KC.TAB,
        KC.MB_LMB,  KC.UP,  KC.MB_RMB,
        KC.LEFT, KC.DOWN, KC.RIGHT,
    ]
]

encoder = EncoderHandler()
encoder.pins = ((board.D0, board.D6, None),)
encoder.map = [[(KC.VOLU, KC.VOLD)]]
keyboard.modules.append(encoder)

if __name__ == '__main__':
    keyboard.go()
