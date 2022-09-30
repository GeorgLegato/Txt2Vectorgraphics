# Text to Vectorgraphics
This is a custom script to extend Automatic1111 StableDiffusion WebUI, in order to generate useful SVG or PDF icons given by your prompts.

## How it works
It tunes your prompts in that way to create suitable images to be vectorizied by the POTRACE command line tool.
The resulting SVG or PDF file is stored next to your png files in output/samples (default).

## Examples


## Installation
- Clone or download the txt2vectorgraphics.py file 
- place it into your SD-installtion folder into "scripts"
- run your webui as usual

## Dependencies, Potrace
At execution time, the script checks if your have 
- already POTRACE in your PATH
- if not, it will download automatically the zip from POTRACE´s sourceforge site (win-x64),
https://potrace.sourceforge.net/download/1.16/potrace-1.16.win64.zip  
and extracts only the executable into scripts folder in the scripts folder.

# Recommendations
- Use short prompts, like "Einstein", "Happy Einstein" ...
- avoid "realistic" attributes
- Sampling Steps ~40 is my best experience (to reduce noise and avoid details)
- CFG Scale 10-12
- Dont restore faces
- use 512x512 if no special demand on ratio
- Batch count support (16)
- Mostly you want to make white parts opaque (see checkbox in the scripts ui)
- Same for clipping the content to SVG size
