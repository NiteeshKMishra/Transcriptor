var audioRecorder = {
    audioBlobs: [],
    mediaRecorder: null,
    streamBeingCaptured: null,
    elapsedTimer: null,
    start: async function () {
            if (!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
                return Promise.reject(new Error('mediaDevices API or getUserMedia method is not supported in this browser.'));
            }
            else {
                return navigator.mediaDevices.getUserMedia({ audio: true })
                    .then(stream => {
                        this.streamBeingCaptured = stream;
                        this.mediaRecorder = new MediaRecorder(stream, {mimeType: "audio/webm; codecs=opus", audioBitsPerSecond: 32000});
                        this.audioBlobs = [];
                        this.mediaRecorder.addEventListener("dataavailable", event => {
                            this.audioBlobs.push(event.data);
                        });
                        this.mediaRecorder.start();
                });
            }
    },
    stop: async function () {
        return new Promise(resolve => {
             this.mediaRecorder.addEventListener("stop", (event) => {
                let mimeType = event.srcElement.mimeType;
                let audioBlob = new Blob(this.audioBlobs, { type: mimeType });
                resolve(audioBlob);
            });

        this.mediaRecorder.stop();
        this.stopStream();
        this.resetRecordingProperties();
        });
    },
    stopStream: function() {
        if(this.streamBeingCaptured) {
            this.streamBeingCaptured.getTracks()
                    .forEach(track => track.stop());
        }
    },
    resetRecordingProperties: function () {
        this.stopStream();
        this.mediaRecorder = null;
        this.streamBeingCaptured = null;
    }
}
