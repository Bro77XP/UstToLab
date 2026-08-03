import json
import argparse

def ds_to_lab(ds_path, lab_path, shift=0.0):
    with open(ds_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    lab_lines = []
    
    for phrase in data:
        offset = phrase['offset'] + shift
        ph_seq = phrase['ph_seq'].split()
        ph_dur = [float(d) for d in phrase['ph_dur'].split()]
        
        current_time = offset
        for ph, dur in zip(ph_seq, ph_dur):
            start = int(round(current_time * 10000000))
            end = int(round((current_time + dur) * 10000000))
            
            label = ph
            if label == 'SP':
                label = 'pau'
            elif label.startswith('en/'):
                label = label[3:]
            
            lab_lines.append(f"{start} {end} {label}")
            current_time += dur
    
    with open(lab_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lab_lines) + '\n')
    
    print(f"Converted {len(lab_lines)} phonemes to {lab_path}")
    if shift != 0.0:
        print(f"Shifted all timings by {shift}s")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Diffsinger DS file to VLabeler lab file')
    parser.add_argument('--shift', type=float, default=0.0,
                        help='Shift all timings by N seconds (e.g. -0.5 to move earlier, 0.3 to move later)')
    parser.add_argument('input', nargs='?', default=r"C:\Users\l-ota\Downloads\softali_vocals.ds")
    parser.add_argument('output', nargs='?', default=r"C:\Users\l-ota\Downloads\diffsinger\Ali\Soft\lab\softali.lab")
    args = parser.parse_args()
    
    ds_to_lab(args.input, args.output, args.shift)
