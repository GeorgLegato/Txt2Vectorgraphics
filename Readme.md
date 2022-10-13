# Text to Vectorgraphics
This is a custom script to extend Automatic1111 StableDiffusion WebUI, in order to generate useful SVG or PDF icons given by your prompts.

## How it works
It tunes your prompts in that way to create suitable images to be vectorizied by the POTRACE command line tool.
The resulting SVG or PDF file is stored next to your png files in output/samples (default).

## Examples

| prompt  |PNG  |SVG |
| :--------  | :-----------------: | :---------------------: |
| Happy Einstein | <img src="https://user-images.githubusercontent.com/7210708/193370360-506eb6b5-4fa7-4b2a-9fec-6430f6d027f5.png" width="40%" /> | <img src="https://user-images.githubusercontent.com/7210708/193370379-2680aa2a-f460-44e7-9c4e-592cf096de71.svg" width=30%/> |
| Mountainbike Downhill | <img src="https://user-images.githubusercontent.com/7210708/193371353-f0f5ff6f-12f7-423b-a481-f9bd119631dd.png" width=40%/> | <img src="https://user-images.githubusercontent.com/7210708/193371585-68dea4ca-6c1a-4d31-965d-c1b5f145bb6f.svg" width=30%/> |
coffe mug in shape of a heart | <img src="https://user-images.githubusercontent.com/7210708/193374299-98379ca1-3106-4ceb-bcd3-fa129e30817a.png" width=40%/> | <img src="https://user-images.githubusercontent.com/7210708/193374525-460395af-9588-476e-bcf6-6a8ad426be8e.svg" width=30%/> |
| Headphones | <img src="https://user-images.githubusercontent.com/7210708/193376238-5c4d4a8f-1f06-4ba4-b780-d2fa2e794eda.png" width=40%/> | <img src="https://user-images.githubusercontent.com/7210708/193376255-80e25271-6313-4bff-a98e-ba3ae48538ca.svg" width=30%/> |

### Screenshot
![image](https://user-images.githubusercontent.com/7210708/193370345-c3e6f3d8-2d75-48d3-98ab-b6501e953d67.png)


## Features

* New: Added Visual Styles - RadioButtons provided by the script. Edit the script to extend of modify 
Stuff like Illustration, Tattoo, Anime etc, to save your time finding prompts on your own.
If nothing matches, select "None - promp only" and have back full control.

* New: Linux and Mac support handling POTRACE for you

## Installation

### Windows
- Clone or download the txt2vectorgraphics.py file 
- place it into your SD-installtion folder into "scripts"
- run your webui as usual

### Linux
If you're running under WSL, Ubuntu or another Linux distro you will need to install potrace.
Run `sudo apt install potrace`.

### Mac
Run `brew install potrace`. Ensure `potrace` is in your PATH so that you could run in simply by calling from a command terminal.

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
