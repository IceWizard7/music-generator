# READ THIS:
# Made by: IceWizard7 & Kebabissos (@v_perm)
# If you want to play the same note twice in a row, you need to use a different layer to play that note

# https://minecraft.fandom.com/wiki/Note_Block?file=Noteblock_reference.png

# Pitches:
# 1 = G
# 2 = G#
# ...
# 24 = F#
# 25 = F# (LOW OCTAVE! Minecraft Note Block Pitch = 0)

# Instruments:
# Piano (0)
# Bass (1)
# Guitar (2)
# Bell (3)
# Flute (4)
# Chime (5)
# Drum (6)
# Click (7)

# Syntax:
# Each line of the file, is a beat
# Instrument: 0, 1, 2, 7, ... being the instrument (in readme make a see ./ or area or smth)
# Pitch: 1F#, 2D, 3C, ... number being the octave (123), and character (ABCDEF) being the note
# Full Note: Instrument_Pitch, examples: 0_0F#, 1_2D, 6_1C
# Multiple Notes: Separate them with a "," (Max: 4 Notes)
# Use a "-" if you don't want any note to be played on that layer
# If you want to play 2 same notes after each other, make sure to use different layers
# For this, use "-" to represent no note on that layer

# BPM = 150
# Max notes = 255


import raw_music_generator
import schematic_generator
import noteblock_studio

song_folder = '../songs/'
schematic_folder = '../schematics/'
file_name = 'HammerOfJustice'

if __name__ == '__main__':
    noteblock_studio.generate_song(f'{song_folder}{file_name}.nbs')
    raw_music_generator.convert_to_raw_music()
    schematic_generator.generate_schematic(f'{file_name}')
