# mount_sd.py will mount an SD card volume
import board, busio, sdcardio, storage
# setup pins for SPI
sck = board.GP10 # yellow
si = board.GP11 # blue
so = board.GP12 # green
cs = board.GP13 # yellow
spi = busio.SPI(sck, si, so)
sdcard = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
