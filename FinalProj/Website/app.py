from flask import Flask, render_template, request, send_file
from midiutil.MidiFile import MIDIFile
from cipher_functions import *

app = Flask(__name__)

# MIDI File Creation
def create_midi_file(ciphertext, cipherType):
    ValidTokens = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "/"]
    mf = MIDIFile(1)
    track = 0
    time = 0
    mf.addTrackName(track, time, "Track")
    mf.addTempo(track, time, 120)

    channel = 0
    volume = 100
    curTime = 0
    for token in ciphertext:
        if token == '/':
            curTime += 1
        else:
            newPitch = 57 + ValidTokens.index(token)
            mf.addNote(track, channel, pitch=newPitch, time=curTime, duration=1, volume=volume)
            curTime += 1

    filepath = cipherType + "_out.mid"
    with open(filepath, "wb") as output_file:
        mf.writeFile(output_file)
    return filepath

# Flask Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/caesar', methods=["GET", "POST"])
def caesar():
    if request.method == "POST":
        melody = request.form["melody"]
        key_note = request.form["key_note"]

        tokens = GetInput(melody, 8)
        key = GetInput(key_note, 1)
        if not tokens:
            return "Invalid input! Please try again."

        try:
            # Process Caesar cipher with a note as key
            ciphertext = CaesarCipher(tokens, key)
        except ValueError:
            return "Invalid key note! Please use a valid note."

        # Generate MIDI
        midi_path = create_midi_file(ciphertext, "caesar")
        return send_file(midi_path, as_attachment=True)

    return render_template("caesar.html")

@app.route('/vig', methods=["GET", "POST"])
def vigenere():
    if request.method == "POST":
        melody = request.form["melody"]
        key_melody = request.form["key_melody"]

        tokens = GetInput(melody, 8)
        key = GetInput(key_melody, -1)

        if not tokens or not key:
            return "Invalid input! Please try again."

        try:
            # Process Caesar cipher with a note as key
            ciphertext = VigCipher(tokens, key)
        except ValueError:
            return "Invalid key note! Please use a valid melodu."

        # Generate MIDI
        midi_path = create_midi_file(ciphertext, "vigenere")
        return send_file(midi_path, as_attachment=True)

    return render_template("vig.html")

@app.route('/affine', methods=["GET", "POST"])
def affine():
    if request.method == "POST":
        melody = request.form["melody"]
        alphaStr = request.form["alpha"]
        betaStr = request.form["beta"]

        tokens = GetInput(melody, 8)
        alpha = GetInput(alphaStr, 1)
        beta = GetInput(betaStr, 1)

        if not tokens:
            return "Invalid input! Please try again."

        try:
            # Process Caesar cipher with a note as key
            ciphertext = AffineCipher(tokens, alpha, beta)
        except ValueError:
            return "Invalid key note! Please use a valid melody."

        # Generate MIDI
        midi_path = create_midi_file(ciphertext, "affine")
        return send_file(midi_path, as_attachment=True)

    return render_template("affine.html")

@app.route('/playfair', methods=["GET", "POST"])
def playfair():
    if request.method == "POST":
        melody = request.form["melody"]
        keyStr = request.form["key_melody"]

        tokens = GetInput(melody, 8)

        if not tokens:
            return "Invalid input! Please try again."

        try:
            # Process Caesar cipher with a note as key
            ciphertext = PlayfairCipher(tokens, keyStr)
        except ValueError:
            return "Invalid key note! Please use a valid melody."

        # Generate MIDI
        midi_path = create_midi_file(ciphertext, "playfair")
        return send_file(midi_path, as_attachment=True)

    return render_template("playfair.html")

@app.route('/adfgx', methods=["GET", "POST"])
def adfgx():
    if request.method == "POST":
        melody = request.form["melody"]
        keyStr = request.form["key_melody"]

        tokens = GetInput(melody, 8)

        if not tokens:
            return "Invalid input! Please try again."

        try:
            # Process Caesar cipher with a note as key
            ciphertext = ADFGXCipher(tokens, keyStr)
        except ValueError:
            return "Invalid key note! Please use a valid melody."

        # Generate MIDI
        midi_path = create_midi_file(ciphertext, "ADFGX")
        return send_file(midi_path, as_attachment=True)

    return render_template("adfgx.html")

@app.route('/hill', methods=["GET", "POST"])
def hill():
    if request.method == "POST":
        melody = request.form["melody"]
        keyStr = request.form["key"]
        dimension = int(request.form["dimension"])

        tokens = GetInput(melody, 8)
        key = GetInput(keyStr, (dimension * dimension))

        if(len(key) != dimension * dimension):
            return "Invalid input! Please try again."

        if not tokens:
            return "Invalid input! Please try again."

        try:
            # Process Caesar cipher with a note as key
            ciphertext = HillCipher(tokens, dimension, key)
        except ValueError:
            return "Invalid key note! Please use a valid melody."

        # Generate MIDI
        midi_path = create_midi_file(ciphertext, "hill")
        return send_file(midi_path, as_attachment=True)

    return render_template("hill.html")

@app.route('/paper', methods=["GET", "POST"])
def paper():
    return send_file("paper.pdf", as_attachment=True)