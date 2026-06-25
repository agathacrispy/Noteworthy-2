import json
import re
from pathlib import Path

import whisperx


def _parse_lrc(lrc_path: Path) -> list[dict]:

    #parse lrc file into list of {start, text} dicts

    lines = []
    pattern = re.compile(r"\[(\d+):(\d+\.\d+)\](.*)")

    for raw in lrc_path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(raw.strip())
        if match:
            minutes, seconds, text = match.groups()
            start = int(minutes) * 60 + float(seconds)
            text = text.strip()
            if text:
                lines.append({"start": start, "text": text})

    return lines


def align(audio_path: Path, lrc_path: Path, output_dir: Path):

    #align lrc lyrics to audio using whisperx forced alignment
    #writes song.json to output_dir

    lrc_lines = _parse_lrc(lrc_path)

    audio = whisperx.load_audio(str(audio_path))
    model, metadata = whisperx.load_align_model(language_code="en", device="cpu")

    lines = []
    for i, line in enumerate(lrc_lines):
        start = line["start"]
        end = lrc_lines[i + 1]["start"] if i + 1 < len(lrc_lines) else start + 10

        #build a whisperx-compatible segment for this line
        segment = {"start": start, "end": end, "text": line["text"]}
        result = whisperx.align([segment], model, metadata, audio, device="cpu")

        words = [
            {"word": w["word"].strip(), "start": round(w["start"], 3), "end": round(w["end"], 3)}
            for w in result["word_segments"]
            if "start" in w and "end" in w
        ]

        lines.append({
            "start": round(start, 3),
            "end": round(end, 3),
            "text": line["text"],
            "words": words,
        })

        print(f"aligned: {line['text']}")

    data = {
        "name": audio_path.stem,
        "backing_track": "backing.wav",
        "lines": lines,
    }

    out = output_dir / "song.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"exported {out}")
