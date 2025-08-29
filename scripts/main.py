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
