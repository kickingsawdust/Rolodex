#!/usr/bin/env python3

# Raspberry Pi Python 3 TM1637 quad 7-segment LED display driver examples
from time import sleep

import tm1637

CLK = 15
DIO = 14
DELAY = .3

tm = tm1637.TM1637(clk=CLK, dio=DIO)

# all segments on "88:88"
tm.write([127, 255, 127, 127])
#tm.write(bytearray([127, 255, 127, 127]))
#tm.write(b'\x7F\xFF\x7F\x7F')
#tm.show('8888', True)
#tm.numbers(88, 88, True)
sleep(DELAY)

# all segments off
tm.write([0, 0, 0, 0])
#tm.show('    ')
sleep(DELAY)

# Scroll trick name
tm.scroll('Select a card with the Great Billsoni') # 4 fps

# Card flash demo

#------------SPADES------------
# Ace of Spades
tm.write([119,0,109,115])
sleep(DELAY)
# Two of Spades
tm.write([91,0,109,115])
sleep(DELAY)
# Three of Spades
tm.write([79,0,109,115])
sleep(DELAY)
# Four of Spades
tm.write([102,0,109,115])
sleep(DELAY)
# Five of Spades
tm.write([109,0,109,115])
sleep(DELAY)
# Six of Spades
tm.write([125,0,109,115])
sleep(DELAY)
# Seven of Spades
tm.write([7,0,109,115])
sleep(DELAY)
# Eight of Spades
tm.write([127,0,109,115])
sleep(DELAY)
# Nine of Spades
tm.write([111,0,109,115])
sleep(DELAY)
# Ten of Spades
tm.write([6,63,109,115])
sleep(DELAY)
# Jack of Spades
tm.write([30,118,109,115])
sleep(DELAY)
# Queen of Spades
tm.write([103,62,109,115])
sleep(DELAY)
# King of Spades
tm.write([118,6,109,115])
sleep(DELAY)
#------------HEARTS------------
# Ace of Hearts
tm.write([119,0,118,121])
sleep(DELAY)
# Two of Hearts
tm.write([91,0,118,121])
sleep(DELAY)
# Three of Hearts
tm.write([79,0,118,121])
sleep(DELAY)
# Four of Hearts
tm.write([102,0,118,121])
sleep(DELAY)
# Five of Hearts
tm.write([109,0,118,121])
sleep(DELAY)
# Six of Hearts
tm.write([125,0,118,121])
sleep(DELAY)
# Seven of Hearts
tm.write([7,0,118,121])
sleep(DELAY)
# Eight of Hearts
tm.write([127,0,118,121])
sleep(DELAY)
# Nine of Hearts
tm.write([111,0,118,121])
sleep(DELAY)
# Ten of Hearts
tm.write([6,63,118,121])
sleep(DELAY)
# Jack of Hearts
tm.write([30,118,118,121])
sleep(DELAY)
# Queen of Hearts
tm.write([103,62,118,121])
sleep(DELAY)
# King of Hearts
tm.write([118,6,118,121])
#------------CLUBS------------
sleep(DELAY)
# Ace of Clubs
tm.write([119,0,57,56])
sleep(DELAY)
# Two of Clubs
tm.write([91,0,57,56])
sleep(DELAY)
# Three of Clubs
tm.write([79,0,57,56])
sleep(DELAY)
# Four of Clubs
tm.write([102,0,57,56])
sleep(DELAY)
# Five of Clubs
tm.write([109,0,57,56])
sleep(DELAY)
# Six of Clubs
tm.write([125,0,57,56])
sleep(DELAY)
# Seven of Clubs
tm.write([7,0,57,56])
sleep(DELAY)
# Eight of Clubs
tm.write([127,0,57,56])
sleep(DELAY)
# Nine of Clubs
tm.write([111,0,57,56])
sleep(DELAY)
# Ten of Clubs
tm.write([6,63,57,56])
sleep(DELAY)
# Jack of Clubs
tm.write([30,118,57,56])
sleep(DELAY)
# Queen of Clubs
tm.write([103,62,57,56])
sleep(DELAY)
# King of Clubs
tm.write([118,6,57,56])
sleep(DELAY)
#------------DIAMONDS------------
# Ace of Diamonds
tm.write([119,0,94,6])
sleep(DELAY)
# Two of Diamonds
tm.write([91,0,94,6])
sleep(DELAY)
# Three of Diamonds
tm.write([79,0,94,6])
sleep(DELAY)
# Four of Diamonds
tm.write([102,0,94,6])
sleep(DELAY)
# Five of Diamonds
tm.write([109,0,94,6])
sleep(DELAY)
# Six of Diamonds
tm.write([125,0,94,6])
sleep(DELAY)
# Seven of Diamonds
tm.write([7,0,94,6])
sleep(DELAY)
# Eight of Diamonds
tm.write([127,0,94,6])
sleep(DELAY)
# Nine of Diamonds
tm.write([111,0,94,6])
sleep(DELAY)
# Ten of Diamonds
tm.write([6,63,94,6])
sleep(DELAY)
# Jack of Diamonds
tm.write([30,118,94,6])
sleep(DELAY)
# Queen of Diamonds
tm.write([103,62,94,6])
sleep(DELAY)
# King of Diamonds
tm.write([118,6,94,6])
sleep(DELAY)
