#!/usr/bin/env python

import os
import random
import argparse
from pathlib import Path


__version__ = '0.3.0'


INPUT_FOLDER = 'input'
INTRO_FOLDER = 'intros'
OUTRO_FOLDER = 'outros'
OUTPUT_FOLDER = 'output'


def get_parser() -> argparse.ArgumentParser:
    """Return argument parser for this script."""
    parser = argparse.ArgumentParser(description='batch add intros and outros to videos with ffmpeg')
    parser.add_argument('--version', action='version', version=__version__)
    return parser


def add_intro_outro(video_path: Path, intro_path: Path, outro_path: Path, out_folder_path: Path):
    """Add intro and outro to video and save to the out folder, using ffmpeg's concat demuxer."""
    out_file_path = out_folder_path / video_path.name
    concat_file_path = out_file_path.with_stem(video_path.stem + '-concat').with_suffix('.txt')
    with open(concat_file_path, 'w') as concat_file:
        concat_file.write(
            f"file '{intro_path.resolve().as_posix()}'\n"
            f"file '{video_path.resolve().as_posix()}'\n"
            f"file '{outro_path.resolve().as_posix()}'\n"
        )

    command = f'ffmpeg -y -f concat -safe 0 -i {concat_file_path} -c:v copy -c:a copy {out_file_path}'
    os.system(command)

    concat_file_path.unlink()


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
