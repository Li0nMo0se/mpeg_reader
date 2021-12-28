# MPEG decoder

## Tools

### mpeg2dec

Get pgm output from mpeg2dec in the current directory.

`tools/mpeg2dec/src/mpeg2dec -o pgm [-t <pid>] <video>`

### Video player script

`tvid.py`

```
$ python3 tvid.py -h
usage: tvid.py [-h] --input INPUT [--fps FPS] [--ppm PPM] [--progressive]

App to live visual mpeg flow

optional arguments:
  -h, --help     show this help message and exit
  --input INPUT  Folder of mpeg2dec output pgm
  --fps FPS      Output fps
  --ppm PPM      Output folder, save in ppm (if not show on screen)
  --progressive  Process images as progressive
```
