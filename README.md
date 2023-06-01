# disco-button
Disco Button built using CircuitPython, Raspberry Pi Pico Ws, and Adafruit IO
Here's what the builds look like in their current - in progress - state
https://www.instagram.com/reel/CsfGvRLMZmW/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA==
Things are working, but there is some random crashing that I'm trying to get to the bottom of.

More to come...

Here's what the build looks like for the Button:
Note - these are the exact parts (not acurately shown in Frizing, but wiring is:)
- Raspberry Pi Pico W
- Large Arcade Button with LED 60mm White - https://www.adafruit.com/product/1192 (shown below as separate button & LED, but wiring is same)
- Panel Mount 10K potentiometer (Breadboard Friendly) - 10K Linear - https://www.adafruit.com/product/562
- The NeoPixel strip I used has no weatherproof plastic coating & hast 7mm square NeoPixels & 10mm between the LEDs. It may be this one, but also might be some off-brand I bought. Sorry - I don't remember - https://www.adafruit.com/product/1138
<img width="1582" alt="image" src="https://github.com/gallaugher/disco-button/assets/20801687/2a02d217-6af5-49db-ac87-661b810bd363">

Here's what the build looks like for the subscriber with speaker & LED lights (but I intend to break this up with audio & neopixels eventually in separate builds for better power management):
- Raspberry Pi Pico W
- Adafruit Micro SD SPI or SDIO Card Breakout Board - 3V ONLY! - https://www.adafruit.com/product/4682
- Wholesale Dream Color LED String Lights WS2811 RGBIC Addressable Individually Full Color 5V Input IP67 360 Degree Light-emitting - LED space 1.5cm, 5 meters - https://www.aliexpress.us/item/3256804447608449.html?spm=a2g0o.order_list.order_list_main.5.44e71802plBaCq&gatewayAdapt=glo2usa
- Any speaker with a stanard 3.5 mm plug will do. I'll eventually add a stereo breadboard jack to the build for sturdier input, but this works for now.
- To connect to speaker, either pin-aligator clips, or (better) a breadboard-friendly stereo jack - 1699 - https://www.adafruit.com/product/1699
<img width="1578" alt="image" src="https://github.com/gallaugher/disco-button/assets/20801687/350afb99-723a-4d72-bd5f-2091516f42d3">

And here's the build for the Pico W with the relay switch. It uses:
- Adafruit STEMMA Non-Latching Mini Relay - JST PH 2mm - 4409 https://www.adafruit.com/product/4409
- And a simple two-prong extension cord with a disco projector light plugged in.
<img width="1852" alt="image" src="https://github.com/gallaugher/disco-button/assets/20801687/0b58d907-9487-4e5b-9ff9-01bc6a4486ba">


