import subprocess
import shutil
from pathlib import Path


def separate_vocals(wav_path: str, output_dir: str) -> str:
    """
    Run Demucs to split vocals from backing track.
    Returns the path to the backing (no_vocals) wav.
    """
    wav = Path(wav_path)
    out = Path(output_dir)

    subprocess.run(
        ["python", "-m", "demucs", "--two-stems=vocals", "-o", str(out), str(wav)],
        check=True,
    )

    backing_src = out / "htdemucs" / wav.stem / "no_vocals.wav"
    backing_dst = out / "backing.wav"
    shutil.move(str(backing_src), str(backing_dst))

    shutil.rmtree(out / "htdemucs", ignore_errors=True)

    return str(backing_dst)
