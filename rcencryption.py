#! /env/bin/python
import os, sys
from PIL import Image



jpgfile = Image.open("images.jpg")

print jpgfile.bits, jpgfile.size, jpgfile.format
print jpgfile
print jpgfile.info
print list(jpgfile.getdata())

jpgfile.show(command="xv")

jpgfile.save("output.jpg")
