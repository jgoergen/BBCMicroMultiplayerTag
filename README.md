# BBC Micro:bit Multiplayer Tag!
A multiplayer tag game using Micro Python, bluetooth, an OLED display and a Piezo Buzzer.

I was trying to see how much of an actual multiplayer game I could make with the external display and sound.
This isn't the most graphically / sonically exciting game I've ever played, but it is kinda fun. I ran out of memory pretty fast so it would appear that this is as complicated a multiplayer game as I could make with micropython.

## Video walkthrough of the hardware build
[![BBC Micro:bit game Video](https://img.youtube.com/vi/IspkMoiKzlE/0.jpg)](https://youtu.be/IspkMoiKzlE)

The hardware consists of:
1. A BBC Micro:bit
2. BBC Micro:Bit Connector Breakout Kit
3. A 128 x 64 monochrome I2C OLED display
4. A Piezo Buzzer
5. A Twin AA Battery Holder with batteries

The hardware is from Hackerboxes box #22, more info can be found here:
http://www.instructables.com/id/HackerBox-0022-BBC-MicroBit/

The idea of the game is each player has a large dot, which represents themselves and a small dot which represents the other player. Tilting the units moves your dot around the screen. Over time the "power gauge" fill up automatically and it can be spent on speeding your character up ( holding the left button. ) And finally when the "power gauge" is full you can use the right button to "tag" the other player. If you are directly ontop of the other player ( or very close, anyways ) you win. Otherwise your gauge empties out and you are left vulnerable.

The Display uses I2C. The code for this display was taken from other libraries. I just pulled in exactly what I needed to get the job done. Because the display update rate was so slow I wrote my own code to manage writting pixels and erasing ONLY the last pixels written ( since last erase ) which I found to be much faster then all of the code I found online which cleared every pixel whenever I wanted to clear the screen.

The Buzzer, tilt, and LED code is using the built in Micro:bit libraries.
