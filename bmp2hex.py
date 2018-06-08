#!/usr/bin/env python

##@file bmp2hex.py
#  @ingroup util
#	A script for converting a 1-bit bitmap to HEX for use in an Arduino sketch.
#
#	The BMP format is well publicized. The byte order of the actual bitmap is a
#	little unusual. The image is stored bottom to top, left to right. In addition,
#	The pixel rows are rounded to DWORDS which are 4 bytes long. SO, to convert this
#   to left to right, top to bottom, no byte padding. We have to do some calculations
#	as we loop through the rows and bytes of the image. See below for more
#
#	Usage: 
#	>>>bmp2hex.py [-i] [-w <bytes>] [-b <size-bytes>] <infile> <tablename>
#	
#	@param infile		The file to convert.
#	@param tablename	The name of the table to create
#	@param raw			"-r", bitmap written as raw table [optional]
#	@param invert		"-i", to invert image pixel colors [optional] 
#	@param tablewidth	"-w <bytes>, The number of characters for each row of the output table [optional]
#	@param sizebytes	"-b <bytes>, Bytes = 0, 1, or 2. 0 = auto. 1 = 1-byte for sizes. 2 = 2-byte sizes (big endian) [optional]
#	
#	@author Robert Gallup 2016-02
#
#	Author:    Robert Gallup (bg@robertgallup.com)
#	License:   MIT Opensource License
#
#	Copyright 2016-2018 Robert Gallup 
#

import sys, array, os, textwrap, math, random, argparse

class DEFAULTS(object):
	TYPEDEF_NAME = 'GFXMeta'

def main ():

	# Default parameters
	infile = ""
	tablename = ""
	tablewidth = 16
	sizebytes = 0
	invert = False
	raw = False
	typedef = False
	double = False

	# Set up parser and handle arguments
	parser = argparse.ArgumentParser()
	parser.add_argument ("infile", help="The BMP file(s) to convert", type=argparse.FileType('r'), nargs='+')
	# parser.add_argument ("tablename", nargs="?", default="bitmap", help="The name of the output table. [default: 'bitmap']")
	parser.add_argument ("-r", "--raw", help="Outputs all data in raw table format", action="store_true")
	parser.add_argument ("-i", "--invert", help="Inverts bitmap pixels", action="store_true")
	parser.add_argument ("-w", "--width", help="Output table width in hex bytes [default: 16]", type=int)
	parser.add_argument ("-b", "--bytes", help="Byte width of BMP sizes: 0=auto, 1, or 2 (big endian) [default: 0]", type=int)
	parser.add_argument ("-t", "--typedef", help="Uses typedef (" + DEFAULTS.TYPEDEF_NAME + ") to structure data", action="store_true")
	# parser.add_argument ("-m", "--meta", help="Outputs graphics without the typedef definition", action="store_true")
	parser.add_argument ("-d", "--double", help="Defines data in 'words' rather than bytes", action="store_true")
	args = parser.parse_args()

	# Required arguments
	infile = args.infile

	# Options
	# if args.tablename:
	# 	tablename = args.tablename
	if args.raw:
		raw = args.raw
	if args.invert:
		invert = args.invert
	if args.width:
		tablewidth = args.width
	if args.bytes:
		sizebytes = args.bytes % 3
	if args.typedef:
		typedef = args.typedef
	if args.double:
		double = args.double

	# Output typedef, if requested
	if (typedef):
		print ('typedef PROGMEM const struct {')
		print ('  unsigned int   width;')
		print ('  unsigned int   height;')
		print ('  unsigned int   bitDepth;')
		print ('  ' + ('uint8_t *', 'uint16_t *')[double] + 'pixel_data;')
		print ('} ' + DEFAULTS.TYPEDEF_NAME + ';')
		print ('')

	# Do the work
	# bmp2hex(infile, tablename, tablewidth, sizebytes, invert, raw, typedef, meta)
	for f in args.infile:
		bmp2hex(f.name, tablewidth, sizebytes, invert, raw, typedef, double)

# Utility function. Return a long int from array (little endian)
def getLONG(a, n):
	return (a[n+3] * (2**24)) + (a[n+2] * (2**16)) + (a[n+1] * (2**8)) + (a[n])

# Utility function. Return an int from array (little endian)
def getINT(a, n):
	return ((a[n+1] * (2**8)) + (a[n]))

# Main conversion function
def bmp2hex(infile, tablewidth, sizebytes, invert, raw, typedef, double):

	# Set the table name to the uppercase root of the file name
	tablename = os.path.splitext(infile)[0].upper()

	# Convert tablewidth to characters from hex bytes
	tablewidth = int(tablewidth) * 6

	# Initilize output buffer
	outstring =  ''

	# Open File
	fin = open(os.path.expanduser(infile), "rb")
	uint8_tstoread = os.path.getsize(os.path.expanduser(infile))
	valuesfromfile = array.array('B')
	try:
		valuesfromfile.fromfile(fin, uint8_tstoread)
	finally:
		fin.close()

	# Get bytes from file
	values=valuesfromfile.tolist()

	# Exit if it's not a Windows BMP
	if ((values[0] != 0x42) or (values[1] != 0x4D)):
		sys.exit ("Error: Unsupported BMP format. Make sure your file is a Windows BMP.")

	# Calculate width, heigth
	dataOffset	= getLONG(values, 10)	# Offset to image data
	pixelWidth  = getLONG(values, 18)	# Width of image
	pixelHeight = getLONG(values, 22)	# Height of image
	bitDepth	= getINT (values, 28)	# Bits per pixel
	dataSize	= getLONG(values, 34)   # Size of raw data

	# Calculate line width in bytes and padded byte width (each row is padded to 4-byte multiples)
	byteWidth	= int(math.ceil(float(pixelWidth * bitDepth)/8.0))
	paddedWidth	= int(math.ceil(float(byteWidth)/4.0)*4.0)

	# For auto (sizebytes = 0), set sizebytes to 1 or 2, depending on size of the bitmap
	if (sizebytes==0):
		if (pixelWidth>255) or (pixelHeight>255):
			sizebytes = 2
		else:
			sizebytes = 1

	# The invert byte is set based on the invert command line flag (but, the logic is reversed for 1-bit files)
	invertbyte = 0xFF if invert else 0x00
	if (bitDepth == 1):
		invertbyte = invertbyte ^ 0xFF

	# Output the hex table declaration
	# Format depending on "raw" flag
	if (raw):
		print ('PROGMEM const unsigned char ' + tablename + ' [] = {')

		if (not (sizebytes%2)):
			print ("{0:#04X}".format((pixelWidth>>8) & 0xFF) + ", " + "{0:#04X}".format(pixelWidth & 0xFF) + ", " + \
		    	  "{0:#04X}".format((pixelHeight>>8) & 0xFF) + ", " + "{0:#04X}".format(pixelHeight & 0xFF) + ",")
		else:
			print ("{0:#04X}".format(pixelWidth & 0xFF) + ", " + "{0:#04X}".format(pixelHeight & 0xFF) + ",")

	elif (typedef):
		print ('const PROGMEM ' + ('uint8_t ', 'uint16_t ')[double] + tablename + '_PIXELS[] = {')

	else:
		print ('PROGMEM const struct {')
		print ('  unsigned int   width;')
		print ('  unsigned int   height;')
		print ('  unsigned int   bitDepth;')

		if (double):
			print ('  uint16_t  pixel_data[{0}];'.format(byteWidth * pixelHeight / 2))
		else:
			print ('  uint8_t  pixel_data[{0}];'.format(byteWidth * pixelHeight))
	
		print ('} ' + tablename + ' = {')
		print ('{0}, {1}, {2}, {{'.format(pixelWidth, pixelHeight, bitDepth))

	# Generate HEX bytes for pixel data in output buffer
	try:
		for i in range(pixelHeight):
			for j in range (byteWidth):
				ndx = dataOffset + ((pixelHeight-1-i) * paddedWidth) + j
				outstring += "{0:#04X}".format(values[ndx] ^ invertbyte) + ", "

	# Wrap the output buffer. Print. Then, finish.
	finally:
		outstring = textwrap.fill(outstring[:-2], tablewidth)
		print (outstring)
		
		if (typedef):
			print ('};')
			print (DEFAULTS.TYPEDEF_NAME + ' ' + tablename + '_META = {{{0}, {1}, {2}, '.format(pixelWidth, pixelHeight, bitDepth) + \
				 ('(uint8_t *)', '(uint16_t *)')[double] + tablename + "_PIXELS};\n\n")
		else:
			if (not raw):
				print ("}")
			print ("};")


# Only run if launched from commandline
if __name__ == '__main__': main()