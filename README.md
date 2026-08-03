# UST to LAB Converter

Converts Diffsinger `.ds` files (exported from OpenUtau) to `.lab` files for VLabeler.

## Overview

When you render a UST in OpenUtau with a DiffSinger voicebank, it produces a `.ds` file containing phoneme-level timing and pitch data. This script extracts the phoneme timings from that `.ds` file and converts them into an HTK-style `.lab` file that VLabeler can import for manual label editing.


<img width="2112" height="1048" alt="Screenshot 2026-08-02 194734" src="https://github.com/user-attachments/assets/618c183d-9ae5-4b2f-b22d-e47c6b43447f" />

## Workflow

```
Vocal WAV
    ↓
diffsingerGenbasedoffvocals.py
    ↓
.ust (UTAU Sequence Text) (where you can adjust timing for word level phonemes)
    ↓
.ds (Diffsinger Synthesizer file)
    ↓
convert_ds_to_lab.py
    ↓
.lab (HTK-style label file)
    ↓
VLabeler (manual phoneme boundary editing)
```

### Step 1: Generate a UST from vocals

Use [`diffsingerGenbasedoffvocals.py`](https://github.com/Bro77XP/VocalsToUst/releases/tag/Cats) to transcribe and analyze a vocal WAV file, producing a DiffSinger-compatible `.ust` file:

Make sure the to name the wav or mp3 file "vocals"

```bash
python diffsingerGenbasedoffvocals.py
```

Place `vocals.wav` in the same directory as the script. The output is `vocals.ust` with pitch, vibrato, and phoneme data extracted from the original vocals.
Make sure they're are only vocals and no music for this to work.

### Step 2: Render in OpenUtau

1. Open the generated `.ust` file in OpenUtau
2. Load a DiffSinger voicebank (e.g. Softali)
3. Render the track (this processes the UST through the DiffSinger model)
4. Export the rendered result as a `.ds` file:
   - **File → Save DS** or **File → ExportDS**

### Step 3: Convert DS to LAB

Run this script to convert the exported `.ds` file to a `.lab` file for VLabeler:

```bash
# Use default input/output paths
python convert_ds_to_lab.py

# Shift all phoneme timings earlier by 0.5 seconds
python convert_ds_to_lab.py --shift -0.5


# Shift all phoneme timings laster by 0.5 seconds
python convert_ds_to_lab.py --shift +0.2

# Specify custom input and output paths
python convert_ds_to_lab.py --shift 0.3 path/to/input.ds path/to/output.lab
```

### Step 4: Label in VLabeler

1. Place the `.lab` file in your VLabeler project's `lab` folder
2. The `.lab` filename must match the corresponding `.wav` filename (e.g. `softali.lab` with `softali.wav`) make sure they match or else pau will show up.
3. Open the `.lbp` project in VLabeler
4. Edit phoneme boundaries as needed using the multi-entry editing mode

## Usage

```bash
python convert_ds_to_lab.py [--shift SECONDS] [input.ds] [output.lab]
```

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `input` | `softali_vocals.ds` | Path to the input DS file |
| `output` | `diffsinger/Ali/Soft/lab/softali.lab` | Path to the output LAB file |
| `--shift` | `0.0` | Shift all timings by N seconds |

### About `--shift`

The `--shift` option adds or subtracts a fixed amount of time from every phoneme boundary. This is useful when the generated labels are slightly out of sync with the audio.

- `--shift -0.5` — moves all phonemes **0.5 seconds earlier**
- `--shift 0.3` — moves all phonemes **0.3 seconds later**
- `--shift 0` (or omit) — keeps the original timings from the DS file

The shift is applied to both the start and end of each phoneme, so durations stay the same — only the position on the timeline changes. The DS file itself is never modified.

## Output Format

The script outputs HTK-style label files compatible with VLabeler's NNSVS singer labeler:

- **Time unit**: 100 nanoseconds (1 second = 10,000,000)
- **Separator**: space
- **Format**: `start end phoneme`

Example:
```
603857 1532857 pau
1532857 2397857 w
2397857 4628857 ay
4628857 5556857 l
5556857 6797857 d
6797857 7726857 pau
```

## Phoneme Mapping

The DS file uses Diffsinger phoneme notation. This script converts it to the format expected by VLabeler's NNSVS labeler:

| DS Format | LAB Format | Description |
|-----------|------------|-------------|
| `SP` | `pau` | Silence / pause |
| `en/w` | `w` | Strips `en/` prefix |
| `en/ay` | `ay` | Strips `en/` prefix |
| `en/sh` | `sh` | Strips `en/` prefix |
| `hh` | `hh` | No change (no prefix) |

## DS File Structure

The input `.ds` file is a JSON array where each element represents a phrase:

```json
{
  "offset": 0.06,
  "text": "SP wild SP",
  "ph_seq": "SP en/w en/ay en/l en/d SP",
  "ph_dur": "0.093 0.087 0.223 0.093 0.124 0.093",
  "note_seq": "rest G3 rest",
  "note_dur": "0.179 0.440 0.093",
  "f0_seq": "196.0 196.0 196.0 ..."
}
```

Key fields:
- `offset` — phrase start time in seconds
- `ph_seq` — space-separated phoneme labels
- `ph_dur` — space-separated phoneme durations in seconds
- `note_seq` — MIDI note names for each note
- `f0_seq` — fundamental frequency values at 10ms intervals

## Requirements

- Python 3.6+
- No external dependencies (uses only `json` and `argparse` from the standard library)
