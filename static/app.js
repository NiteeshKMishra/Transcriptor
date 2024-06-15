function startRecording() {
    audioRecorder.resetRecordingProperties()
    const startBtn = document.getElementById("startbtn")
    const stopBtn = document.getElementById("stopbtn")
    const heading = document.getElementById("heading")
    const timer = document.getElementById("timer")
    let transcribeBtn = document.getElementById("transcribe-btn")
    let audioEle = document.getElementById("recording")
    while (audioEle.firstChild) {
        audioEle.removeChild(audioEle.lastChild);
    }
    transcribeBtn.removeAttribute("filename")


    startBtn.classList.add("display-none")
    transcribeBtn.classList.add("display-none")
    audioEle.classList.add("display-none")
    stopBtn.classList.remove("display-none")
    timer.classList.remove("display-none")
    heading.innerText = "Recording..."

    audioRecorder.start()
        .then(() => {
            handleElapsedTime(new Date())
        })
        .catch(error => {
            if (error.message.includes("mediaDevices API or getUserMedia method is not supported in this browser.")) {
                console.log("To record audio, use browsers like Chrome and Firefox.");
            }
        });
}

function stopRecordingAndSave() {
    const startBtn = document.getElementById("startbtn")
    const stopBtn = document.getElementById("stopbtn")
    const heading = document.getElementById("heading")
    const timer = document.getElementById("timer")

    stopBtn.classList.add("display-none")
    timer.classList.add("display-none")
    startBtn.classList.remove("display-none")
    heading.innerText = "Start Recording"

    audioRecorder.stop()
        .then((audioBlob) => {
            if(audioRecorder.elapsedTimer) {
                clearInterval(audioRecorder.elapsedTimer)
                audioRecorder.elapsedTimer = null
            }
            const filename = Date.now().toString()

            let data = new FormData();
            data.append('file', audioBlob);
            data.append('filename', filename);

            fetch("/save", {
                method: "POST",
                body: data,
            }).then(res => res.json()).then((res) => {
                if(res.message == "success") {
                    let transcribeBtn = document.getElementById("transcribe-btn")
                    transcribeBtn.classList.remove("display-none")
                    transcribeBtn.setAttribute("filename", filename)

                    let audioEle = document.getElementById("recording")
                    audioEle.classList.remove("display-none")

                    srcEle = document.createElement("source")
                    audioEle.appendChild(srcEle)

                    let reader = new FileReader();
                    reader.onload = (e) => {
                        let base64URL = e.target.result;
                        srcEle.src = base64URL;
                        let BlobType = audioBlob.type.includes(";") ?
                            audioBlob.type.substr(0, audioBlob.type.indexOf(';')) : audioBlob.type;
                        srcEle.type = BlobType
                        audioEle.load();
                        audioEle.play();
                    }
                    reader.readAsDataURL(audioBlob)
                }
            })
        })
        .catch(error => {
            console.log("An error occured with the error name " + error.name);
        });
}

function computeElapsedTime(startTime) {
    let endTime = new Date();
    let timeDiff = endTime - startTime;
    timeDiff = timeDiff / 1000;
    let seconds = Math.floor(timeDiff % 60);
    seconds = seconds < 10 ? "0" + seconds : seconds;
    timeDiff = Math.floor(timeDiff / 60);

    let minutes = timeDiff % 60;
    minutes = minutes < 10 ? "0" + minutes : minutes;

    timeDiff = Math.floor(timeDiff / 60);

    let hours = timeDiff % 24;
    timeDiff = Math.floor(timeDiff / 24);
    let days = timeDiff;

    let totalHours = hours + (days * 24);
    totalHours = totalHours < 10 ? "0" + totalHours : totalHours;

    if (totalHours === "00") {
        return minutes + ":" + seconds;
    } else {
        return totalHours + ":" + minutes + ":" + seconds;
    }
}

function handleElapsedTime(startDate) {
    displayElapsedTime("00:00");
    audioRecorder.elapsedTimer = setInterval(() => {
        let elapsedTime = computeElapsedTime(startDate);
        displayElapsedTime(elapsedTime);
    }, 1000);
}

function displayElapsedTime(elapsedTime) {
    const timer = document.getElementById("timer")
    timer.innerHTML = elapsedTime;
    let elapsedTimeSplitted = elapsedTime.split(":");
    let minutes = elapsedTimeSplitted.length > 2 ? Number(elapsedTimeSplitted[1]) : Number(elapsedTimeSplitted[0])
    if (minutes > 30) {
        stopRecordingAndSave();
    }
}

function transcribeRecording() {
    let transcribeBtn = document.getElementById("transcribe-btn")
    let id = transcribeBtn.getAttribute("filename")
    fetch(`/transcribe/${id}`, {
        method: "POST",
    }).then((res) => res.json()).then((res) => {
        if(res.message === "success") {
            location.assign(location.href+"/transcripts/"+id)
        }
    }).catch((err) => {
        console.log("error in transcribing")
    })
}

function navigate(id) {
    location.assign(location.href+"?id="+id)
}
