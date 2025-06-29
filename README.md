# What's this?

This is the repo for a Manimation that visually demonstrates how Linked lists and Binary Trees are traversed.
## Tools Used
- Manim CE (0.19.0)
- Jupyter notebook (I can't stress enough how much time testing with it has saved me)
- Obsidian (this is a note-taking tool that helped me plan the structure of the animations, list the objects needed for each scene, and draft the voice-over scripts. It kinda served as the backbone of all my planning)
##  Repo Structure

```bash
├── output/          # contains complete renders, I only let git track this folder (not the "media" one), since I want only the complete videos to be synced
│
├── animations.py    # contains the animations that I used in my main file
├── main.py          # contains all my scenes
├── manim-lab.ipynb  # my experimenting with manim
├── manim-lab.py     # (don't ask me why I use both my text editor and jupter notebook to do it)
├── media_script.py  # the script I use to move complete renders to the output folder
├── objects.py       # contains custom mobjects that I've created
├── processing.py    # contains helper functions
├── python-lab.ipynb # my python experimenting
└── README.md        # you are here
```
## Note:
While working on this manimation, I’ve gained a much deeper understanding of how recursive functions work. I implemented several of them myself demonstrating pre-order, in-order, and post-order visits , most of which can be found in the `objects.py` or `processing.py` files. 

If all goes well, I will start working on another manimation on recursion soon, _in sha' Allah_ =)

Link to the YouTube video: https://youtu.be/19tjEb0-vBI?si=HsA9hGMBHGNHIqFC
