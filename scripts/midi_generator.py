import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage, second2tick

# Mapping of natural note names to a base MIDI note for octave 4 (Middle C = 60)
base_notes = {
    'C': 60,
    'C#': 61,
    'D': 62,
    'D#': 63,
    'E': 64,
    'F': 65,
    'F#': 66,
    'G': 67,
    'G#': 68,
    'A': 69,
    'A#': 70,
    'B': 71
}

def parse_token(token):
    """
    Parse tokens like "Piano_C", "Bass_Drum_C", or "Piano_2F#".
    Returns a tuple (note, channel) where note is the MIDI note number and
    channel is determined based on the instrument. Drum instruments use channel 9.
    """
    try:
        instrument, note_str = token.rsplit('_', 1)
    except ValueError:
        instrument = "Piano"
        note_str = token

    octave_offset = 0
    i = 0
    while i < len(note_str) and note_str[i].isdigit():
        i += 1
    if i > 0:
        octave_value = int(note_str[:i])
        octave_offset = (octave_value - 1) * 12
        note_part = note_str[i:]
    else:
        note_part = note_str

    base = base_notes.get(note_part)
    if base is None:
        raise ValueError(f"Unknown note {note_part} in token {token}")
    note_value = base + octave_offset

    # For drum instruments, use channel 9; otherwise channel 0.
    if instrument.lower().startswith('bass_drum') or instrument.lower().startswith('drum'):
        channel = 9
    else:
        channel = 0

    return note_value, channel

def create_midi_instant(filename, output_midi='output.mid', tps=1, sustain_duration=0.8):
    """
    Reads the text file where each line represents a tick (duration = 1/tps seconds).
    As each line is processed, the corresponding note-on and note-off events are added,
    and the MIDI file is rewritten. This allows you to see the output MIDI file
    updated immediately.
    
    tps - ticks per second
    sustain_duration - how long to hold each note (in seconds)
    """
    # Fixed tempo: 500000 microseconds per beat (120 BPM)
    tempo = 500000
    ticks_per_beat = 480
    tick_duration = 1.0 / tps

    events = []  # list of (time_in_seconds, type, note, channel)
    with open(filename, 'r') as f:
        lines = f.readlines()

    mid = MidiFile(ticks_per_beat=ticks_per_beat)
    
    for idx, line in enumerate(lines):
        line = line.strip()
        current_time = idx * tick_duration
        if line:
            tokens = line.split(',')
            for token in tokens:
                token = token.strip()
                if token:
                    try:
                        note, channel = parse_token(token)
                        # Add note_on and note_off events.
                        events.append((current_time, 'on', note, channel))
                        events.append((current_time + sustain_duration, 'off', note, channel))
                    except ValueError as e:
                        print(e)
                        
        # Sort events so far; in case of tie, note_on precedes note_off.
        events.sort(key=lambda x: (x[0], 0 if x[1]=='on' else 1))
        
        # Rebuild the track messages from events.
        track = MidiTrack()
        mid.tracks = [track]
        # Set tempo.
        track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
        prev_time = 0.0
        for event in events:
            event_time, ev_type, note, channel = event
            delta_seconds = event_time - prev_time
            delta_ticks = int(round(second2tick(delta_seconds, ticks_per_beat, tempo)))
            prev_time = event_time
            if ev_type == 'on':
                track.append(Message('note_on', note=note, velocity=100, channel=channel, time=delta_ticks))
            else:
                track.append(Message('note_off', note=note, velocity=0, channel=channel, time=delta_ticks))
        
        # Save (or overwrite) the MIDI file after processing this tick.
        mid.save(output_midi)
        print(f"MIDI file updated as {output_midi} after processing tick {idx+1}")
        
    print("Finished processing and saving final MIDI file.")

if __name__ == '__main__':
    # Adjust tps and sustain_duration as needed.
    create_midi_instant('music.txt', output_midi='../output.mid', tps=5, sustain_duration=0.8)
