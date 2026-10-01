import io
import wave
import struct
import base64
import math
from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")


def now_ist():
    """Current date & time in Indian Standard Time, regardless of server location."""
    return datetime.now(IST)


def parse_time_str(t):
    """Try to parse a reminder time string in common formats. Returns a time object or None."""
    t = t.strip()
    formats = ["%I:%M %p", "%I:%M%p", "%H:%M", "%I %p", "%H.%M"]
    for fmt in formats:
        try:
            return datetime.strptime(t, fmt).time()
        except ValueError:
            continue
    return None


def minutes_until(reminder_time):
    """Returns how many minutes from now (IST) until the reminder time (negative if already passed)."""
    now = now_ist()
    reminder_dt = now.replace(hour=reminder_time.hour, minute=reminder_time.minute, second=0, microsecond=0)
    diff = (reminder_dt - now).total_seconds() / 60
    return diff


def is_due(reminder_time):
    """A reminder is 'due' if its time has already passed today, within the last 60 minutes."""
    diff = minutes_until(reminder_time)
    return diff <= 0 and diff > -60


def generate_beep_base64(duration=0.4, freq=880, volume=0.5, rate=44100):
    """Generates a short beep sound as a base64-encoded WAV string (no internet/files needed)."""
    n_samples = int(rate * duration)
    buf = io.BytesIO()
    wf = wave.open(buf, "w")
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(rate)
    frames = bytearray()
    for i in range(n_samples):
        value = int(volume * 32767 * math.sin(2 * math.pi * freq * i / rate))
        frames += struct.pack("<h", value)
    wf.writeframes(bytes(frames))
    wf.close()
    return base64.b64encode(buf.getvalue()).decode()
