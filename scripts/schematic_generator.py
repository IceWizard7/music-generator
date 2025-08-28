import mcschematic
from colorama import Fore, Style

xz_locations = []
y_locations = []

def define_constants():
    global xz_locations, y_locations

    current_y_location = 1
    current_y_location_index = 0
    for i in range(32):
        if current_y_location_index % 8 == 0:
            current_y_location -= 4
            current_y_location_index = 0
        else:
            current_y_location -= 2
        current_y_location_index += 1
        y_locations.append(current_y_location)


    current_x_location = 2
    for i in range(8):
        if i % 2 == 0:
            current_x_location -= 4
        else:
            current_x_location -= 8

        for j in range(32):
            xz_locations.append((current_x_location, 2*j))

def generate_schematic(filename):
    define_constants()

    filename = filename.replace('-', '_') # Schemati (ORE Tool) doesn't like '-'

    schem = mcschematic.MCSchematic()

    with open('binary.txt', 'r') as file:
        content = file.readlines()

    clean_content = []
    for line in content:
        clean_content.append(line.replace('\n', ''))  # Remove new lines

    if any(len(item) != 32 for item in clean_content):  # Too many / too few characters at one line
        indices = [i for i, item in enumerate(clean_content) if len(item) != 32]
        raise ValueError(f'{Fore.RED}Fatal Error. Line wrong length at {indices = }.{Style.RESET_ALL}')

    if len(clean_content) > 256:  # Too many lines
        raise ValueError(f'{Fore.RED}Fatal Error. Too many lines. {len(clean_content)} (received) > 256 (maximum) Lines.{Style.RESET_ALL}')

    for address in range(len(clean_content)):
        for y_pos, bit in enumerate(clean_content[address]):
            if bit == '0':
                block_data = 'minecraft:white_wool'  # "0"
            elif bit == '1':
                if xz_locations[address][0] in [-2, -14, -26, -38]: # west
                    block_data = 'minecraft:repeater[facing=west]'  # "1"
                else: # east
                    block_data = 'minecraft:repeater[facing=east]'  # "1"
            else:
                raise ValueError(f'{Fore.RED}Fatal Error. {address = }, {y_pos}: Bit not 1 or 0.{Style.RESET_ALL}')
            schem.setBlock((xz_locations[address][0], y_locations[y_pos], xz_locations[address][1]), blockData=block_data)
            schem.setBlock((xz_locations[address][0], y_locations[y_pos] - 1, xz_locations[address][1]), blockData='minecraft:lime_wool')

    schem.save('../schematics', filename, mcschematic.Version.JE_1_20_4)

    print(f'{Fore.LIGHTGREEN_EX}Successfully generated Schematic! ({filename}){Style.RESET_ALL}')
    # print(f'Paste with:')
    # print(f'//schematic load {filename}')
    # print(f'//paste -a')

if __name__ == '__main__':
    generate_schematic('test')
