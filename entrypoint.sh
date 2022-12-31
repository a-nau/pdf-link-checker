#!/bin/sh

if [ ! -z $1 ]
then
  python pdfchecker.py --pdf_path $1
else
  python pdfchecker.py
fi

