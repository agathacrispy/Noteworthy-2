import subprocess
import shutil
from pathlib import Path

from preprocessing.convert import wav_to_mp3

def separate_two_stems(wav_path: Path, output_dir: Path) -> tuple[Path, Path]:

    #separate vocals from backing track using demucs
    #outputs vocals.mp3 and backing.mp3 directly to output_dir

    subprocess.run(
        ["python", "-m", "demucs", "--two-stems=vocals", "--out", str(output_dir), str(wav_path)],
        check=True,
    )

    stem = output_dir / "htdemucs" / wav_path.stem

    vocals_path = output_dir / "vocals.wav"
    backing_path = output_dir / "backing.wav"

    shutil.move(str(stem / "vocals.wav"), str(vocals_path))
    shutil.move(str(stem / "no_vocals.wav"), str(backing_path))

    shutil.rmtree(output_dir / "htdemucs", ignore_errors=True)

    return vocals_path, backing_path
