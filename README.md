# Blue Raven CLI

CLI to operate the Featherweight Blue Raven over USB. Focus on reliable data download with structured outputs. Extensible to full configuration and testing.

## Install

```sh
python -m pip install -e .
```

## Usage

Common operations are summarised below; use `braven --help` or append
`--help` to any subcommand for full details and options.

- **List ports** – Enumerate available serial devices.

```sh
braven ports
braven ports --json
```

- **Status stream** – Print live `@ BLR_STAT` messages for a given duration
  (seconds). Optionally capture the stream to a file.

```sh
braven status --port COM7 --duration 5
braven status --port COM7 --duration 10 --out out/status.txt
```

- **Summary** – Request the last flight summary and write it as JSON.

```sh
braven summary --port COM7 --out out/summary.json
```

- **Download logs** – Retrieve raw low‑rate (50 Hz) or high‑rate (500 Hz)
  log lines. The CLI now waits a short period for the first line to
  arrive and treats a configurable idle timeout as the end of the log. Use
  `--idle` to adjust how long to wait (seconds) after the last received line
  before assuming the log is complete. For high‑rate data a larger idle
  timeout (5–10 seconds) is recommended to avoid prematurely closing the
  connection and freezing the device. You can limit capture with
  `--max-lines` for testing.

```sh
braven download-low --port COM7 --out out/flight1_low.txt
braven download-high --port COM7 --out out/flight1_high.txt
braven download-high --port COM7 --out out/flight1_high.txt --idle 10
```

- **Configure profiles** – Load one of the pre‑defined deployment profiles
  (`default`, `sustainer`, `2nd stage`, `3 stage sim`).

```sh
braven configure --port COM7 --profile default
```

- **Name** – Set the rocket name that appears in summaries (max 13 characters).

```sh
braven name --port COM7 "Rocket1"
```

- **Modes** – Set the unit into `checkout` or `prelaunch` mode.

```sh
braven mode --port COM7 checkout
braven mode --port COM7 prelaunch
```

- **Beeps and LEDs** – Enable/disable the automatic beeper and manually
  control the tri‑colour LED.

```sh
braven beeps --port COM7 on
braven leds --port COM7 3 1  # hold current LED
braven leds --port COM7 3 0  # release manual LED control
```

- **Erase memory** – Clear flight data or reset configuration to factory
  defaults.

```sh
braven erase --port COM7 data
braven erase --port COM7 config
```

- **Calibrate** – Control the accelerometer calibration sequence.

```sh
braven calibrate --port COM7 start   # engage calibration mode
braven calibrate --port COM7 axis    # record one orthogonal orientation
braven calibrate --port COM7 stop    # commit calibration after six axes
```

- **Simulate** – Start the built‑in flight simulator with explicit parameters.
  Each parameter is a fixed‑width field exactly as documented in the USB
  guide. See the guide for details on choosing these values.

```sh
braven simulate --port COM7 \
0080 010 \
0000 000 \
07100 0000 \
000 00002 \
0 1 0 1
```

## Notes

- **Power before USB** – Always power the Blue Raven before connecting the
  USB cable. An unpowered unit can confuse driver detection.
- **Use a data‑capable cable** – Many micro‑USB leads are charge‑only. Use one
  that supports data transfer to communicate with the Raven.
- **Disconnect energetics** – Simulations and some deployment profiles can
  actuate outputs. Remove igniters or otherwise disconnect pyro circuits
  during testing and configuration.

## Functionality Test Log (COM7)

### Verified working

- **Port listing**
  - Command: `braven ports`
  - Result: Enumerates serial devices.
- **Status stream**
  - Command: `braven status --port COM7 --duration 5`
  - Result: Streams `@ BLR_STAT` lines.
- **Flight summary**
  - Command: `braven summary --port COM7 --out out/summary.json`
  - Result: Writes last flight summary as JSON.
- **Download: low-rate**
  - Command: `braven download-low --port COM7 --out out/flight_low.txt`
  - Result: Captures only `@ LOG_LOW` lines. Stops on prefix change or idle timeout.
- **Download: high-rate**
  - Command: `braven download-high --port COM7 --out out/flight_high.txt`
  - Result: Captures only `@ LOG_HIR` lines. Stops on prefix change or idle timeout.
- **Mode control**
  - Checkout: `braven mode --port COM7 checkout` → Beeps stop; LED hold persists.
  - Prelaunch: `braven mode --port COM7 prelaunch` → Pad-ready; beeps resume.
- **Configure (default)**
  - Command: `braven configure --port COM7 default`
  - Result: Loads canned profile.
- **Name**
  - Command: `braven name --port COM7 "Test1"`
  - Result: Reflected in next `summary`.
- **Beeps**
  - Commands: `braven beeps --port COM7 off` / `braven beeps --port COM7 on`
  - Result: Audible toggle verified.
- **LEDs**
  - Commands: `braven leds --port COM7 1 1`, `braven leds --port COM7 1 0`, `braven leds --port COM7 3 0`
  - Result: In **prelaunch**, firmware reclaims LEDs after a few seconds. In **checkout**, manual hold persists.

### To test next (non-destructive)

- **Configure (sustainer)**
  - `braven configure --port COM7 sustainer`
- **Configure (2nd stage)**
  - `braven configure --port COM7 "2nd stage"`
- **Configure (3 stage sim)**
  - `braven configure --port COM7 "3 stage sim"`
- **Calibrate**
  - `braven calibrate --port COM7 start` → place in each of 6 orientations → `braven calibrate --port COM7 axis` ×6 → `braven calibrate --port COM7 stop`
- **Simulate**
  - `braven simulate --port COM7 0080 010 0000 000 07100 0000 000 00002 0 1 0 1`
  - Note: Disconnect energetics. Outputs may actuate per logic.

### Destructive (run last)

- **Erase data**
  - `braven erase --port COM7 data`
  - Effect: Clears stored flights.
- **Erase config**
  - `braven erase --port COM7 config`
  - Effect: Resets settings to factory defaults; reconfiguration required.

### Behaviour notes

- **During downloads**
  - `download-low` or `download-high` puts device into **checkout**. Beeping stops during and after. Restore with `braven mode --port COM7 prelaunch` or power-cycle.
- **LED control**
  - In **prelaunch**, firmware may override manual LED states. Use **checkout** to keep manual LED hold active.
