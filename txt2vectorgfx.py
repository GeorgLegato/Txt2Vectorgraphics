""" 
using POTRACE as backend cmd line tool for vectorizing SD output
This script will download from

https://potrace.sourceforge.net/#downloading

the windows exetuable (todo: mac, linux support)
Potrace is under GPL, you can download the source from the url above.

If you dont want to download that, please install POTRACE to your 
system manually and assign it to your PATH env variable properly.
"""
POS_PROMPT = ",(((vector graphic))), (((black white, line art))), atari graphic"
NEG_PROMPT = ",background, colors, shading, details"
PO_URL     = "https://potrace.sourceforge.net/download/1.16/potrace-1.16.win64.zip"
PO_ZIP     = "potrace.zip"
PO_ZIP_EXE = "potrace-1.16.win64/potrace.exe"
PO_EXE     = "scripts/potrace.exe"

##########################################################################

import os
import pathlib
import subprocess
from zipfile import ZipFile
import requests
import glob
import os.path
from sys import platform

import modules.scripts as scripts
import modules.images as Images
import gradio as gr

from modules.processing import Processed, process_images
from modules.shared import opts

class Script(scripts.Script):
    def title(self):
        return "Text to Vectorgraphics"

    def ui(self, is_img2img):
        poFormat = gr.Dropdown(["svg","pdf"], label="Output format", value="svg")
        poOpaque = gr.Checkbox(label="White is Opaque", value=True)
        poTight = gr.Checkbox(label="Cut white margin from input", value=True)
        poKeepPnm = gr.Checkbox(label="Keep temp images", value=False)
        poThreshold = gr.Slider(label="Threshold", minimum=0.0, maximum=1.0, step=0.05, value=0.5)

        return [poFormat,poOpaque, poTight, poKeepPnm, poThreshold]

    def run(self, p, poFormat, poOpaque, poTight, poKeepPnm, poThreshold):
        PO_TO_CALL = self.check_protrace_install()

        p.do_not_save_grid = True

        # make SD great b/w stuff
        p.prompt += POS_PROMPT
        p.negative_prompt += NEG_PROMPT

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

        try:
            # vectorize
            for i,img in enumerate(images[::-1]): 
                fullfn = files[i]
                fullofpnm = pathlib.Path(fullfn).with_suffix('.pnm')
                fullof = pathlib.Path(fullfn).with_suffix('.'+poFormat)

                img.save(fullofpnm)

                args = [PO_TO_CALL,  "-b", poFormat, "-o", fullof, "--blacklevel", format(poThreshold, 'f')]
                if poOpaque: args.append("--opaque")
                if poTight: args.append("--tight")
                args.append(fullofpnm)

                p2 = subprocess.Popen(args)

                if not poKeepPnm:
                    p2.wait()
                    os.remove(fullofpnm)

        except (Exception):
            raise Exception("TXT2Vectorgraphics: Execution of Protrace failed, check filesystem, permissions, installation or settings")

        return Processed(p, images, p.seed, "")

    def check_protrace_install(self) -> str:
        # For Linux, run potrace from installed binary
        if platform == "linux" or platform == "linux2":
            try:
                # check whether already in PATH 
                checkPath = subprocess.Popen(["potrace","-v"])
                checkPath.wait()
                return "potrace"
            except (Exception):
                raise Exception("Cannot find installed Protrace. Please run `sudo apt install potrace`")
                    
        # prefer local potrace over that from PATH
        elif platform == "win32":
            if not os.path.exists(PO_EXE):
                try:
                    # check whether already in PATH 
                    checkPath = subprocess.Popen(["potrace","-v"])
                    checkPath.wait()
                    return "potrace"

                except (Exception):
                    try:
                        # try to download protrace and unzip locally into "scripts"
                        if not os.path.exists(PO_ZIP):
                            r = requests.get(PO_URL)
                            with open(PO_ZIP, 'wb') as f:
                                f.write(r.content) 

                        with ZipFile(PO_ZIP, 'r') as zipObj:
                            exe = zipObj.read(PO_ZIP_EXE)
                            with open(PO_EXE,"wb") as e:
                                e.write(exe)
                                zipObj.close()
                                os.remove(PO_ZIP)
                    except:
                        raise Exception("Cannot find and or download/extract Protrace. Provide protrace in script folder. ")
        return PO_EXE
