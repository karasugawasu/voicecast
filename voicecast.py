#!/usr/bin/env python3.11
import requests
import os
import json
import time
import tempfile
import argparse
from dotenv import load_dotenv

load_dotenv()

def synthesize_and_cast(text, speaker_id, device_ip, upload_url_base, auth_user, auth_pass,
                        volume, speed, intonation):
    host = "http://127.0.0.1:50021"

    query = requests.post(
        f"{host}/audio_query",
        params={"text": text, "speaker": speaker_id}
    ).json()

    query["volumeScale"] = volume
    query["speedScale"] = speed
    query["intonationScale"] = intonation

    wav_data = requests.post(
        f"{host}/synthesis",
        params={"speaker": speaker_id},
        data=json.dumps(query),
        headers={"Content-Type": "application/json"}
    ).content

    ts = int(time.time())
    filename = f"voice_{ts}.wav"
    upload_url = f"{upload_url_base}/{filename}"

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
        tmp_wav.write(wav_data)
        tmp_wav.flush()
        local_path = tmp_wav.name

    with open(local_path, "rb") as f:
        requests.put(
            upload_url,
            data=f,
            auth=(auth_user, auth_pass),
            headers={"Content-Type": "audio/wav"}
        )

    os.system(f'catt -d {device_ip} cast "{upload_url}"')

    time.sleep(10)

    requests.delete(upload_url, auth=(auth_user, auth_pass))
    os.remove(local_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cast VOICEVOX-generated speech to Google Home via dufs")
    parser.add_argument("text", help="Text to be spoken")
    parser.add_argument("--volume", type=float, help="Volume scale (e.g. 1.8)")
    parser.add_argument("--speed", type=float, help="Speed scale (e.g. 1.0)")
    parser.add_argument("--intonation", type=float, help="Intonation scale (e.g. 1.2)")
    args = parser.parse_args()

    volume_scale = args.volume or float(os.getenv("VOLUME_SCALE", 1.0))
    speed_scale = args.speed or float(os.getenv("SPEED_SCALE", 1.0))
    intonation_scale = args.intonation or float(os.getenv("INTONATION_SCALE", 1.0))

    synthesize_and_cast(
        text=args.text,
        speaker_id=int(os.getenv("SPEAKER_ID", 9)),
        device_ip=os.getenv("DEVICE_IP"),
        upload_url_base=os.getenv("UPLOAD_URL"),
        auth_user=os.getenv("AUTH_USER"),
        auth_pass=os.getenv("AUTH_PASS"),
        volume=volume_scale,
        speed=speed_scale,
        intonation=intonation_scale
    )

