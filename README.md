# bmp2hex

```
Author:    		Robert Gallup (bg@robertgallup.com)
Date:      		March 9, 2016
License:   		MIT Opensource License (see license.txt) 
Compatability: 	Python 2/3
```

Command line Python utility to output a table of hex values representing the size and data in a bmp graphics file. This would typically be used to create graphics for display by a microprocessor, say an Arduino, on an OLED or LCD.

The _input_ is a 1-bit .bmp file (color bmp files will not work)

The _output_ is a valid C variable definition for  the Arduino. The bytes are defined as an array of const unsigned char. Since bitmaps can takea significant number of bytes, the PROGMEM keyword is used to place the data in program memory, rather than on the stack.

Results from bmp2hex.py are directed to **standard output**. You can redirect them to a file, or use cut/paste to transfer the output to your code.

### The command line is:

``` bash
$ python bmp2hex.py [-h] [-i] [-w WIDTH] [-b BYTESIZE] infile tablename
```

### Where:

_-h, \-\-help_ = Help<br />
_-i, \-\-invert_ = Invert image pixels<br />
_WIDTH_ = Width of table in infile bytes (optional). [_Default = 16_]<br />
_BYTESIZE_ = Number of bytes for size (optional). 0=auto, 1 or 2 (big endian) [_default = 0_]<br />
_infile_ = Path to input bmp file<br />
_tablename_ = Name to use for the output table<br />

### Example:

``` bash
$ python bmp2hex.py -w 8 -b 2  soba.bmp SOBA
```
Process the file _soba.bmp_. Name the output table _SOBA_. Display the table with _8_ hex bytes on each row. Display the x/y sizes of the table using _2_ bytes, the first byte is the most significant (big endian).
### Output:

```
const unsigned char PROGMEM SOBA [] = {
0X00, 0X28, 0X00, 0X20,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X80, 0X00, 0X00, 0X00, 0X01,
0X90, 0X00, 0X00, 0X00, 0X03, 0X30, 0X00, 0X00,
0X00, 0X06, 0X60, 0X00, 0X00, 0X00, 0X0C, 0XC0,
0X00, 0X00, 0X00, 0X19, 0X80, 0X00, 0X1F, 0X00,
0X33, 0X00, 0X00, 0X7B, 0XC0, 0X66, 0X00, 0X01,
0XE0, 0XF0, 0XCC, 0X00, 0X03, 0X80, 0X39, 0X98,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X07, 0XFF,
0XFF, 0XFF, 0XE0, 0X07, 0XFF, 0XFF, 0XFF, 0XE0,
0X07, 0XFF, 0XFF, 0XFF, 0XE0, 0X07, 0XFF, 0XFF,
0XFF, 0XE0, 0X07, 0XFF, 0XFF, 0XFF, 0XE0, 0X03,
0XFF, 0XFF, 0XFF, 0XC0, 0X03, 0XFF, 0XFF, 0XFF,
0XC0, 0X01, 0XFF, 0XFF, 0XFF, 0X80, 0X01, 0XFF,
0XFF, 0XFF, 0X80, 0X00, 0XFF, 0XFF, 0XFF, 0X00,
0X00, 0X7F, 0XFF, 0XFE, 0X00, 0X00, 0X3F, 0XFF,
0XFC, 0X00, 0X00, 0X1F, 0XFF, 0XF8, 0X00, 0X00,
0X0F, 0XFF, 0XF0, 0X00, 0X00, 0X03, 0XFF, 0XC0,
0X00, 0X00, 0X01, 0XFF, 0X80, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00
};
```