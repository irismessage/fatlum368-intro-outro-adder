#!/usr/bin/env python

import os
import random
import argparse
from pathlib import Path


# todo: add folders etc. as argparse options


__version__ = '0.4.0'


INPUT_FOLDER = 'input'
INTRO_FOLDER = 'intros'
OUTRO_FOLDER = 'outros'
OUTPUT_FOLDER = 'output'
RESOLUTION = '1280:720'


def get_parser() -> argparse.ArgumentParser:
    """Return argument parser for this script."""
    parser = argparse.ArgumentParser(description='batch add intros and outros to videos with ffmpeg')
    parser.add_argument('--version', action='version', version=__version__)
    return parser


def add_intro_outro(
        video_path: Path, intro_path: Path, outro_path: Path, out_folder_path: Path, resolution: str = RESOLUTION
):
    """Add intro and outro to video and save to the out folder, using ffmpeg's concat demuxer.

    Resolution should be in the form width:height eg '1280:720'
    """
    out_file_path = out_folder_path / video_path.name
    # original: https://video.stackexchange.com/questions/28153/batch-add-intro-and-outro-to-videos
    # ffmpeg -y -i %INTRO% -i "%%a" -filter_complex
    # "[0:v]scale=1280:720:force_original_aspect_ratio=1,pad=1280:720:(ow-iw)/2:(oh-ih)/2[v0];
    # [1:v]scale=1280:720:force_original_aspect_ratio=1,pad=1280:720:(ow-iw)/2:(oh-ih)/2[v1];
    # [v0][0:a][v1][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" %OUTPUT_FOLDER%\\%%~na.mp4"
    command = (
        'ffmpeg -y '
        f'-i "{intro_path}" '
        f'-i "{video_path}" '
        f'-i "{outro_path}" '
        '-filter_complex "'
        f'[0:v]scale={resolution}:force_original_aspect_ratio=1,pad={resolution}:(ow-iw)/2:(oh-ih)/2[v0]; '
        f'[1:v]scale={resolution}:force_original_aspect_ratio=1,pad={resolution}:(ow-iw)/2:(oh-ih)/2[v1]; '
        f'[2:v]scale={resolution}:force_original_aspect_ratio=1,pad={resolution}:(ow-iw)/2:(oh-ih)/2[v2]; '
        '[v0][0:a][v1][1:a][v2][2:a]concat=n=3:v=1:a=1[v][a]'
        '" '
        '-map "[v]" '
        '-map "[a]" '
        f'"{out_file_path}"'
    )
    print(command)
    os.system(command)


def main():
    """Run the script."""
    get_parser().parse_args()

    input_folder_path = Path(INPUT_FOLDER)
    intro_folder_path = Path(INTRO_FOLDER)
    outro_folder_path = Path(OUTRO_FOLDER)
    output_folder_path = Path(OUTPUT_FOLDER)
    output_folder_path.mkdir(exist_ok=True)

    intro_paths = [p for p in intro_folder_path.iterdir() if p.is_file()]
    outro_paths = [p for p in outro_folder_path.iterdir() if p.is_file()]

    for video in input_folder_path.iterdir():
        if not video.is_file():
            continue

        selected_intro = random.choice(intro_paths)
        selected_outro = random.choice(outro_paths)
        add_intro_outro(video, selected_intro, selected_outro, output_folder_path)


if __name__ == '__main__':
    main()
