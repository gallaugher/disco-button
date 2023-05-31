# MQTT Disco Subscriber (ONLY LIGHTS)
# Note - I'll eventually put sound & neopixels in separate builds to better manage power,
# but am using a single subscriber while I debug.
import board, time, neopixel, microcontroller
import os, ssl, socketpool, wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT

from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.rainbow import Rainbow
from rainbowio import colorwheel

# Setup Neopixel strip & colors
BLACK = (0, 0, 0) # lights off

strip_num_of_lights = 350
strip = neopixel.NeoPixel(board.GP16, strip_num_of_lights)
strip.fill(BLACK)

# setup animations
solid_strip = Solid(strip, color=BLACK)
rainbow_strip = Rainbow(strip, speed=0.05, period=2)

current_animation = "Solid"

def roll_lights():
    block_size = round(strip_num_of_lights / 14)
    num_of_blocks = int(strip_num_of_lights/block_size)

    for i in range(num_of_blocks):
        strip[i*block_size:(i*block_size)+block_size] = [colorwheel(i*(256/num_of_blocks))] * block_size
        strip.show()
        time.sleep(0.01)

def perform_animation(current_animation):
    if current_animation == "Rainbow":
        try:
            rainbow_strip.animate()
        except Exception as e:
            print(f"ERROR: in Rainbow animation: {e}")

# Get adafruit io username and key from settings.toml
aio_username = os.getenv('AIO_USERNAME')
aio_key = os.getenv('AIO_KEY')

# Setup a feed: This may have a different name than your Dashboard
animation = aio_username + "/feeds/disco_animation"

# Setup functions to respond to MQTT events

def connected(client, userdata, flags, rc):
    # Connected to broker at adafruit io
    print("Connected to Adafruit IO! Listening for topic changes in feeds I've subscribed to")
    # Subscribe to all changes on the feed.
    client.subscribe(animation)

def disconnected(client, userdata, rc):
    # Disconnected from the broker at adafruit io
    print("Disconnected from Adafruit IO!")

def message(client, topic, message):
    global current_animation
    # The bulk of your code to respond to MQTT will be here, NOT in while True:
    print(f"topic: {topic}, message: {message}")
    if topic == animation:
        current_animation = message
        print(f"current_animation from message: {current_animation}")
        if current_animation == "Solid":
            if current_animation == "Solid":
                try:
                    solid_strip.animate()
                except Exception as e:
                    print(f"ERROR: in Solid animation: {e}")
        elif current_animation == "Rainbow":
            roll_lights()
            try:
                rainbow_strip.animate()
            except Exception as e:
                print(f"ERROR: in rainbow_strip animation: {e}")

# Connect to WiFi
print(f"Connecting to WiFi: {os.getenv("WIFI_SSID")}")
try:
    wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
except Exception as e: # if for some reason you don't connect to Wi-Fi here, reset the board & try again
    microcontroller.reset()
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

print(f"{aio_username}, {aio_key}, {pool}, {os.getenv("PORT")}, {os.getenv("BROKER")}")

# Setup the "callback" mqtt methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect to the MQTT broker (adafruit io for us)
print("Connecting to Adafruit IO...")
mqtt_client.connect()

# Roll lights just to show we're on & subscribed
roll_lights()
strip.fill(BLACK)
strip.show()
print("Ready to receive messages!")

while True:
    if current_animation != "Solid":
        perform_animation(current_animation)
    # keep checking the mqtt message queue
    try:
        mqtt_client.loop()
    except Exception as e:
        print(f"Failed to get data, retrying: {e}")
        wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
        mqtt_client.connect()
