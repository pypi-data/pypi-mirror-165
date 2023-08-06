__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import logging
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import sys
from argparse import ArgumentParser, Namespace
from collections import defaultdict
from datetime import timedelta
from functools import partial
from operator import itemgetter
from os import get_terminal_size
from pathlib import Path
from pprint import pformat
from typing import List, Dict

from media_tools.util.length_reader import (
    AudioreadLengthReader, Eyed3LengthReader, MutagenLengthReader, SoundfileLengthReader
)
from media_tools.util.logging import setup_logging

AUDIO_EXTENSIONS = ('mp3', 'ogg', 'flac', 'wav', 'm4a', 'm4b', 'm4p', 'aif', 'aiff', 'ape', 'spx')


def parse_commandline(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        description="Print length of audio files in directories"
    )
    parser.add_argument('directory', type=str, help='root directory')
    parser.add_argument(
        '-r', '--recursive', action='store_true', help='print run time for every folder'
    )
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('--max-debug-items', type=int, default=-1, help='N shortest items to print')
    return parser.parse_args(args)


class LengthStore:

    def __init__(self, root: Path, recursive: bool):
        self.root = root
        self.recursive = recursive
        self.lengths: Dict[Path, timedelta] = {}
        self.errors: Dict[Path, float] = {}
        self.backends_used: Dict[str, Dict[Path, float]] = defaultdict(dict)

    def scan(self):
        self.lengths[self.root] = self.dir_length(self.root)

    def print_metadata(self, num_entries: int = -1):
        width, _ = get_terminal_size(0)
        logging.debug(pformat({
            backend: [
                f"{track.relative_to(self.root)}: {length:.1f}s"
                for track, length in sorted(tracks.items(), key=itemgetter(1))[:num_entries]
            ]
            for backend, tracks in self.backends_used.items()
        }, width=width))

    def print_errors(self, num_entries: int = -1):
        if not self.errors:
            return
        width, _ = get_terminal_size(0)
        logging.warning('%s errors', len(self.errors))
        logging.warning(pformat([
            f"{track.relative_to(self.root)}: {size / 1024:.1f}kB"
            for track, size in sorted(self.errors.items(), key=itemgetter(1))[:num_entries]
        ], width=width))

    def dir_length(self, folder: Path, parallel: bool = True) -> timedelta:
        audio, folders = get_audio_and_folders(folder)

        length = self.sum_audio_lengths(audio)

        dir_length = partial(self.dir_length, parallel=False)
        if parallel:
            # for recursive printing of run times we need threads, else can use processes
            # using "processes=1" is the experimentally determined ideal number of threads
            with self.create_pool() as pool:
                length = sum(pool.imap_unordered(dir_length, folders), length)
        else:
            length = sum(map(dir_length, folders), length)

        if length:
            self.lengths[folder] = length

        return length

    def create_pool(self):
        return ThreadPool(processes=1) if self.recursive else Pool()

    def sum_audio_lengths(self, paths: List[Path]) -> timedelta:
        return sum([as_timedelta(self.get_duration(path)) for path in paths], timedelta(seconds=0))

    def print(self) -> None:
        max_duration = self.format_timedelta(self.lengths[self.root])
        for path, duration in sorted(self.lengths.items(), key=lambda item: item[1]):
            self.print_line(
                path if path == self.root else path.relative_to(self.root),
                self.format_timedelta(duration).rjust(len(max_duration))
            )

    @staticmethod
    def format_timedelta(duration: timedelta) -> str:
        days = duration.days
        rest = duration - timedelta(days=days)
        hours = str(rest).split('.', maxsplit=1)[0]
        return f"{days}d {hours:>8}" if days else hours

    @staticmethod
    def print_line(path: Path, duration: str) -> None:
        print(f"{duration}   {path}")

    def get_duration(self, track: Path) -> float:
        for reader_class in (
                MutagenLengthReader, Eyed3LengthReader, SoundfileLengthReader, AudioreadLengthReader
        ):
            duration = reader_class(track).get_duration()
            if duration:
                self.backends_used[reader_class.__name__][track] = duration
                return duration
        self.errors[track] = track.stat().st_size
        return 0


def is_audio(track: Path):
    return track.suffix[1:].lower() in AUDIO_EXTENSIONS and track.is_file()


def get_audio_and_folders(folder: Path):
    audio, folders = [], []
    for thing in folder.iterdir():
        if is_audio(thing):
            audio.append(thing)
        elif thing.is_dir():
            folders.append(thing)
    return audio, folders


def as_timedelta(duration: float) -> timedelta:
    try:
        return timedelta(seconds=duration)
    except OverflowError:
        return timedelta(0)


def main() -> None:
    args: List[str] = sys.argv[1:]
    opts = parse_commandline(args)
    setup_logging(opts, fmt='%(message)s')
    lengths = LengthStore(Path(opts.directory), opts.recursive)
    lengths.scan()
    lengths.print()
    if opts.debug:
        lengths.print_errors(opts.max_debug_items)
        lengths.print_metadata(opts.max_debug_items)


if __name__ == '__main__':
    main()
