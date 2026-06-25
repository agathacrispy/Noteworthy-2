import json
from pathlib import Path
from faster_whisper import WhisperModel


def transcribe(path: Path, output_dir: Path, model_size: str = "medium"):

    #transcribe audio file using whisper, writes song.json to output_dir

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(path), beam_size=5, word_timestamps=True)

    print(f"detected language '{info.language}' with probability {info.language_probability:.2f}")

    lines = []
    for segment in segments:
        words = [
            {"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)}
            for w in (segment.words or [])
        ]
        lines.append({
            "start": round(segment.start, 3),
            "end": round(segment.end, 3),
            "text": segment.text.strip(),
            "words": words,
        })

    data = {
        "name": path.stem,
        "backing_track": "backing.wav",
        "lines": lines,
    }

    out = output_dir / "song.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"exported {out}")
