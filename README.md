# bmp2hex - Graphics bitmap file to C-style hex converter

```
Author:    		Robert Gallup (bg@robertgallup.com)
Date:      		June 7, 2018
License:   		MIT Opensource License (see license.txt) 
Compatability: 	Python 2/3
Version:		2.1
```

## New in Version 2.1

* The batch file has been removed. The main command line supports multiple files for input:

``` bash
$ python bmp2hex.sh *.bmp	
```

* 1-bit, 4- and 8-bit grayscale, and color (16-bit, 5/6/5 format) .bmp files are now supported (some sample files have been added to the repository). All of these files can be created using Adobe Photoshop (and, maybe GIMP)
* The table name is now derived from the uppercase of the file name rather than being a command line parameter.
* A typedef parameter has been added which uses a single "GFXMeta" typedef in the definitions of all the images. This makes it easier to create arrays of pointers to images (very useful in various applications)

### Bin2Hex Overview

Command line Python utility to output a table of hex values representing the size and data from a .bmp graphics file. This would typically be used to create graphics for display by a microprocessor, say an Arduino, on an OLED or LCD.

The *input* is a .bmp file. Windows format 1-bit, grayscale (8-bit), and color (16-bit) bitmaps are known to work.

The *output* is a valid C structure variable definition with meta data for image width and height. A _raw_ format is also supported with the image data defined as an array of const unsigned char. Since bitmaps can take a significant number of bytes, the PROGMEM keyword is used to place data in program memory, rather than on the stack.

Results from bmp2hex.py are directed to **standard output**. You can redirect them to a file, or use cut/paste to transfer the output to your code.

### The command line is:

``` bash
$ python bmp2hex.py [-h] [-i] [-r] [-d] [-t] [-w WIDTH] [-b BYTESIZE] infile
```

### Where:

*-h, \-\-help* : Help<br />
*-i, \-\-invert* : Invert image pixel colors<br />
*-r, \-\-raw* : Output data in *raw* table format, not as a *structure*<br />
*-t, \-\-typedef* : Uses a typedef to represent table data<br />
*-d, \-\-double* : uses double byte 'uint16_t' for pixels rather than the default, 'uint8_t'<br />
*WIDTH* : Width of table in infile bytes (optional). \[*default: 16*\]<br />
*BYTESIZE* : Number of bytes for size (optional). 0=auto, 1 or 2 (big endian) \[*default: 0*\]<br />
*infile* : Path to input .bmp file<br />

### Example 1:

``` bash
$ python bmp2hex.py -w 8 soba.bmp
```
Process the file *soba.bmp*. Display the pixel data with *8* hex bytes on each row.

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
$ python bmp2hex.py -t -w 12 soba.bmp
```
Process the file, *soba.bmp*, using the 'typedef' format. Use a 12 hex bytes wide listing.

### Output:

```
typedef PROGMEM const struct {
  unsigned int   width;
  unsigned int   height;
  unsigned int   bitDepth;
  uint8_t *pixel_data;
} GFXMeta;

const PROGMEM uint8_t SOBA_PIXELS[] = {
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X80, 0X00, 0X00, 0X00, 0X01,
0X90, 0X00, 0X00, 0X00, 0X03, 0X30, 0X00, 0X00, 0X00, 0X06, 0X60, 0X00,
0X00, 0X00, 0X0C, 0XC0, 0X00, 0X00, 0X00, 0X19, 0X80, 0X00, 0X1F, 0X00,
0X33, 0X00, 0X00, 0X7B, 0XC0, 0X66, 0X00, 0X01, 0XE0, 0XF0, 0XCC, 0X00,
0X03, 0X80, 0X39, 0X98, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X07, 0XFF,
0XFF, 0XFF, 0XE0, 0X07, 0XFF, 0XFF, 0XFF, 0XE0, 0X07, 0XFF, 0XFF, 0XFF,
0XE0, 0X07, 0XFF, 0XFF, 0XFF, 0XE0, 0X07, 0XFF, 0XFF, 0XFF, 0XE0, 0X03,
0XFF, 0XFF, 0XFF, 0XC0, 0X03, 0XFF, 0XFF, 0XFF, 0XC0, 0X01, 0XFF, 0XFF,
0XFF, 0X80, 0X01, 0XFF, 0XFF, 0XFF, 0X80, 0X00, 0XFF, 0XFF, 0XFF, 0X00,
0X00, 0X7F, 0XFF, 0XFE, 0X00, 0X00, 0X3F, 0XFF, 0XFC, 0X00, 0X00, 0X1F,
0XFF, 0XF8, 0X00, 0X00, 0X0F, 0XFF, 0XF0, 0X00, 0X00, 0X03, 0XFF, 0XC0,
0X00, 0X00, 0X01, 0XFF, 0X80, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00,
0X00, 0X00, 0X00, 0X00
};
GFXMeta SOBA_META = {40, 32, 1, (uint8_t *)SOBA_PIXELS};
```
