from pathlib import Path
from pydub import AudioSegment


def mp3_to_wav(mp3_path: Path) -> Path:
    
    #convert mp3 to wav, returns path to new wav file
    #mp3 file MAY be deleted later
    
    wav_path = mp3_path.with_suffix(".wav")

    audio = AudioSegment.from_mp3(str(mp3_path))
    audio.export(str(wav_path), format="wav")
    
    mp3_path.unlink()

    return wav_path
