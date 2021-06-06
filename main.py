#!/usr/bin/env python

import random
from pathlib import Path
import ffmpeg


INPUT_FOLDER = 'input'
INTRO_FOLDER = 'intros'
OUTRO_FOLDER = 'outros'
OUTPUT_FOLDER = 'output'


def add_intro_outro(video_path: Path, intro_path: Path, outro_path: Path, out_folder_path: Path):
    out_file_path = out_folder_path / video_path.name
    concat_file_path = out_file_path.with_stem(video_path.stem + '-concat').with_suffix('.txt')
    with open(concat_file_path, 'w') as concat_file:
        concat_file.write(
            f"file '{video_path}'"
            f"file '{intro_path}'"
            f"file '{outro_path}'\n"
        )

    stream = ffmpeg.input(str(concat_file), format='concat', safe=0)
    stream = ffmpeg.output(stream, str(out_file_path), c='copy')
    ffmpeg.run(stream)


def main():
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
