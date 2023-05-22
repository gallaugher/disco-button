# Just a test of playing MP3 files when pushing a button

import board, time, microcontroller, mount_sd, digitalio, random

from audiopwmio import PWMAudioOut as AudioOut
from audiomp3 import MP3Decoder

from adafruit_debouncer import Button

# create a debounced Button
button_input = digitalio.DigitalInOut(board.GP21)
button_input.switch_to_input(pull=digitalio.Pull.UP) # False when pressed, True when not pressed
button = Button(button_input)

# setup the speaker
audio = AudioOut(board.GP15) # assuming speaker plug tip to GP16

# set path where audio files can be found on device
path = "/sd/disco_songs/"

# set up the mp3 decoder
filename = "Boogie Wonderland.mp3"
mp3_file = open(path + filename, "rb")
decoder = MP3Decoder(mp3_file)

# song is normally sent over MQTT
songs = ["Disco Inferno",
        "Boogie Wonderland",
        "Play That Funky Music",
        "Stayin' Alive"]

# play an mp3 file - pass in string that includes filename extension
def play_mp3(filename):
#     if audio.playing:
#         audio.stop()
    print(f"About to play {path + filename}")
    try:
        decoder.file = open(path + filename, "rb")
        audio.play(decoder)
    except OSError as e:
        print(f"No such file/directory: {path + filename}\nERROR: {e}\nRESTARTING")
        time.sleep(5.0)
        audio.stop()
    except:
        print("UNKNOWN ERROR - RESTARTING - error while playing sound")
        time.sleep(5.0)
        microcontroller.reset()

while True:
    button.update()
    if button.pressed:
        print("BUTTON PRESSED")
        song = random.choice(songs)+".mp3"
        play_mp3(song)
    if button.released:
        print("button released")

