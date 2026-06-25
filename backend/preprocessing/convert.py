from pathlib import Path
from pydub import AudioSegment


def mp3_to_wav(mp3_path: Path) -> Path:
    
    #convert mp3 to wav, returns path to new wav file
    
    wav_path = mp3_path.with_suffix(".wav")

    audio = AudioSegment.from_mp3(str(mp3_path))
    audio.export(str(wav_path), format="wav")
    
    mp3_path.unlink()

    return wav_path

def wav_to_mp3(wav_path: Path) -> Path:
    
    mp3_path = wav_path.with_suffix(".mp3")

    audio = AudioSegment.from_mp3(str(wav_path))
    audio.export(str(mp3_path), format="wav")
    
    wav_path.unlink()

    return mp3_path