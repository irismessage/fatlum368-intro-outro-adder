#!/usr/bin/env python

import os
import random
import argparse
from pathlib import Path


__version__ = '1.0.0'


INPUT_FOLDER = 'input'
INTRO_FOLDER = 'intros'
OUTRO_FOLDER = 'outros'
OUTPUT_FOLDER = 'output'
RESOLUTION = '1280:720'


def get_parser() -> argparse.ArgumentParser:
    """Return argument parser for this script."""
    parser = argparse.ArgumentParser(description='batch add intros and outros to videos with ffmpeg')
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument(
        '--input-folder', dest='input_folder', type=Path, default=INPUT_FOLDER,
        help='folder from which to get videos to add intros and outros to'
    )
    parser.add_argument(
        '--intros-folder', dest='intros_folder', type=Path, default=INTRO_FOLDER,
        help='folder to randomly select intros from'
    )
    parser.add_argument(
        '--outros-folder', dest='outros_folder', type=Path, default=OUTRO_FOLDER,
        help='folder to randomly select outros from'
    )
    parser.add_argument(
        '--output-folder', dest='output_folder', type=Path, default=OUTPUT_FOLDER,
        help='folder to output videos with intros and outros added'
    )
    parser.add_argument(
        '--resolution', dest='resolution', default=RESOLUTION,
        help='output resolution in the form width:height'
    )

    return parser


def add_intro_outro(
        video_path: Path, intro_path: Path, outro_path: Path, out_folder_path: Path, resolution: str
):
    """Add intro and outro to video and save to the out folder, using ffmpeg's concat filter.

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
        '-vsync 2 '
        '-map "[v]" '
        '-map "[a]" '
        f'"{out_file_path}"'
    )
    print(command)
    os.system(command)


def add_to_folders(
        input_folder_path: Path, intro_folder_path: Path, outro_folder_path: Path, output_folder_path: Path,
        resolution: str
):
    intro_paths = [p for p in intro_folder_path.iterdir() if p.is_file()]
    outro_paths = [p for p in outro_folder_path.iterdir() if p.is_file()]

    for video in input_folder_path.iterdir():
        if not video.is_file():
            continue

        selected_intro = random.choice(intro_paths)
        selected_outro = random.choice(outro_paths)
        add_intro_outro(video, selected_intro, selected_outro, output_folder_path, resolution)


def main():
    """Run the script."""
    args = get_parser().parse_args()

    input_folder_path = args.input_folder
    intro_folder_path = args.intros_folder
    outro_folder_path = args.outros_folder
    output_folder_path = args.output_folder
    output_folder_path.mkdir(exist_ok=True)

    resolution = args.resolution

    add_to_folders(input_folder_path, intro_folder_path, outro_folder_path, output_folder_path, resolution)


if __name__ == '__main__':
    main()
