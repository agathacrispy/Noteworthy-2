import argparse
from pathlib import Path

from preprocessing.convert import mp3_to_wav


def parse_args():
    parser = argparse.ArgumentParser(
        description="Preprocess a song for Noteworthy."
    )

    parser.add_argument(
        "input",
        help="Path to the input .wav or .mp3 file"
    )

    parser.add_argument(
        "--model",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: medium)"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    path = Path(args.input)

    if not path.exists():
        print(f"file not found: {path}")
        return

    if path.suffix.lower() not in (".wav", ".mp3"):
        print(f"unsupported file type '{path.suffix}'. Must be .wav or .mp3.")
        return

    if path.suffix.lower() == ".mp3":
        mp3_to_wav(path)
        

if __name__ == "__main__":
    main()
