import json
from pathlib import Path


def export(lines: list[dict], backing_path: str, output_dir: str, song_name: str):
    """Write the final song.json consumed by Godot."""
    data = {
        "name": song_name,
        "backing_track": "backing.wav",
        "lines": lines,
    }

    out = Path(output_dir) / "song.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out}")
