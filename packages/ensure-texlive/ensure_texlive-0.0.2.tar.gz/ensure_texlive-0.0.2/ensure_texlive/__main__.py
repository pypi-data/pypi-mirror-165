#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
import requests
import shutil
import zipfile
import functools
import platform
import sys
import subprocess


# download_file function taken from https://stackoverflow.com/a/39217788
def download_file(url):
    local_filename = url.split("/")[-1]
    with requests.get(url, stream=True) as resp:
        resp.raw.read = functools.partial(resp.raw.read, decode_content=True)
        with open(local_filename, "wb") as f:
            shutil.copyfileobj(resp.raw, f, length=16 * 1024 * 1024)
    return local_filename


def tlmgr_exists(strict=False, tlmgr_path=None):
    if not tlmgr_path:
        tlmgr_path = os.path.join(os.path.expanduser("~"), "texlive", "bin", "tlmgr")
    if strict:
        return shutil.which(tlmgr_path)
    return shutil.which("tlmgr")


def patch_path(dir_path):
    os.environ["PATH"] = os.environ["PATH"] + os.pathsep + dir_path


def patch_config(config_path, line):
    with open(config_path, "r", encoding="utf8") as f:
        cnt = f.read()
    lines = cnt.split("\n")
    if line not in lines:
        lines.append(line)
    cnt = "\n".join(lines)
    if not cnt.endswith("\n"):
        cnt += "\n"
    with open(config_path, "w", encoding="utf8") as f:
        f.write(cnt)


def get_single_subdir(dir_path, absolute=False):
    subdirs = [
        x for x in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, x))
    ]
    assert len(subdirs) == 1
    if absolute:
        return os.path.join(dir_path, subdirs[0])
    else:
        return subdirs[0]


def patch_path_global(texlive_bin_path):
    windows = platform.system() == "Windows"
    home_dir = os.path.expanduser("~")
    if windows:
        subprocess.run(["setx", "PATH", f"%PATH%;{texlive_bin_path}"], check=True)
    else:
        for fn in (
            os.path.join(home_dir, ".bashrc"),
            os.path.join(home_dir, ".zshrc"),
        ):
            patch_config(fn, f"export PATH=$PATH:{texlive_bin_path}")


CUSTOM_LIST = [
    "amscls",
    "amsfonts",
    "amsmath",
    "atbegshi",
    "atveryend",
    "auxhook",
    "babel",
    "bibtex",
    "bigintcalc",
    "bitset",
    "booktabs",
    "cm",
    "ctablestack",
    "dehyph",
    "dvipdfmx",
    "dvips",
    "ec",
    "epstopdf-pkg",
    "etex",
    "etexcmds",
    "etoolbox",
    "euenc",
    "everyshi",
    "fancyvrb",
    "filehook",
    "firstaid",
    "float",
    "fontspec",
    "framed",
    "geometry",
    "gettitlestring",
    "glyphlist",
    "graphics",
    "graphics-cfg",
    "graphics-def",
    "helvetic",
    "hycolor",
    "hyperref",
    "hyph-utf8",
    "iftex",
    "inconsolata",
    "infwarerr",
    "intcalc",
    "knuth-lib",
    "kvdefinekeys",
    "kvoptions",
    "kvsetkeys",
    "l3backend",
    "l3kernel",
    "l3packages",
    "latex",
    "latex-amsmath-dev",
    "latex-bin",
    "latex-fonts",
    "latex-tools-dev",
    "latexconfig",
    "latexmk",
    "letltxmacro",
    "lm",
    "lm-math",
    "ltxcmds",
    "lua-alt-getopt",
    "lua-uni-algos",
    "luahbtex",
    "lualatex-math",
    "lualibs",
    "luaotfload",
    "luatex",
    "luatexbase",
    "mdwtools",
    "metafont",
    "mfware",
    "natbib",
    "pdfescape",
    "pdftex",
    "pdftexcmds",
    "plain",
    "psnfss",
    "refcount",
    "rerunfilecheck",
    "selnolig",
    "stringenc",
    "tex",
    "tex-ini-files",
    "times",
    "tipa",
    "tools",
    "unicode-data",
    "unicode-math",
    "uniquecounter",
    "url",
    "xcolor",
    "xetex",
    "xetexconfig",
    "xkeyval",
    "xunicode",
    "zapfding",
]


PROFILE = """
selected_scheme {{scheme}}

TEXDIR {{texdir}}

TEXMFSYSCONFIG {{texdir}}/texmf-config
TEXMFLOCAL {{texdir}}/texmf-local
TEXMFSYSVAR {{texdir}}/texmf-var

option_doc 0
option_src 0
option_autobackup 0

portable 1
"""


def clear_dir(dir_path):
    for x in os.listdir(dir_path):
        full_path = os.path.join(dir_path, x)
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)


def extract_zip(zip_file):
    dirname = zip_file[:-4]
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(dirname)


def ensure_texlive(force=False, strict=False):
    initial_dir = os.getcwd()
    home_dir = os.path.expanduser("~")
    texlive_raw_bin_path = os.path.join(home_dir, "texlive", "bin")
    if os.path.isdir(texlive_raw_bin_path):
        subdir = get_single_subdir(texlive_raw_bin_path)
        texlive_bin_path = os.path.join(texlive_raw_bin_path, subdir)
        texlive_tlmgr_path = os.path.join(texlive_bin_path, "tlmgr")
    else:
        texlive_bin_path = None
        texlive_tlmgr_path = None
    existing_tlmgr = tlmgr_exists(strict=strict, tlmgr_path=texlive_tlmgr_path)
    tmp_dir = os.path.join(home_dir, ".ensure_texlive")
    target_dir = os.path.join(home_dir, "texlive")
    if texlive_tlmgr_path and os.path.isfile(texlive_tlmgr_path) and not existing_tlmgr:
        print(
            f"existing texlive installation found at {texlive_tlmgr_path} but not in path, so just patching path"
        )
        patch_path(texlive_bin_path)
        patch_path_global(texlive_bin_path)
        return
    windows = platform.system() == "Windows"
    if existing_tlmgr and not force:
        print(f"tlmgr already exists at {existing_tlmgr}, won't reinstall")
        return
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    if os.path.isdir(target_dir):
        clear_dir(target_dir)
    os.mkdir(tmp_dir)
    os.chdir(tmp_dir)
    print("downloading texlive installer zip...")
    download_file("https://mirror.ctan.org/systems/texlive/tlnet/install-tl.zip")
    extract_zip("install-tl.zip")
    os.chdir("install-tl")
    subdir = os.listdir(os.getcwd())[0]
    os.chdir(subdir)
    if windows:
        executable = "install-tl-windows.bat"
    else:
        executable = "./install-tl"
        subprocess.run(["chmod", "+x", executable], check=True)
    args = [executable, "-no-gui"]
    if windows:
        args.append("-non-admin")
    with open("tinytex.profile", "w") as f:
        f.write(
            PROFILE.replace("{{texdir}}", target_dir)
                .replace("{{scheme}}", "scheme-basic" if windows else "scheme-infraonly")
        )
    args.extend(["-profile", "tinytex.profile", "--no-interaction"])
    print("running texlive installer...")
    subprocess.run(args, check=True)
    os.chdir(home_dir)
    if not texlive_bin_path:
        subdir = get_single_subdir(texlive_raw_bin_path)
        texlive_bin_path = os.path.join(texlive_raw_bin_path, subdir)
    if windows:
        tlmgr = "tlmgr.bat"
    else:
        tlmgr = "tlmgr"
    subprocess.run([os.path.join(texlive_bin_path, tlmgr), "-version"], check=True)
    try:
        custom_list = requests.get(
            "https://tinytex.yihui.org/pkgs-custom.txt"
        ).text.split("\n")
        custom_list = [x for x in custom_list if x]
    except:
        print(
            "couldn't get pkgs-custom from tinytex.yihui.org, resorting to local copy"
        )
        custom_list = CUSTOM_LIST
    custom_list.extend(["microtype", "texliveonfly"])
    subprocess.run(
        [os.path.join(texlive_bin_path, tlmgr), "install"] + custom_list, check=True
    )
    patch_path_global(texlive_bin_path)
    print("texlive successfully installed, removing tmp directory..")
    shutil.rmtree(tmp_dir)


def main():
    ensure_texlive()


if __name__ == "__main__":
    main()
