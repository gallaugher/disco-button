# MQTT Disco Subscriber turns relay switch on (Rainbow) and off (Solid)
# The switch is attached to an extension cord plugged into a disco light
import board, time, neopixel, microcontroller, digitalio
import os, ssl, socketpool, wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT

# setup the relay
relay = digitalio.DigitalInOut(board.GP17)
relay.direction = digitalio.Direction.OUTPUT
relay.value = False # No power through the relay

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
    # The bulk of your code to respond to MQTT will be here, NOT in while True:
    print(f"topic: {topic}, message: {message}")
    if topic == animation:
        current_animation = message
        print(f"current_animation from message: {current_animation}")
        if current_animation == "Solid":
            print("light off")
            relay.value = False # turn off disco light
        elif current_animation == "Rainbow":
            print("LIGHT ON!")
            relay.value = True # turn on disco light

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

while True:
    # keep checking the mqtt message queue
    try:
        mqtt_client.loop()
    except Exception as e:
        print(f"Failed to get data, retrying: {e}")
        wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
        mqtt_client.connect()
