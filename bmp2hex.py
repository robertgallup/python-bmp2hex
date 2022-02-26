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
#	>>>bmp2hex.py [-i] [-r] [-n] [-d] [-x] [-w <bytes>] [-b <size-bytes>] <infile> <tablename>
#	
#	@param infile		The file to convert.
#	@param tablename	The name of the table to create
#	@param raw			"-r", bitmap written as raw table [optional]
#	@param invert		"-i", to invert image pixel colors [optional] 
#	@param tablewidth	"-w <bytes>, The number of characters for each row of the output table [optional]
#	@param sizebytes	"-b <bytes>, Bytes = 0, 1, or 2. 0 = auto. 1 = 1-byte for sizes. 2 = 2-byte sizes (big endian) [optional]
#	@param named		"-n", use a names structure [optional]
##	@param double		"-d", use double bytes rather than single ones [optional]
#	@param xbm			"-x", use XBM format (bits reversed in byte) [optional]
#	@param version		"-v", returns version number
#	
#	@author Robert Gallup 2016-02
#
#	Author:    Robert Gallup (bg@robertgallup.com)
#	License:   MIT Opensource License
#
#	Copyright 2016-2022 Robert Gallup 
#

import sys, array, os, textwrap, math, random, argparse, struct

class DEFAULTS(object):
	STRUCTURE_NAME = 'GFXMeta'
	VERSION = '2.3.5'

def main ():

	# Default parameters
	infile = ""
	tablename = ""
	tablewidth = 16
	sizebytes = 0
	invert = False
	raw = False
	named = False
	double = False
	xbm = False
	version = False

	# Set up parser and handle arguments
	parser = argparse.ArgumentParser()
	# parser.add_argument ("infile", help="The BMP file(s) to convert", type=argparse.FileType('r'), nargs='+', default=['-'])
	parser.add_argument ("infile", help="The BMP file(s) to convert", type=argparse.FileType('r'), nargs='*', default=['-'])
	parser.add_argument ("-r", "--raw", help="output all data in raw table format", action="store_true")
	parser.add_argument ("-i", "--invert", help="invert bitmap pixels", action="store_true")
	parser.add_argument ("-w", "--width", help="output table width in hex bytes [default: 16]", type=int)
	parser.add_argument ("-b", "--bytes", help="set byte width of BMP sizes: 0=auto, 1, or 2 (big endian) [default: 0]", type=int)
	parser.add_argument ("-n", "--named", help="use named structure (" + DEFAULTS.STRUCTURE_NAME + ") for data", action="store_true")
#	parser.add_argument ("-d", "--double", help="define data in 'words' rather than bytes", action="store_true")
	parser.add_argument ("-x", "--xbm", help="use XBM bit order (low order bit is first pixel of byte)", action="store_true")
	parser.add_argument ("-v", "--version", help="echo the current bmp2hex version", action="store_true")
	args = parser.parse_args()

	# Required arguments
	infile = args.infile

	# Options
	if args.raw:
		raw = args.raw
	if args.invert:
		invert = args.invert
	if args.width:
		tablewidth = args.width
	if args.bytes:
		sizebytes = args.bytes % 3
	if args.named:
		named = args.named
	# if args.double:
	# 	double = args.double
	double = False
	if args.xbm:
		xbm = args.xbm
	if args.version:
		print ('// bmp2hex version ' + DEFAULTS.VERSION)

	# Output named structure, if requested
	if (named):
		print ('struct ' + DEFAULTS.STRUCTURE_NAME + ' {')
		print ('  unsigned   int width;')
		print ('  unsigned   int height;')
		print ('  unsigned   int bitDepth;')
		print ('             int baseline;')
		print ('  ' + getDoubleType(double)[0] + 'pixel_data;')
		print ('};')
		print ('')

	# Do the work
	for f in args.infile:
		if f == '-':
			sys.exit()
		bmp2hex(f.name, tablewidth, sizebytes, invert, raw, named, double, xbm)

def reflect(a):
	"""Reverse pixels in a byte."""
	r = 0
	for i in range(8):
		r <<= 1
		r |= (a & 0x01)
		a >>= 1
	return (r)

def getDoubleType (d):
	"""Return a tuple with the C data type name and length for double and short data types."""
	if d:
		dType = 'uint16_t' + ' *'
		dLen = 2
	else:
		dType = 'uint8_t' + ' *'
		dLen = 1

	return (dType, dLen)

def unsupported_file_error(msg):
	"""Exit with unsupported file format message"""
	sys.exit("error: " + msg)

# Main conversion function
def bmp2hex(infile, tablewidth, sizebytes, invert, raw, named, double, xbm):
	"""Comvert supported BMP files to hex string output"""

	# Set up some variables to handle the "-d" option
	(pixelDataType, dataByteLength) = getDoubleType(double)

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
		unsupported_file_error("Not BMP file.")

	# Unpack header values using struct
	# Note: bytes(bytearray)) is used for compatibility with python < 2.7.3
	dataOffset,  \
	headerSize,  \
	pixelWidth,  \
	pixelHeight, \
	colorPlanes, \
	bitDepth,    \
	compression, \
	dataSize     = struct.unpack("<2L2l2h2L", bytes(bytearray(values[10:38])))

	# Check other conditions for compatibility
	if bitDepth > 16:
		unsupported_file_error("unsupported bit depth (max 16): " + str(bitDepth))
	elif pixelWidth < 0:
		unsupported_file_error("unsupported negative pixel width: " + str(pixelWidth))
	elif pixelHeight < 0:
		unsupported_file_error("unsupported negative pixel height: " + str(pixelHeight))

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
	# With "raw" output, output just an array of chars
	if (raw):
		# Output the data declaration
		print ('PROGMEM unsigned char const ' + tablename + ' [] = {')

		# Output the size of the BMP
		if (not (sizebytes%2)):
			print ("{0:#04X}".format((pixelWidth>>8) & 0xFF) + ", " + "{0:#04X}".format(pixelWidth & 0xFF) + ", " + \
		    	  "{0:#04X}".format((pixelHeight>>8) & 0xFF) + ", " + "{0:#04X}".format(pixelHeight & 0xFF) + ",")
		else:
			print ("{0:#04X}".format(pixelWidth & 0xFF) + ", " + "{0:#04X}".format(pixelHeight & 0xFF) + ",")

	elif (named):
		print ('PROGMEM ' + getDoubleType(double)[0] + ' const ' + tablename + '_PIXELS[] = {')

	elif (xbm):
		print ('#define ' + tablename + '_width ' + str(pixelWidth))
		print ('#define ' + tablename + '_height ' + str(pixelHeight))
		print ('PROGMEM ' + getDoubleType(double)[0] + ' const ' + tablename + '_bits[] = {')

	else:
		print ('PROGMEM const struct {')
		print ('  unsigned int   width;')
		print ('  unsigned int   height;')
		print ('  unsigned int   bitDepth;')
		print ('  ' + pixelDataType + 'pixel_data[{0}];'.format(round(byteWidth * pixelHeight / dataByteLength))) 
		print ('} ' + tablename + ' = {')
		print ('{0}, {1}, {2}, {{'.format(pixelWidth, pixelHeight, bitDepth))

	# Generate HEX bytes for pixel data in output buffer
	try:
		for i in range(pixelHeight):
			for j in range (byteWidth):
				ndx = dataOffset + ((pixelHeight-1-i) * paddedWidth) + j
				v = values[ndx] ^ invertbyte
				if (xbm):
					v = reflect(v)
					# print ("{0:#04x}".format(v))
				outstring += "{0:#04x}".format(v) + ", "

	# Wrap the output buffer. Print. Then, finish.
	finally:
		outstring = textwrap.fill(outstring[:-2], tablewidth)
		print (outstring)
		
		if (named):
			print ('};')
			print (DEFAULTS.STRUCTURE_NAME + ' const ' + tablename + ' = {{{0}, {1}, {2}, 0, '.format(pixelWidth, pixelHeight, bitDepth) + \
				 pixelDataType + tablename + "_PIXELS};\n\n")
		else:
			if (not (raw or xbm)):
				print ("}")
			print ("};")


# Only run if launched from commandline
if __name__ == '__main__': main()
