"""Original background music and sound design for the Anjum Mart reels (synthesised here, so there is no copyright claim).

Usage:  python3 make_music.py <plan.json> <out.wav>

The plan (plans/<id>.json) gives: duration (s), bpm, style ('gold', 'noir' or 'pulse') and cues, a list of
[time_s, kind] sound-design hits that line up with the pictures: 'whoosh', 'boom', 'tick', 'chime', 'riser', 'sparkle'.
All sounds are built from sine / band-limited oscillators, filtered noise and a synthetic room reverb.
"""
import json
import sys

import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 44100
RNG = np.random.default_rng(1111)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def lowpass(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR / 2), 'low')
    return signal.lfilter(b, a, x)


def highpass(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR / 2), 'high')
    return signal.lfilter(b, a, x)


def bandpass(x, lo, hi, order=2):
    b, a = signal.butter(order, [lo / (SR / 2), hi / (SR / 2)], 'band')
    return signal.lfilter(b, a, x)


def env(n, attack, release, curve=2.0):
    e = np.ones(n)
    a = int(attack * SR)
    r = int(release * SR)
    if a > 0:
        e[:a] = np.linspace(0, 1, min(a, n)) ** curve
    if r > 0:
        r = min(r, n)
        e[-r:] *= np.linspace(1, 0, r) ** curve
    return e


def decay(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def osc_saw(f, n, harmonics=10):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for k in range(1, harmonics + 1):
        if f * k > 9000:
            break
        out += np.sin(2 * np.pi * f * k * t + k) / k
    return out * (2 / np.pi)


def place(buf, sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= buf.shape[1]:
        return
    if i < 0:
        sig = sig[-i:]
        i = 0
    n = min(len(sig), buf.shape[1] - i)
    if n <= 0:
        return
    l = gain * np.cos((pan + 1) * np.pi / 4)
    r = gain * np.sin((pan + 1) * np.pi / 4)
    buf[0, i:i + n] += sig[:n] * l
    buf[1, i:i + n] += sig[:n] * r


# ---- instruments -------------------------------------------------------------------------------------------------
def pad(notes, dur, bright=1200):
    n = int(dur * SR)
    out = np.zeros(n)
    for m in notes:
        f = midi(m)
        for det in (-0.004, 0.0, 0.004):
            out += osc_saw(f * (1 + det), n, 14)
    out = lowpass(out, bright, 2)
    return out * env(n, 0.9, 1.1) / (len(notes) * 3)


def bass(note, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = midi(note)
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return x * env(n, 0.01, 0.12) * decay(n, 0.5)


def kick(soft=1.0):
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 48 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * decay(n, 0.11) * soft


def hat(open_=False):
    n = int((0.22 if open_ else 0.06) * SR)
    x = highpass(RNG.standard_normal(n), 7000, 2)
    return x * decay(n, 0.05 if open_ else 0.014)


def clap():
    n = int(0.25 * SR)
    x = bandpass(RNG.standard_normal(n), 1100, 3200, 2)
    e = decay(n, 0.07)
    for k in (0.0, 0.012, 0.024):
        j = int(k * SR)
        e[j:j + 80] += 1.2
    return x * e * 0.8


def pluck(note, tau=0.22, bright=3500):
    n = int(1.2 * SR)
    t = np.arange(n) / SR
    f = midi(note)
    x = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * 2 * f * t) + 0.2 * np.sin(2 * np.pi * 3 * f * t)
    x = lowpass(x, bright, 2)
    return x * decay(n, tau) * env(n, 0.003, 0.05)


def bell(note, tau=1.4):
    n = int(3.2 * SR)
    t = np.arange(n) / SR
    f = midi(note)
    x = np.zeros(n)
    for ratio, amp, tt in ((1, 1.0, 1.0), (2.76, 0.5, 0.7), (5.4, 0.3, 0.45), (8.93, 0.15, 0.3)):
        x += amp * np.sin(2 * np.pi * f * ratio * t) * decay(n, tau * tt)
    return x * env(n, 0.002, 0.2)


def whoosh(dur=0.9):
    n = int(dur * SR)
    x = RNG.standard_normal(n)
    out = np.zeros(n)
    steps = 24
    seg = n // steps
    for i in range(steps):
        a, b = i * seg, (i + 1) * seg if i < steps - 1 else n
        fc = 300 * (14 ** (i / (steps - 1)))
        out[a:b] = lowpass(x[a:b], min(fc, 14000), 2)
    e = np.linspace(0, 1, n) ** 2.2
    tail = int(0.12 * SR)
    e[-tail:] *= np.linspace(1, 0, tail)
    return out * e * 1.4


def riser(dur=2.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 180 * (10 ** (t / dur))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = 0.35 * np.sin(ph) + 0.12 * RNG.standard_normal(n)
    x = highpass(x, 400, 2)
    return x * (np.linspace(0, 1, n) ** 2) * env(n, 0, 0.02)


def boom():
    n = int(2.2 * SR)
    t = np.arange(n) / SR
    f = 34 + 70 * np.exp(-t * 9)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * decay(n, 0.7)
    burst = lowpass(RNG.standard_normal(n), 900, 2) * decay(n, 0.09) * 0.8
    return (x + burst) * env(n, 0.002, 0.3)


def tick():
    n = int(0.08 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1900 * t) * decay(n, 0.012) * 0.6


def sparkle():
    out = np.zeros(int(1.4 * SR))
    for k, m in enumerate((88, 91, 95, 100, 103)):
        s = bell(m, 0.35)[:len(out)]
        out[int(k * 0.06 * SR):] += s[:len(out) - int(k * 0.06 * SR)] * 0.5
    return out


def reverb(stereo, wet=0.28, tau=0.9, length=2.4):
    n = int(length * SR)
    t = np.arange(n) / SR
    out = np.zeros_like(stereo)
    for ch in range(2):
        ir = RNG.standard_normal(n) * np.exp(-t / tau)
        ir = lowpass(ir, 6500, 2)
        ir[: int(0.018 * SR)] *= 0.2
        ir /= np.sqrt(np.sum(ir ** 2)) / 5
        out[ch] = signal.fftconvolve(stereo[ch], ir)[: stereo.shape[1]]
    return stereo * (1 - wet * 0.6) + out * wet


# ---- arrangement -------------------------------------------------------------------------------------------------
PROG = [
    ([57, 60, 64, 67], 45),   # Am7   bass A
    ([53, 57, 60, 64], 41),   # Fmaj7 bass F
    ([48, 55, 60, 64], 48),   # C     bass C
    ([55, 59, 62, 66], 43),   # G     bass G
]
ARP = {
    'gold': [0, 2, 1, 3, 2, 1, 3, 2],
    'noir': [0, 3, 2, 3, 1, 3, 2, 3],
    'pulse': [0, 1, 2, 3, 2, 1, 2, 3],
}


def compose(plan):
    dur = plan['duration']
    bpm = plan['bpm']
    style = plan.get('style', 'gold')
    beat = 60.0 / bpm
    bar = beat * 4
    n = int(dur * SR)
    buf = np.zeros((2, n))
    bars = int(np.ceil(dur / bar))
    kick_from = plan.get('kick_from', bar * 1.0)
    for b in range(bars):
        t0 = b * bar
        notes, root = PROG[b % 4]
        place(buf, pad([m for m in notes], min(bar + 1.2, dur - t0 + 1.2), 1800 + 900 * (b / max(1, bars))), t0, 0.42 if style != 'noir' else 0.5)
        place(buf, pad([m + 12 for m in notes[1:]], min(bar + 1.2, dur - t0 + 1.2), 4200), t0, 0.16, pan=0.2)
        if t0 >= 0:
            place(buf, bass(root, bar), t0, 0.2 if style == 'gold' else 0.14)
        # arpeggio, louder as the track builds
        pat = ARP[style]
        step = beat / 2
        for k in range(8):
            tt = t0 + k * step
            if tt < bar * 0.5 and b == 0:
                continue
            note = notes[pat[k] % len(notes)] + (12 if style != 'gold' else 12)
            level = 0.34 + 0.16 * min(1.0, b / 3)
            place(buf, pluck(note, 0.22 if style != 'noir' else 0.45, 6000), tt, level, pan=((k % 4) - 1.5) * 0.3)
        if tt >= 0 and style == 'noir' and b % 2 == 1:
            place(buf, bell(notes[2] + 24, 1.6), t0 + beat * 2, 0.2, pan=0.3)
        # drums
        if t0 + 1e-6 >= kick_from and style in ('gold', 'pulse'):
            for k in range(4):
                tt = t0 + k * beat
                if style == 'pulse' or k in (0, 2):
                    place(buf, kick(0.9), tt, 0.4)
                if k % 2 == 1:
                    place(buf, clap(), tt, 0.3)
            for k in range(8):
                place(buf, hat(k % 4 == 3), t0 + k * beat / 2, 0.2 if k % 2 else 0.12, pan=0.35)
        elif style == 'noir' and t0 + 1e-6 >= kick_from:
            place(buf, kick(0.6), t0, 0.22)
            place(buf, tick(), t0 + beat * 1.5, 0.22, pan=-0.4)
            place(buf, tick(), t0 + beat * 3.5, 0.18, pan=0.4)
    # sound design on the picture cues
    for t, kind in plan.get('cues', []):
        if kind == 'whoosh':
            place(buf, whoosh(0.9), t - 0.8, 0.22, pan=-0.2)
        elif kind == 'boom':
            place(buf, boom(), t, 0.3)
        elif kind == 'tick':
            place(buf, tick(), t, 0.35)
        elif kind == 'chime':
            place(buf, bell(88, 1.6), t, 0.3, pan=0.2)
            place(buf, bell(95, 1.2), t + 0.09, 0.2, pan=-0.2)
        elif kind == 'riser':
            place(buf, riser(1.8), t - 1.8, 0.35)
        elif kind == 'sparkle':
            place(buf, sparkle(), t, 0.16)
    buf = reverb(buf, 0.24 if style == 'gold' else 0.32)
    # master: gentle compression, fades, level
    buf = np.tanh(buf * 1.1) / 1.1
    fade = int(0.9 * SR)
    buf[:, -fade:] *= np.linspace(1, 0, fade) ** 1.6
    buf[:, :int(0.015 * SR)] *= np.linspace(0, 1, int(0.015 * SR))
    peak = np.max(np.abs(buf)) or 1.0
    buf = buf / peak * 0.89
    return buf


def main():
    plan = json.load(open(sys.argv[1]))
    buf = compose(plan)
    pcm = (buf.T * 32767).astype(np.int16)
    wavfile.write(sys.argv[2], SR, pcm)
    print('wrote', sys.argv[2], round(plan['duration'], 2), 's')


if __name__ == '__main__':
    main()
