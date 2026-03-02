import serial
import serial.tools.list_ports
import json
import time


def find_xiao():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        desc = (p.description or '').lower()
        if 'usb serial device' in desc or 'usb serial' in desc:
            return p.device
    return None


def sync(port):
    time.sleep(3)
    now = time.localtime()
    payload = json.dumps([now.tm_year, now.tm_mon, now.tm_mday,
                          now.tm_hour, now.tm_min, now.tm_sec,
                          now.tm_wday]) + '\n'
    with serial.Serial(port, 115200, timeout=2) as s:
        time.sleep(1)
        s.write(payload.encode())
        time.sleep(0.5)
        s.write(b'SYNCED\n')
        print("Time synced:", time.strftime("%H:%M:%S", now))


last_port = None
print("Watching for board...")

while True:
    port = find_xiao()
    if port and port != last_port:
        try:
            sync(port)
            last_port = port
        except PermissionError:
            print("Port busy, retrying...")
            last_port = None
        except Exception as e:
            print("Sync failed:", e)
    if not port:
        last_port = None
    time.sleep(3)