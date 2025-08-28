# by victor_the_king (@the_victorius)

import pynbs

instruments = ('Piano', 'Bass', 'Drum', 'Piano', 'Click', 'Guitar', 'Flute', 'Bell', 'Chime')
note_names = (
    '1F#', '1G', '1G#', '1A', '1A#', '1B', '1C', '1C#', '1D', '1D#', '1E', '1F',
    '2F#', '2G', '2G#', '2A', '2A#', '2B', '2C', '2C#', '2D', '2D#', '2E', '2F', '3F#'
)

def generate_song(name):
    song = pynbs.read(name)
    r_tick = 0
    lines = []

    for tick, chord in song:
        gap = tick - r_tick - 1
        if gap > 0:
            lines.extend([''] * gap)
        r_tick = tick

        values = []
        for note in chord:
            instrument = instruments[0] if note.instrument > 8 else instruments[note.instrument]
            values.append(f'{instrument}_{note_names[note.key - 33]}')
        line = ','.join(values)
        lines.append(line)



    print(f'Reducing Length. Original Length: {len(lines)}')
    lines = lines[:255]
    text = '\n'.join(lines)

    with open('music.txt', 'w') as f:
        f.write(text)

if __name__ == '__main__':
    generate_song("../jinglebells.nbs")
