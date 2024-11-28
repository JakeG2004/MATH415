from midiutil import MIDIFile

# Define MIDI file parameters
track = 0
channel = 0
start_time = 0  # Start time
tempo = 120     # Tempo in BPM
volume = 100    # Volume (0-127)

# Create a new MIDI file with one track
mf = MIDIFile(1)
mf.addTempo(track, start_time, tempo)

# Notes for the scale (C major scale as an example: C4 to C5)
scale_notes = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI pitches

# Add each note of the scale
cur_time = start_time
for pitch in scale_notes:
    mf.addNote(track, channel, pitch=pitch, time=cur_time, duration=1, volume=volume)
    cur_time += 1  # Move to the next beat for the next note

# Save the MIDI file
output_filename = "scale.mid"
with open(output_filename, "wb") as output_file:
    mf.writeFile(output_file)

print(f"Scale MIDI file saved as '{output_filename}'.")
