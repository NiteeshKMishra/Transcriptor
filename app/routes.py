import os
import logging
import json
from datetime import datetime
from pathlib import Path
from flask import Blueprint, render_template, request

routes = Blueprint(
    'routes', __name__, url_prefix='/'
)

@routes.route("/")
def home_page():
    return render_template("home.html")

@routes.route("/transcripts")
def transcripts_page():
    logger = logging.getLogger()
    transcripts_folder="./transcripts"
    os.makedirs(transcripts_folder, mode = 0o777, exist_ok = True)

    try:
        transcript_id = request.args.get("id", "")
        if transcript_id == "":
            transcripts = []
            for p in Path(transcripts_folder).rglob('*.json'):
                transcript = json.loads(p.read_text())
                id = p.name.split(".")[0]
                transcripts.append({
                    "id": id,
                    "created_at": datetime.utcfromtimestamp(int(id)/1000).strftime('%Y-%m-%d %H:%M'),
                    "summary": transcript["summary"],
                    "sentiment": transcript["sentiment"]
                })
            data={
                "found": len(transcripts) > 0,
                "transcripts": transcripts
            }
            return render_template("transcripts.html", data=data)
        else:
            transcript_path = os.path.join(transcripts_folder, transcript_id+".json")
            data = {
                "found": True,
                "summary": "",
                "transcript": "",
                "sentiment": ""
            }
            if not os.path.exists(transcript_path):
                logger.error("path does not exists", transcript_path)
                data["found"]=False
                return render_template("transcript.html", data=data)
            with open(transcript_path, "rb") as f:
                transcript_data = json.load(f)
                data = {
                    **data,
                    **transcript_data
                }
            return render_template("transcript.html", data=data)
    except Exception as e:
        logger.error("error in transcripts_page", repr(e))
        return render_template("home.html")
