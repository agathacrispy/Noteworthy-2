from faster_whisper import WhisperModel


def transcribe(wav_path: str, model_size: str = "medium") -> list[dict]:
    """Return a list of line dicts, each with word-level timestamps."""
    model = WhisperModel(model_size, compute_type="int8")
    segments, _ = model.transcribe(wav_path, word_timestamps=True)

    lines = []
    for seg in segments:
        words = [
            {"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)}
            for w in (seg.words or [])
        ]
        lines.append({
            "start": round(seg.start, 3),
            "end": round(seg.end, 3),
            "text": seg.text.strip(),
            "words": words,
        })

    return lines
