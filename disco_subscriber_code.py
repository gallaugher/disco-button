# MQTT Disco Subscriber (lights & speakers) mp3
# Note - I'll eventually put sound & neopixels in separate builds to better manage power,
# but am using a single subscriber while I debug.
import board, time, neopixel, microcontroller, mount_sd
import os, ssl, socketpool, wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT

from audiomp3 import MP3Decoder

from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.SparklePulse import SparklePulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.sequence import AnimationSequence

# setup the speaker
from audiopwmio import PWMAudioOut as AudioOut
audio = AudioOut(board.GP15) # assuming speaker plug tip to GP16

# set path where audio files can be found on device
path = "/sd/disco_songs_mp3/"

filename = "Disco Inferno.mp3"
mp3_file = open(path + filename, "rb")
decoder = MP3Decoder(mp3_file)

def play_mp3(filename):
    print(f"About to play {path + filename}")
    if audio.playing:
        audio.stop()
    try:
        decoder.file = open(path + filename, "rb")
        audio.play(decoder)
    except OSError as e:
        print(f"No such file/directory: {path + filename}\nERROR: {e}\nRESTARTING")
        audio.stop()
    except Exception as e:
        print(f"Error playing sound: {e}")
#         microcontroller.reset()

# Setup Neopixel strip & colors
from adafruit_led_animation.color import (
    AMBER, #(255, 100, 0)
    AQUA, # (50, 255, 255)
    BLACK, #OFF (0, 0, 0)
    BLUE, # (0, 0, 255)
    CYAN, # (0, 255, 255)
    GOLD, # (255, 222, 30)
    GREEN, # (0, 255, 0)
    JADE, # (0, 255, 40)
    MAGENTA, #(255, 0, 20)
    OLD_LACE, # (253, 245, 230)
    ORANGE, # (255, 40, 0)
    PINK, # (242, 90, 255)
    PURPLE, # (180, 0, 255)
    RED, # (255, 0, 0)
    TEAL, # (0, 255, 120)
    WHITE, # (255, 255, 255)
    YELLOW, # (255, 150, 0)
    RAINBOW # a list of colors to cycle through
    # RAINBOW is RED, ORANGE, YELLOW, GREEN, BLUE, and PURPLE ((255, 0, 0), (255, 40, 0), (255, 150, 0), (0, 255, 0), (0, 0, 255), (180, 0, 255))
)

INDIGO = (63, 0, 255)
VIOLET = (127, 0, 255)

colors = [RED, MAGENTA, ORANGE, YELLOW, GREEN, JADE, BLUE, INDIGO, VIOLET, PURPLE, BLACK]

strip_num_of_lights = 350
strip = neopixel.NeoPixel(board.GP16, strip_num_of_lights)
strip_color = BLACK
strip.fill(strip_color)

# setup animations
solid_strip = Solid(strip, color=strip_color)
blink_strip = Blink(strip, speed=0.5, color=strip_color)
colorcycle_strip = ColorCycle(strip, 0.1, colors=colors)
chase_strip = Chase(strip, speed=0.1, color=strip_color, size=3, spacing=1)
comet_strip = Comet(strip, speed=0.05, color=strip_color, tail_length=int(strip_num_of_lights/4), bounce=True)
pulse_strip = Pulse(strip, speed=.1, color=strip_color, period=5)
sparkle_strip = Sparkle(strip, speed=0.05, color=strip_color)
sparkle_pulse_strip = SparklePulse(strip, speed=0.01, period=5, color=strip_color)
rainbow_strip = Rainbow(strip, speed=0.05, period=2)
rainbow_chase_strip = RainbowChase(strip, speed=0.1, size=3, spacing=1, reverse = False, step=16)

current_animation = "solid"

def perform_animation(current_animation):
    if current_animation == "Solid":
        try:
            if audio.playing:
                audio.stop()
        except Exception as e:
            print(f"Problem stopping voice: {e}")
        solid_strip.color = strip_color
        solid_strip.animate()
    elif current_animation == "Blink":
        blink_strip.color = strip_color
        blink_strip.animate()
    elif current_animation == "ColorCycle":
        colorcycle_strip.animate()
    elif current_animation == "Chase":
        chase_strip.color = strip_color
        chase_strip.animate()
    elif current_animation == "Comet":
        comet_strip.color = strip_color
        comet_strip.animate()
    elif current_animation == "Pulse":
        pulse_strip.color = strip_color
        pulse_strip.animate()
    elif current_animation == "Sparkle":
        sparkle_strip.color = strip_color
        sparkle_strip.animate()
    elif current_animation =="SparklePulse":
        sparkle_pulse_strip.color = strip_color
        sparkle_pulse_strip.animate()
    elif current_animation == "Rainbow":
        rainbow_strip.animate()
    elif current_animation == "RainbowChase":
        rainbow_chase_strip.animate()

# Get adafruit io username and key from settings.toml
aio_username = os.getenv('AIO_USERNAME')
aio_key = os.getenv('AIO_KEY')

# Setup a feed: This may have a different name than your Dashboard
light_color = aio_username + "/feeds/disco_color"
animation = aio_username + "/feeds/disco_animation"
disco_song_name = aio_username + "/feeds/disco_song_name"

# Setup functions to respond to MQTT events

def connected(client, userdata, flags, rc):
    # Connected to broker at adafruit io
    print("Connected to Adafruit IO! Listening for topic changes in feeds I've subscribed to")
    # Subscribe to all changes on the feed.
    client.subscribe(light_color)
    client.subscribe(animation)
    client.subscribe(disco_song_name)

def disconnected(client, userdata, rc):
    # Disconnected from the broker at adafruit io
    print("Disconnected from Adafruit IO!")

def message(client, topic, message):
    # The bulk of your code to respond to MQTT will be here, NOT in while True:
    global current_animation
    global strip_color # strip_color will be used outside this function
    print(f"topic: {topic}, message: {message}")
    if topic == light_color: # button pressed to play a sounds
        if message[0] == "#": # check to make sure it's a hex value
            message = message[1:] # remove # from string
            strip_color = int(message, 16) # converts base 16 value to int
    elif topic == disco_song_name:
        play_mp3(message+".mp3")
    elif topic == animation:
        if message != "0":
            current_animation = message
            print(f"current_animation from message: {current_animation}")
            if current_animation == "Solid":
                solid_strip = Solid(strip, color=strip_color)
            elif current_animation == "Blink":
                blink_strip.color = strip_color
            elif current_animation == "ColorCycle":
                pass
            elif current_animation == "Chase":
                chase_strip.color = strip_color
            elif current_animation == "Comet":
                comet_strip.color = strip_color
            elif current_animation == "Pulse":
                pulse_strip.color = strip_color
            elif current_animation == "Sparkle":
                sparkle_strip.color = strip_color
            elif current_animation =="SparklePulse":
                sparkle_pulse_strip.color = strip_color
            elif current_animation == "Rainbow":
                rainbow_strip.animate()
            elif current_animation == "RainbowChase":
                rainbow_chase_strip.animate()

# Connect to WiFi
print(f"Connecting to WiFi: {os.getenv("WIFI_SSID")}")
wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
print("Connected!")

# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Set up a MiniMQTT Client - this is our current program that subscribes or "listens")
mqtt_client = MQTT.MQTT(
    broker=os.getenv("BROKER"),
    port=os.getenv("PORT"),
    username=aio_username,
    password=aio_key,
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

# Setup the "callback" mqtt methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

broker=os.getenv("BROKER")
port=os.getenv("PORT")
username=aio_username
password=aio_key
socket_pool=pool
ssl_context=ssl.create_default_context()
print(f"{aio_username}, {aio_key}, {pool}, {port}, {broker}")

# Setup the "callback" mqtt methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect to the MQTT broker (adafruit io for us)
print("Connecting to Adafruit IO...")
mqtt_client.connect()

# Tell the dashboard to send the latest settings for these feeds
# Publishing to a feed with "/get" added to the feed name
# will send the latest values from that feed.

while True:
    if not audio.playing:
        current_animation = "Solid"
    perform_animation(current_animation)
    # keep checking the mqtt message queue
    try:
        mqtt_client.loop()
    except (ValueError, RuntimeError, MQTT.MMQTTException) as e:
        print("Failed to get data, retrying\n", e)
        wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
        mqtt_client.connect()
#         microcontroller.reset()
