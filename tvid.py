from argparse import ArgumentParser

import pgm2ppm
import os
import os.path
import cv2
import numpy as np
import time
from datetime import datetime

import re
from typing import List

# https://stackoverflow.com/questions/4623446/how-do-you-sort-files-numerically
def sort_nicely(l: List[str]):
    """ Sort the given list in the way that humans expect.
    """

    def tryint(s):
        try:
            return int(s)
        except:
            return s

    def alphanum_key(s):
        """ Turn a string into a list of string and number chunks.
            "z23a" -> ["z", 23, "a"]
        """
        return [ tryint(c) for c in re.split('([0-9]+)', s) ]

    l.sort(key=alphanum_key)
    return l

last = datetime.now()

def handle_display(rgb_images, fps):
    global last

    for rgb_image in rgb_images:
        current = datetime.now()

        time.sleep(max((1 / fps) - (current - last).total_seconds(), 0))
        cv2.imshow(f"Output video", rgb_image[..., ::-1])
        if cv2.waitKey(25) & 0xFF == ord('q'):
            return True

        last = datetime.now()


counter_frame = 0
def handle_save(rgb_images):
    global counter_frame

    for rgb_image in rgb_images:    
        file1 = os.path.join(args.ppm, f"{str(counter_frame)}.ppm")
        cv2.imwrite(file1, rgb_image[..., ::-1])
        counter_frame += 1


if __name__ == "__main__":
    parser = ArgumentParser(description="App to live visual mpeg flow")
    parser.add_argument("--input", type=str, help="Folder of mpeg2dec output pgm", required=True)
    parser.add_argument("--fps", type=float, help="Output fps", default=25.)
    parser.add_argument("--ppm", type=str, help="Output folder, save in ppm (if not show on screen)")
    parser.add_argument("--progressive", action="store_true", help="Process images as progressive", default=False)

    args = parser.parse_args()

    if args.ppm:
        if not os.path.isdir(args.ppm):
            os.mkdir(args.ppm)


    files = sort_nicely(os.listdir(args.input))
    if len(files) == 0:
        raise ValueError(f"{args.input}: empty folder.")

    # Read, convert and display
    for file in files:
        im_path = os.path.join(args.input, file)
        if im_path.split(".")[-1] != "pgm":
            continue

        # Convert yuv from mpeg2dec to rgb image(s)
        rgb_images = pgm2ppm.yuv2rgb(im_path, out_path=None, progressive=args.progressive)

        if args.ppm is None:
            if handle_display(rgb_images, args.fps): # return true if stop display
                break
        else:
            handle_save(rgb_images)