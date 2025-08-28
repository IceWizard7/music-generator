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

def convert_to_raw_music():
    with open('music.txt', 'r') as file:
        content = file.readlines()

    clean_content = []
    raw_content = []

    for line in content:
        clean_content.append(line.replace('\n', ''))  # Remove new lines

    raw_content.append(4 * 8 * '0')

    for line in clean_content:
        if ',' in line:
            parts = line.split(',')
            notes = ''
            for part in parts:
                notes = notes + note_to_bin(part)

            notes = notes + ((4 - len(parts)) * 8 * '0')

            raw_content.append(notes)
        else:
            notes = note_to_bin(line) + 3 * 8 * '0'
            raw_content.append(notes)

    with open('binary.txt', 'w') as file:
        file.write('\n'.join(raw_content))

if __name__ == '__main__':
    convert_to_raw_music()
