import numpy as np
import cv2
import argparse

def _split_img(img, framejump, frame_width):
    """ Splits the image into frames 
    
    Parameters
    ----------
    img : np.ndarray - the image as an array

    framejump : int - the number of pixels to move between frames

    frame_width : int - the width of each frame

    Returns
    -------
    None

    """
    images = []
    left = 0
    right = frame_width
    while right < img.shape[1]:
        split = img[:, left:right, :]
        images.append(split)
        left += framejump
        right += framejump
    return images

def _save_video(img, fps, framejump, mode, ratio):
    """ Saves the image to a video 
    
    Parameters
    ----------
    img : np.ndarray - the image as an array

    fps : int - the desired frames per second of the video

    framejump : int - the number of pixels to move between frames

    mode : str - "portrait" or "landscape"

    ratio : float - the desired aspect ratio

    Returns
    -------
    None

    """
    img_width = int(img.shape[0]*ratio)
    images = _split_img(img, framejump, img_width)
    size = (img_width, img.shape[0])

    out = cv2.VideoWriter(f"{args.filename.split('.')[0]}_{mode}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    for frame in images:
        out.write(frame)
    out.release()

def convert_to_vid(filename, fps=60, framejump=4, landscape=False, portrait=True):
    """ Converts a panoramic image to a scrolling video 
    
    Parameters
    ----------
    filename : str - the name of the panorama file

    fps : int (default=60) - the desired frames per second of the video

    framejump : int (default=4) - the number of pixels to move between frames

    landscape : bool (default=False) - whether or not to save a landscape version of the video

    portrait : bool (default=True) - whether or not to save a portrait version of the video

    Returns
    -------
    None
    """
    img = cv2.imread(args.filename)
    if args.portrait or not args.landscape:
        ratio = 9/16
        _save_video(img, fps, framejump, "portrait", ratio)

    if args.landscape:
        ratio = 16/9
        _save_video(img, fps, framejump, "landscape", ratio)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Filename of panorama photo")
    parser.add_argument("--fps", type=int, help="Frames per second of video (default=60)")
    parser.add_argument("--framejump", type=int, help="Pixels to move between frames (default=4)")
    parser.add_argument("--landscape", action='store_const', const=True, help="Save a video in landscape mode")
    parser.add_argument("--portrait", action='store_const', const=True, help="Save a video in portrait mode (default)")
    args = parser.parse_args()

    if args.filename is None:
        print("Must put filename as first argument")
        print("See all options with --help")
        exit()

    fps = 60 if args.fps is None else args.fps
    framejump = 4 if args.framejump is None else args.framejump
    convert_to_vid(args.filename, portrait=args.portrait, landscape=args.landscape, fps=fps, framejump=framejump)