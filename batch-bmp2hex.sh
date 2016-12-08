#!/bin/bash

echo 'Creating file: bitmaps.h'
# Create the header file
echo > bitmaps.h
# Loop through all .bmp files
for f in *.bmp; do
# Get the file name
	stem=${f%.*};
# Convert file name to upper case for table name
	tbl=$(echo $stem | tr 'a-z' 'A-Z')
# Echo the table name to the terminal
	echo "${tbl}"
# Run the conversion utility
	python bmp2hex.py $f $tbl >> bitmaps.h
# Put a couple of blank lines between tables
	echo >> bitmaps.h
	echo >> bitmaps.h
done
echo "Done!"