import argparse
from pathlib import Path

from preprocessing.separate import separate_two_stems
from preprocessing.transcribe import transcribe
from preprocessing.align import align


def parse_args():
    parser = argparse.ArgumentParser(
        description="Preprocess a song for Noteworthy."
    )

    parser.add_argument(
        "input",
        help="Path to the input .mp3 file"
    )

    parser.add_argument(
        "--lrc",
        help="Path to an .lrc file with lyrics and timestamps (optional)"
    )

    parser.add_argument(
        "--model",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: medium, ignored if --lrc is provided)"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    path = Path(args.input)

    if not path.exists():
        print(f"file not found: {path}")
        return

    if path.suffix.lower() not in (".mp3"):
        print(f"unsupported file type '{path.suffix}'. must be .mp3.")
        return

    output_dir = Path("output") / path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    vocals_path, backing_path = separate_two_stems(path, output_dir)

    if args.lrc:
        lrc_path = Path(args.lrc)
        if not lrc_path.exists():
            print(f"lrc file not found: {lrc_path}")
            return
        align(path, lrc_path, output_dir)
    else:
        transcribe(path, output_dir, args.model)


if __name__ == "__main__":
    main()
