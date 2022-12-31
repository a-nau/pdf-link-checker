#!/bin/sh

if [ ! -z $1 ]
then
  python /src/pdfchecker.py --pdf_path $1
else
  python /src/pdfchecker.py
fi

