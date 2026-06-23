from pathlib import Path
from faster_whisper import WhisperModel


def transcribe(path: Path, model_size: str = "medium") -> list[dict]:

    #transcribe audio file using whisper, returns list of line dicts with word timestamps

    model = WhisperModel(model_size, compute_type="int8")
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

    for l in lines:
        print (l)
        
    return lines
