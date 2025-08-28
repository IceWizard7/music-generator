import itertools


def instrument_to_bin(instrument):
    instruments = {
        'piano': '000',
        'bass': '001',
        'guitar': '010',
        'bell': '011',
        'flute': '100',
        'chime': '101',
        'drum': '110',
        'click': '111'
    }

    return instruments[instrument]

def pitch_to_bin(pitch):
    pitches = {
        '1F#': '11001',
        '1G': '00001',
        '1G#': '00010',
        '1A': '00011',
        '1A#': '00100',
        '1B': '00101',
        '1C': '00110',
        '1C#': '00111',
        '1D': '01000',
        '1D#': '01001',
        '1E': '01010',
        '1F': '01011',

        '2F#': '01100',
        '2G': '01101',
        '2G#': '01110',
        '2A': '01111',
        '2A#': '10000',
        '2B': '10001',
        '2C': '10010',
        '2C#': '10011',
        '2D': '10100',
        '2D#': '10101',
        '2E': '10110',
        '2F': '10111',

        '3F#': '11000'
    }

    return pitches[pitch]

def note_to_bin(note):
    if note.strip() in ('-', ''):
        return 8 * '0'
    try:
        instrument, pitch = note.strip().split('_')
        return f'{instrument_to_bin(instrument.lower())}{pitch_to_bin(pitch.upper())}'
    except (ValueError, KeyError):
        raise ValueError(f'Invalid note format: {note}')


def fix_alignment(current_note, previous_note):
    assert len(current_note) == 32 and len(previous_note) == 32

    def byte_split(s: str):
        return [s[i:i + 8] for i in range(0, 32, 8)]

    def byte_join(blocks):
        return "".join(blocks)

    prev_blocks = byte_split(previous_note)

    def is_valid(curr_blocks):
        return all(c != p or c == "00000000" for c, p in zip(curr_blocks, prev_blocks))

    blocks = byte_split(current_note)

    # 1) Try rotations only
    for shift in range(4):  # 0, 1, 2, 3 blocks
        rotated = blocks[-shift:] + blocks[:-shift] if shift else blocks
        if is_valid(rotated):
            return byte_join(rotated)

    # 2) Try permutations + rotations
    for perm in itertools.permutations(blocks, 4):
        for shift in range(4):
            rotated = list(perm[-shift:] + perm[:-shift]) if shift else list(perm)
            if is_valid(rotated):
                return byte_join(rotated)

    # 3) If nothing works
    raise ValueError("No valid alignment found — identical notes across all layers.")


def convert_to_raw_music():
    with open('music.txt', 'r') as file:
        content = file.readlines()

    clean_content = []
    raw_content = []

    for line in content:
        clean_content.append(line.replace('\n', ''))  # Remove new lines

    raw_content.append(4 * 8 * '0')
    previous_note = 4 * 8 * '0'

    for line in clean_content:
        if ',' in line:
            parts = line.split(',')
            notes = ''
            for part in parts:
                notes = notes + note_to_bin(part)

            notes = notes + ((4 - len(parts)) * 8 * '0')

            notes = fix_alignment(notes, previous_note)

            previous_note = notes
            raw_content.append(notes)
        else:
            notes = note_to_bin(line) + 3 * 8 * '0'
            notes = fix_alignment(notes, previous_note)
            previous_note = notes
            raw_content.append(notes)

    with open('binary.txt', 'w') as file:
        file.write('\n'.join(raw_content))

if __name__ == '__main__':
    convert_to_raw_music()
