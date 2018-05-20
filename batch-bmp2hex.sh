#!/bin/bash

# Loop through all .bmp files
for f in *.bmp; do
# Get the file name
	stem=${f%.*};
# Convert file name to upper case for table name
	tbl=$(echo $stem | tr 'a-z' 'A-Z')
# Run bmp2hex with command line arguments (everything entered when script is invoked)
	python bmp2hex.py $@ $f $tbl
# Put a couple of blank lines between tables and at the end
printf "\n\n"
done
