#!/usr/bin/env python

import os
import itertools
import argparse
from pathlib import Path


__version__ = '2.0.1'


INPUT_VIDEOS_FOLDER = 'input'
INPUT_AUDIO_FOLDER = 'audio'
OUTPUT_FOLDER = 'output'


def get_parser() -> argparse.ArgumentParser:
    """Return argument parser for this script."""
    parser = argparse.ArgumentParser(description='batch replace audio of videos with ffmpeg')
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument(
        '--input-videos-folder', dest='input_videos_folder', type=Path, default=INPUT_VIDEOS_FOLDER,
        help='folder from which to get videos to replace audio of'
    )
    parser.add_argument(
        '--intros-audio-folder', dest='input_audio_folder', type=Path, default=INPUT_AUDIO_FOLDER,
        help='folder to get replacement audio from'
    )
    parser.add_argument(
        '--output-folder', dest='output_folder', type=Path, default=OUTPUT_FOLDER,
        help='folder to output videos with intros and outros added'
    )

    return parser


def replace_audio(video_path: Path, audio_path: Path, out_folder_path: Path):
    """Replace audio of video and save to the out folder, using ffmpeg."""
    out_file_path = out_folder_path / video_path.name

    command = (
        'ffmpeg -y '
        f'-i "{video_path}" -i "{audio_path}" '
        '-shortest -c:v copy -c:a copy -map 0:v:0 -map 1:a:0 '
        f'"{out_file_path}"'
    )
    print(command)
    os.system(command)


def replace_in_folder(input_folder_path: Path, audio_folder_path: Path, output_folder_path: Path):
    # this will yield the next video from the folder in a loop
    audio_cycle = itertools.cycle([a for a in audio_folder_path.iterdir() if a.is_file()])

    for video in input_folder_path.iterdir():
        if not video.is_file():
            continue

        replacement_audio = next(audio_cycle)
        replace_audio(video, replacement_audio, output_folder_path)


def main():
    """Run the script."""
    args = get_parser().parse_args()

    input_folder_path = args.input_videos_folder
    audio_folder_path = args.input_audio_folder
    output_folder_path = args.output_folder
    output_folder_path.mkdir(exist_ok=True)

    replace_in_folder(input_folder_path, audio_folder_path, output_folder_path)


if __name__ == '__main__':
    main()
