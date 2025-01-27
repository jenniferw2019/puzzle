# Sliding Puzzle
A sliding puzzle implementation using Python Tkinter. To play, first install
the following Python packages.
* Tkinter (for GUI processing)
* OpenCV (to read the puzzle image)
* NumPy (required by OpenCV)

Then download/clone this repository. Finally, open a terminal to the
download/clone location and run

    python3 main.py 3 cat.png

and enjoy! This will create a 3-by-3 sliding puzzle (i.e. an 8-puzzle) using
the image file 'cat.png'.

If you want to use a different image (say, 'myimage.jpg'), delete the cached
image files and specify your new image on the command line

    rm img*.png                            # delete cache
    python3 main.py 3 /path/to/myimage.jpg # run with your image

and it should work. Just make sure that 'myimage.jpg' is a square image.
Otherwise, it may get visibly distorted.

To play at higher difficulty levels, just change the number on the command
line. For instance,

    rm img*.png                            # delete cache
    python3 main.py 4 /path/to/myimage.jpg # run with your image

will create a 4-by-4 sliding puzzle (i.e. a 15-puzzle), whereas

    rm img*.png                            # delete cache
    python3 main.py 6 /path/to/myimage.jpg # run with your image

will create a 6-by-6 sliding puzzle (i.e. a 35-puzzle).

Deleting the cache is necessary whenever you want to change either the
difficulty level or the puzzle image.

