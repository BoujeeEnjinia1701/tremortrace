"""TremorTrace sizing calculations for TRT-CAL-001.

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number that docs/04-calcs/01-sizing.md quotes. Research and
educational prototype, not a medical device.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))

G = 9.80665

# ---------------------------------------------------------------- assumptions
FS = 104.0            # IMU output data rate, Hz (LSM6DS3TR-C ODR setting)
WIN_S = 10.0          # summary window, s
BAND = (3.0, 15.0)    # tremor band, Hz
ACC_ND = 90e-6        # accelerometer noise density, g/sqrt(Hz) (ST datasheet, high-performance, +/-2 g)
GYR_ND = 5e-3         # gyroscope rate noise density, dps/sqrt(Hz) (ST datasheet, high-performance)
ODR_TOL = 0.02        # assumed IMU internal oscillator tolerance, fraction (not a datasheet figure; confirm)

WEAR_H = 16.0         # worn and recording, h per day (R4)
OFF_H = 24.0 - WEAR_H
CELL_MAH = 150.0      # Adafruit 1317 class protected LiPo
USABLE = 0.85 * 0.90  # 85 % above a 3.5 V firmware cutoff, times 90 % for ageing and cold

# Recording currents, mA: (nominal, conservative)
I_IMU = (0.90, 0.90)          # accel + gyro combo, high-performance (ST product page figure)
I_MCU_RUN = 6.3               # nRF52840 CPU running from flash at 64 MHz, LDO mode (assumed)
I_SLEEP = 0.005               # board standby, "less than 5 uA" (Seeed wiki)
I_BLE_ADV = (0.015, 0.10)     # advertising at 1 s interval so the owner can sync (assumed)
I_FLASH = (0.005, 0.02)       # QSPI flash writes and erases, averaged (assumed)
I_LED = (0.002, 0.01)         # 2 mA blink, 10 ms every 10 s (nominal)
I_PCM = (0.003, 0.005)        # cell protection circuit (assumed)
I_OFF = (0.05, 0.08)          # off-wrist: accel only at low rate for wear detection, plus BLE advertising
MCU_CONS = 0.50               # conservative MCU average, mA (untuned firmware)

# MCU duty from first principles (per 10 s window)
I2C_HZ = 400e3
BYTES_PER_SAMPLE = 12         # 6 axes x 16 bit
DSP_CYCLES = 6 * (1040 * 2 * 20 + 40_000 + 512 * 10) * 2   # 6 axes: filter, 1024-pt real FFT, magnitude; x2 overhead
WAKE_S = 10 * 0.5e-3          # 10 FIFO wakes per window at 0.5 ms each

RECORD_B = 32                 # bytes per 10 s summary record (layout in the note)
FLASH_B = 2 * 1024 * 1024     # 2 MB QSPI flash on the module; firmware lives in the nRF52840 internal flash
RAW_RESERVE_B = 256 * 1024    # reserved for on-demand raw snippets (decided: summaries plus optional raw)
FS_OVERHEAD = 0.03            # sector headers and wear levelling in a simple log store

CHARGE_MA = (50.0, 100.0)     # BQ25101 charge current settings on the module (Seeed wiki); 50 mA decided (TRT-DDR-002)
CELL_MAX_CHARGE_MA = 150.0    # Adafruit 1317 limit

DENS = {"PETG": 1.27, "TPU": 1.21}   # g/cm3
MASS_BOUGHT_G = {                    # g
    "Textile strap, 22 mm (assumed)": 8.0,
    "Controller and IMU module (assumed)": 3.0,
    "LiPo cell, 150 mAh (Adafruit 1317)": 4.65,
    "Charging connector receptacle (assumed)": 1.0,
    "Spring bars, 2 (assumed)": 0.6,
    "M2 x 6 countersunk screws, 4 (assumed)": 0.6,       # four, one per lug horn (TRT-DDR-003)
    "Wire, two foam pads, light pipe, epoxy (assumed)": 1.0,  # upper foam pad and epoxy added (TRT-DDR-003)
}


def hr(t):
    print("\n" + t + "\n" + "-" * len(t))


# ---------------------------------------------------------------- R1, R3: sampling and resolution
hr("R1, R3: sampling and frequency resolution")
N = int(FS * WIN_S)
df = FS / N
print(f"Samples per window N = {N}; bin spacing df = {df:.3f} Hz; Nyquist = {FS/2:.0f} Hz")
print(f"Band {BAND[0]:.0f} to {BAND[1]:.0f} Hz covers {int((BAND[1]-BAND[0])/df)} bins")
err_uncorr = BAND[1] * ODR_TOL
print(f"Uncorrected ODR tolerance {ODR_TOL*100:.0f} % gives up to {err_uncorr:.2f} Hz error at {BAND[1]:.0f} Hz")
print(f"With the sample rate measured against the 32.768 kHz crystal (20 ppm): {BAND[1]*20e-6*1000:.2f} mHz")

# ---------------------------------------------------------------- R2: amplitude range and noise floor
hr("R2: amplitude noise floor and full scale")
bw = BAND[1] - BAND[0]
acc_noise_mg = ACC_ND * 1000 * math.sqrt(bw)
gyr_noise = GYR_ND * math.sqrt(bw)
det_mg = 3 * acc_noise_mg
disp_um = det_mg / 1000 * G / (2 * math.pi * 5.0) ** 2 * 1e6
print(f"Accel noise in band: {acc_noise_mg:.2f} mg RMS; gyro noise in band: {gyr_noise:.3f} dps RMS")
print(f"Detection floor (3x noise): {det_mg:.2f} mg RMS, about {disp_um:.1f} um RMS displacement at 5 Hz")
cases = [(5.0, 20.0), (8.0, 10.0), (12.0, 5.0)]   # (Hz, peak displacement mm) for severe tremor
for f, x in cases:
    a_g = (2 * math.pi * f) ** 2 * x / 1000 / G
    print(f"Severe tremor {x:.0f} mm peak at {f:.0f} Hz: {a_g:.2f} g peak, plus 1 g gravity = {a_g+1:.2f} g")
for f, deg in [(6.0, 15.0), (8.0, 20.0)]:
    w = 2 * math.pi * f * deg
    print(f"Rotation +/-{deg:.0f} deg at {f:.0f} Hz: {w:.0f} dps peak")
print("Chosen ranges: accelerometer +/-8 g (0.244 mg/LSB), gyroscope +/-2000 dps (70 mdps/LSB)")

# ---------------------------------------------------------------- synthetic check of the window algorithm
hr("R1, R2: synthetic check of the 10 s window algorithm")
rng = np.random.default_rng(3)


def window_summary(sig, fs):
    n = len(sig)
    x = sig - sig.mean()
    w = np.hanning(n)
    spec = np.abs(np.fft.rfft(x * w)) ** 2
    f = np.fft.rfftfreq(n, 1 / fs)
    band = (f >= BAND[0]) & (f <= BAND[1])
    low = (f >= 0.3) & (f < BAND[0])
    k = np.argmax(np.where(band, spec, 0))
    a, b, c = np.log(spec[k - 1:k + 2])                      # parabolic peak interpolation
    fpk = f[k] + (a - c) / (2 * (a - 2 * b + c)) * (f[1] - f[0])
    xf = np.fft.irfft(np.where(band, np.fft.rfft(x), 0), n)  # band-limited RMS
    ratio = spec[band].sum() / max(spec[low].sum(), 1e-12)
    return fpk, float(np.sqrt(np.mean(xf ** 2))), ratio


t = np.arange(N) / FS
sig_noise = ACC_ND * math.sqrt(FS / 2) * G                  # per-sample noise, m/s2
worst_f, worst_a = 0.0, 0.0
print(" f true   f est    err     RMS true  RMS est  err %")
for f0 in (3.33, 4.77, 6.25, 9.14, 12.46, 14.61):   # off-bin frequencies
    amp_rms = 0.05                                          # m/s2 RMS, a mild tremor
    s = amp_rms * math.sqrt(2) * np.sin(2 * math.pi * f0 * t + rng.uniform(0, 6.28))
    s = s + rng.normal(0, sig_noise, N)
    fe, ae, _ = window_summary(s, FS)
    worst_f = max(worst_f, abs(fe - f0)); worst_a = max(worst_a, abs(ae - amp_rms) / amp_rms)
    print(f"{f0:6.2f}  {fe:6.3f}  {fe-f0:+6.3f}   {amp_rms:.4f}    {ae:.4f}   {100*(ae-amp_rms)/amp_rms:+5.1f}")
print(f"Worst frequency error {worst_f:.3f} Hz (target 0.2 Hz); worst amplitude error {100*worst_a:.1f} %")

hr("Activity flag: synthetic cases (indicative only)")
flag_ratio = 1.0
walk = np.zeros(N)
for k0 in np.arange(0, WIN_S, 0.55):                        # heel strikes at about 1.8 steps/s
    idx = int(k0 * FS)
    walk[idx:idx + 6] += 3.0 * np.hanning(6)
cases = {
    "Rest tremor, 5 Hz, 0.3 m/s2": 0.3 * math.sqrt(2) * np.sin(2 * math.pi * 5 * t),
    "Voluntary reach, 0.8 Hz, 1.5 m/s2": 1.5 * math.sqrt(2) * np.sin(2 * math.pi * 0.8 * t),
    "Walking arm swing plus heel strikes": 1.2 * np.sin(2 * math.pi * 0.9 * t) + walk,
    "Tremor 5 Hz during reach": 0.3 * math.sqrt(2) * np.sin(2 * math.pi * 5 * t)
                                + 1.5 * math.sqrt(2) * np.sin(2 * math.pi * 0.8 * t),
}
for name, s in cases.items():
    _, rms, ratio = window_summary(s + rng.normal(0, sig_noise, N), FS)
    print(f"{name:38s} band/low power ratio {ratio:9.2f}  -> {'tremor' if ratio > flag_ratio else 'activity'}")

# ---------------------------------------------------------------- R4: power budget
hr("R4: power budget")
i2c_s = N * BYTES_PER_SAMPLE * 9 / I2C_HZ
dsp_s = DSP_CYCLES / 64e6
duty = (i2c_s + dsp_s + WAKE_S) / WIN_S
i_mcu = I_MCU_RUN * duty + I_SLEEP
print(f"MCU active per window: I2C {i2c_s*1000:.0f} ms, DSP {dsp_s*1000:.0f} ms, wakes {WAKE_S*1000:.0f} ms; duty {duty*100:.2f} %")
print(f"MCU average {i_mcu:.3f} mA nominal; {MCU_CONS:.2f} mA conservative")
usable = CELL_MAH * USABLE
res = {}
for j, label in enumerate(("nominal", "conservative")):
    rec = I_IMU[j] + (i_mcu if j == 0 else MCU_CONS) + I_BLE_ADV[j] + I_FLASH[j] + I_LED[j] + I_PCM[j]
    sync = 184.32 / 10.0 / 3600 * 5.0            # 184 kB at 10 kB/s, 5 mA radio
    day = rec * WEAR_H + I_OFF[j] * OFF_H + sync
    res[label] = (rec, day, usable / day)
    print(f"{label:12s}: recording {rec:.3f} mA; off-wrist {I_OFF[j]:.3f} mA; {day:.1f} mAh per day; "
          f"{usable/day:.1f} days on {usable:.0f} mAh usable")
no_sleep = (I_IMU[0] + I_MCU_RUN) * WEAR_H + (I_MCU_RUN + 0.03) * OFF_H
print(f"Firmware that never sleeps: {no_sleep:.0f} mAh per day, {usable/no_sleep:.2f} days (fails R4)")
for c in CHARGE_MA:
    print(f"Charge at {c:.0f} mA: {c/CELL_MAH:.2f} C (cell limit {CELL_MAX_CHARGE_MA:.0f} mA), about "
          f"{CELL_MAH/c*1.2:.1f} h; linear charger loss about {(5.0-3.7)*c/1000*1000:.0f} mW")

# ---------------------------------------------------------------- R5: storage
hr("R5: on-band storage")
rec_day = WEAR_H * 3600 / WIN_S
b_day = rec_day * RECORD_B
avail = (FLASH_B - RAW_RESERVE_B) * (1 - FS_OVERHEAD)
raw_win = N * BYTES_PER_SAMPLE
print(f"{rec_day:.0f} records per day x {RECORD_B} B = {b_day/1000:.1f} kB per day")
print(f"Available after {RAW_RESERVE_B//1024} kB raw reserve and {FS_OVERHEAD*100:.0f} % overhead: {avail/1000:.0f} kB")
print(f"History: {avail/b_day:.1f} days at {WEAR_H:.0f} h per day; {avail/(b_day*24/WEAR_H):.1f} days if logging 24 h")
print(f"Raw 10 s window: {raw_win} B, so summaries are {raw_win/RECORD_B:.0f} times smaller")
print(f"Raw reserve holds {RAW_RESERVE_B//raw_win} raw 10 s snippets")

# ---------------------------------------------------------------- R6: size and mass
hr("R6: size and mass (from cad/src/model.py)")
import model  # noqa: E402
P = model.build_parts()
p = P["_p"]
bb = model.build().bounding_box()
print(f"Pod envelope {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm (limit 45 x 35 x 14 mm; "
      f"{bb.size.Y:.0f} across the wrist, {bb.size.X:.0f} along it)")
stack = p["cell"][2] + p["foam_t"] + p["module"][2]
print(f"Internal stack {stack:.1f} mm in a {p['cav_h']:.1f} mm cavity: {p['cav_h']-stack:.1f} mm, filled by the upper foam pad "
      f"({p['top_foam_t']:.1f} mm compressed) so the lid clamps the stack")
m_print = {"Enclosure base (PETG)": P["base"].volume / 1000 * DENS["PETG"],
           "Enclosure lid (PETG)": P["lid"].volume / 1000 * DENS["PETG"],
           "Gasket (TPU)": P["gasket"].volume / 1000 * DENS["TPU"]}
total = 0.0
for k, v in {**m_print, **MASS_BOUGHT_G}.items():
    total += v
    print(f"  {k:50s} {v:5.2f} g")
print(f"Total mass {total:.1f} g (limit 30 g); margin {30-total:.1f} g")
print(f"With a 12 g silicone strap (TRL 3 baseline, replaced per TRT-DDR-002): {total-8+12:.1f} g; "
      f"with a 10 g textile strap: {total-8+10:.1f} g")

# ---------------------------------------------------------------- R10: cost
hr("R10: cost (bom/bom.csv)")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
target = 150.0   # budget_usd in project.yaml: a value-engineering target, not a limit
print(f"{len(rows)} lines, parts total ${cost:.2f} per band; value-engineering target ${target:.0f}, "
      f"${target-cost:.2f} under the target")
