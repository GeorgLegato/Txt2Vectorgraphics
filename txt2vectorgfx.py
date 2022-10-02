""" 
using POTRACE as backend cmd line tool for vectorizing SD output
This script will download from

https://potrace.sourceforge.net/#downloading

the windows exetuable (todo: mac, linux support)
Potrace is under GPL, you can download the source from the url above.

If you dont want to download that, please install POTRACE to your 
system manually and assign it to your PATH env variable properly.
"""

POS_PROMPT_BW = ",((vector graphic)), ((line art)), (atari graphic)"
NEG_PROMPT_BW = ",background, colors, colorful, shading, details"

POS_PROMPT_CO = ",((cell shading)),(vector graphic), (line art), atari graphic"
NEG_PROMPT_CO = "shadings, shades, details"

PO_URL     = "https://github.com/visioncortex/vtracer/releases/download/0.4.0/vtracer.exe"
PO_EXE     = "scripts/vtracer.exe"

##########################################################################

import os
import pathlib
import subprocess
from zipfile import ZipFile
import requests
import glob
import os.path

import modules.scripts as scripts
import modules.images as Images
import gradio as gr

from modules.processing import Processed, process_images
from modules.shared import opts
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

class Script(scripts.Script):
    def title(self):
        return "Text to Vectorgraphics - VTRACER"

    def ui(self, is_img2img):
        poMode = gr.Dropdown(["Monochrome","Colored"], visible=False, label="Colormode", value="Monochrome")
      
        poFormat = gr.Dropdown(["svg","pdf"], visible=False, label="Output format", value="svg")
        poPreset = gr.Dropdown(["none","bw","poster","photo"], visible=True, label="Preset", value="none")
        poFilterSpeckle = gr.Slider(label="Filter Speckles", minimum=0, maximum=128, step=1, value=30)
        poColorPrecision = gr.Slider(label="Color Precision", minimum=1, maximum=8, step=1, value=7)
        poOpaque = gr.Checkbox(label="White is Opaque", value=True)
        poTight = gr.Checkbox(label="Cut white margin from input", value=True)
        poKeepPnm = gr.Checkbox(label="Keep temp images", value=False)
        poThreshold = gr.Slider(label="Threshold", minimum=0.0, maximum=1.0, step=0.05, value=0.5)

        return [poFormat,poOpaque, poTight, poKeepPnm, poThreshold,poPreset,poFilterSpeckle, poColorPrecision, poMode]

    def run(self, p, poFormat, poOpaque, poTight, poKeepPnm, poThreshold,poPreset,poFilterSpeckle,poColorPrecision, poMode):
        PO_TO_CALL = self.check_protrace_install()

        p.do_not_save_grid = True

        # make SD great b/w stuff
        if "Monochrome" == poMode:
            p.prompt += POS_PROMPT_BW
            p.negative_prompt += NEG_PROMPT_BW
            modearg = ["--colormode","bw"]
        else:
            p.prompt += POS_PROMPT_CO
            p.negative_prompt += NEG_PROMPT_CO
            modearg = ["--colormode","color"]

        images = []
        proc = process_images(p)
        images += proc.images        

        # unfortunately the concrete file name is nontrivial using increment counter etc, so we have to reverse-guess the last stored images by changetime
        folder = p.outpath_samples

        if opts.save_to_dirs:
            folder = glob.glob(p.outpath_samples+"/*")
            folder = max(folder, key=os.path.getctime)

        files = glob.glob(folder+"/*."+opts.samples_format)
        # latest first
        files = sorted(files, key=os.path.getctime, reverse=True)

        imagePairs = []

        try:
            # vectorize
            for i,img in enumerate(images[::-1]): 
                fullfn = files[i]
                fullof = pathlib.Path(fullfn).with_suffix('.'+poFormat)
                fullofpng = pathlib.Path(fullfn).with_suffix('.'+poFormat+".png")

                args = [PO_TO_CALL]

                if poPreset != "none": 
                    args.append("--preset")
                    args.append(poPreset)
                else:
                    args.extend (modearg)
                    args.extend (["-m", "spline"])
                    args.extend (["--path_precision", "6"])
                    args.extend (["-p", str(poColorPrecision)])

                args.extend (["-i", fullfn, "-o", fullof])

                p2 = subprocess.Popen(args)
                p2.wait()

                drawing = svg2rlg(fullof)
                #renderPDF.drawToFile(drawing, "file.pdf")
                renderPM.drawToFile(drawing, fullofpng, fmt="PNG")

#                p3 = subprocess.Popen(["magick" ,"convert", fullof, fullofpng])
#                p3.wait()

                svgimg = Image.open(fullofpng)
                imagePairs.append (img)
                imagePairs.append (svgimg)

        except (Exception):
            raise Exception("TXT2Vectorgraphics: Execution of Tracer failed, check filesystem, permissions, installation or settings")

        return Processed(p, imagePairs, p.seed, "chacka")

    def check_protrace_install(self) -> str:
        # prefer local potrace over that from PATH
        if not os.path.exists(PO_EXE):
            try:
                # check whether already in PATH 
                checkPath = subprocess.Popen(["vtracer","-v"])
                checkPath.wait()
                return "vtracer"

            except (Exception):
                try:
                    # try to download protrace and unzip locally into "scripts"
                    if not os.path.exists(PO_EXE):
                        r = requests.get(PO_URL)
                        with open(PO_EXE, 'wb') as f:
                            f.write(r.content) 
                except:
                    raise Exception("Cannot find and or download/extract Vtrace. Provide protrace in script folder. ")
        return PO_EXE
