# bmp2hex - Graphics bitmap file to C-style hex converter

```
Author:    		Robert Gallup (bg@robertgallup.com)
Date:      		March 20, 2018
License:   		MIT Opensource License (see license.txt) 
Compatability: 	Python 2/3
Version:		2
```

## New in Version 2

* Non-Windows .bmp files are now flagged as unsupported.
* 1-bit, grayscale (8-bit), and color (16-bit, 5/6/5 format) .bmp files are now supported (sample files have been added to the repository). All of these files can be created using Adobe Photoshop (and, maybe GIMP)
* There is now a creative, default name for the output bitmap data, *bitmap*.
* The default output is now a C structure variable. This makes it easier to use in a C program. The original "raw" table format can still be output using the "-r" option.
* The batch shell script has been changed to allow command line arguments. Any arguments added after the script invocation will be passed to bin2hex.
* Also in the batch script, by default, *bin2hex* output is directed to the terminal. If you want it in a file, you can use ">>" redirection on the batch command. E.g., to output converted bitmaps to the file, *bitmapdata.h* use:

``` bash
$ sh batch-bmp2hex.sh -w 16 >> bitmapdata.h
```

### Bin2Hex Overview

Command line Python utility to output a table of hex values representing the size and data from a .bmp graphics file. This would typically be used to create graphics for display by a microprocessor, say an Arduino, on an OLED or LCD.

The *input* is a .bmp file. Windows format 1-bit, grayscale (8-bit), and color (16-bit) bitmaps are known to work.

The *output* is a valid C structure variable definition with meta data for image width and height. A _raw_ format is also supported with the image data defined as an array of const unsigned char. Since bitmaps can take a significant number of bytes, the PROGMEM keyword is used to place data in program memory, rather than on the stack.

Results from bmp2hex.py are directed to **standard output**. You can redirect them to a file, or use cut/paste to transfer the output to your code.

### The command line is:

``` bash
$ python bmp2hex.py [-h] [-i] [-r] [-w WIDTH] [-b BYTESIZE] infile [tablename]
```

### Where:

*-h, \-\-help* : Help<br />
*-i, \-\-invert* : Invert image pixel colors<br />
*-r, \-\-raw* : Output data in *raw* table format, not as a *structure*<br />
*WIDTH* : Width of table in infile bytes (optional). \[*default: 16*\]<br />
*BYTESIZE* : Number of bytes for size (optional). 0=auto, 1 or 2 (big endian) \[*default: 0*\]<br />
*infile* : Path to input .bmp file<br />
*tablename* : Name to use for the output table \[*default: 'bitmap'*\]<br />

### Example 1:

``` bash
$ python bmp2hex.py -w 8 soba.bmp SOBA
```
Process the file *soba.bmp*. Name the output table *SOBA*. Display the pixel data with *8* hex bytes on each row.

### Output:

```
PROGMEM const struct {
  unsigned int   width;
  unsigned int   height;
  unsigned int   bytes_per_pixel;
  uint8_t  pixel_data[160];
} SOBA = {
40, 32, 0, {
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
}
};
```

### Example 2:

``` bash
$ python bmp2hex.py -r -w 12 sobaG.bmp SOBA
```
Process the file, *sobaG.bmp*, using a *raw* table format. Use a 12 hex bytes wide listing, and use the name, *SOBA* as the table name.

### Output:

```
PROGMEM const unsigned char SOBA [] = {
0X28, 0X20,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0XFF, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0XFF,
0XFF, 0X00, 0X00, 0XFF, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0XFF, 0XFF, 0X00, 0X00, 0XFF, 0XFF, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0XFF, 0XFF, 0X00, 0X00, 0XFF, 0XFF, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0XFF, 0XFF, 0X00, 0X00,
0XFF, 0XFF, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0XFF,
0XFF, 0X00, 0X00, 0XFF, 0XFF, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X57,
0X57, 0X58, 0X58, 0X57, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0XFF, 0XFF, 0X00, 0X00, 0XFF, 0XFF, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X57, 0X57, 0X58, 0X57, 0X00, 0X58, 0X57, 0X57, 0X57, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0XFF, 0XFF, 0X00, 0X00, 0XFF, 0XFF, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X58, 0X57, 0X58, 0X58, 0X00, 0X00, 0X00, 0X00, 0X00,
0X57, 0X57, 0X57, 0X58, 0X00, 0X00, 0X00, 0X00, 0XFF, 0XFF, 0X00, 0X00,
0XFF, 0XFF, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X57, 0X57, 0X57, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X57, 0X57, 0X57, 0X00, 0X00, 0XFF,
0XFF, 0X00, 0X00, 0XFF, 0XFF, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X8A, 0X8A, 0X8B, 0X8B, 0X8A, 0X8B, 0X8A, 0X8B, 0X8A, 0X8B, 0X8A,
0X8A, 0X8B, 0X8A, 0X8A, 0X8B, 0X8A, 0X8B, 0X8B, 0X8B, 0X8B, 0X8A, 0X8B,
0X8B, 0X8B, 0X8B, 0X8B, 0X8A, 0X8B, 0X8A, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X8A, 0X8B, 0X8A, 0X8B, 0X8B, 0X8B, 0X8A,
0X8A, 0X8B, 0X8A, 0X8A, 0X8B, 0X8A, 0X8A, 0X8A, 0X8B, 0X8B, 0X8A, 0X8A,
0X8B, 0X8B, 0X8B, 0X8B, 0X8B, 0X8B, 0X8B, 0X8B, 0X8A, 0X8A, 0X8B, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X8B, 0X8A, 0X8A,
0X8A, 0X8A, 0X8A, 0X8B, 0X8A, 0X8B, 0X8B, 0X8B, 0X8B, 0X8B, 0X8B, 0X8B,
0X8A, 0X8A, 0X8A, 0X8A, 0X8A, 0X8B, 0X8A, 0X8A, 0X8B, 0X8A, 0X8B, 0X8A,
0X8A, 0X8B, 0X8B, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X8B, 0X8B, 0X8A, 0X8A, 0X8B, 0X8A, 0X8B, 0X8B, 0X8A, 0X8B, 0X8A,
0X8A, 0X8B, 0X8B, 0X8A, 0X8A, 0X8A, 0X8B, 0X8A, 0X8B, 0X8A, 0X8A, 0X8A,
0X8B, 0X8A, 0X8A, 0X8A, 0X8B, 0X8B, 0X8B, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X8B, 0X8A, 0X8B, 0X8B, 0X8B, 0X8B, 0X8A,
0X8A, 0X8B, 0X8A, 0X8A, 0X8A, 0X8A, 0X8B, 0X8A, 0X8B, 0X8B, 0X8B, 0X8B,
0X8A, 0X8B, 0X8B, 0X8A, 0X8B, 0X8A, 0X8B, 0X8A, 0X8A, 0X8A, 0X8A, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X8A, 0X8B,
0X8A, 0X8A, 0X8B, 0X8A, 0X8A, 0X8B, 0X8B, 0X8B, 0X8A, 0X8B, 0X8B, 0X8B,
0X8A, 0X8B, 0X8B, 0X8A, 0X8B, 0X8B, 0X8A, 0X8A, 0X8A, 0X8A, 0X8B, 0X8A,
0X8B, 0X8A, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X8B, 0X8B, 0X8B, 0X8A, 0X8B, 0X8B, 0X8B, 0X8B, 0X8A, 0X8B,
0X8A, 0X8B, 0X8B, 0X8A, 0X8A, 0X8B, 0X8B, 0X8A, 0X8A, 0X8B, 0X8B, 0X8A,
0X8A, 0X8A, 0X8B, 0X8A, 0X8A, 0X8B, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X8B, 0X8B, 0X8B, 0X8B, 0X8B,
0X8A, 0X8B, 0X8A, 0X8A, 0X8A, 0X8B, 0X8A, 0X8A, 0X8B, 0X8B, 0X8A, 0X8B,
0X8B, 0X8A, 0X8A, 0X8B, 0X8A, 0X8B, 0X8B, 0X8A, 0X8A, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X8B,
0X8B, 0X8A, 0X8B, 0X8B, 0X8A, 0X8B, 0X8B, 0X8B, 0X8B, 0X8A, 0X8A, 0X8B,
0X8B, 0X8A, 0X8A, 0X8B, 0X8B, 0X8B, 0X8A, 0X8A, 0X8A, 0X8B, 0X8B, 0X8A,
0X8B, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X8B, 0X8A, 0X8A, 0X8A, 0X8B, 0X8B, 0X8A, 0X8B,
0X8A, 0X8B, 0X8B, 0X8A, 0X8B, 0X8B, 0X8B, 0X8B, 0X8B, 0X8B, 0X8A, 0X8B,
0X8A, 0X8A, 0X8B, 0X8A, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X8A, 0X8B, 0X8A,
0X8B, 0X8B, 0X8A, 0X8B, 0X8B, 0X8A, 0X8A, 0X8A, 0X8A, 0X8B, 0X8A, 0X8A,
0X8A, 0X8A, 0X8A, 0X8B, 0X8B, 0X8A, 0X8B, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X8B, 0X8A, 0X8B, 0X8A, 0X8B, 0X8B, 0X8A, 0X8B, 0X8B, 0X8A,
0X8A, 0X8A, 0X8A, 0X8A, 0X8A, 0X8B, 0X8B, 0X8B, 0X8B, 0X8B, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X8B, 0X8B, 0X8A, 0X8B, 0X8B,
0X8A, 0X8B, 0X8B, 0X8B, 0X8A, 0X8A, 0X8B, 0X8B, 0X8A, 0X8B, 0X8B, 0X8A,
0X8A, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X8A, 0X8A, 0X8B, 0X8B, 0X8B, 0X8B, 0X8A, 0X8A, 0X8B, 0X8B, 0X8A, 0X8B,
0X8A, 0X8B, 0X8B, 0X8B, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X8B, 0X8A, 0X8B, 0X8A, 0X8B, 0X8A,
0X8A, 0X8A, 0X8B, 0X8A, 0X8B, 0X8A, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X8B,
0X8B, 0X8B, 0X8A, 0X8A, 0X8B, 0X8A, 0X8B, 0X8A, 0X8A, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00
};
```
