# Transcriptor
Transcriptor is transcription app that transcribes any recording or an external file using OpenAI whisper. It also generates summary of the transcription and does sentiment analysis

## Local Setup
Before running this application. Please download `Docker Desktop` and `python >= 3.9` in your system and start docker desktop

Clone this repo locally and switch to this repo folder
```
https://github.com/NiteeshKMishra/Transcriptor.git
```
Run below command to download all go packages required for running this app
```
pip install -r requirements.txt
```

This app is hosted on port 8080
Create `secrets.env` at root of the directory and copy the contents of file `secrets.example.env` into `secrets.env`

Run the app with
```
FLASK_ENV=development python web.py
```

Run all tests with
```
python -m unittest discover -s tests -p "*_test.py"
```

### Running via Docker

This app can also be run via docker, use following commands run run via docker
```
docker build -t transcriptor .
docker run -p 8080:8080 transcriptor
```
