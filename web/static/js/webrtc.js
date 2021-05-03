const constraints =window.constraints = {
  audio: false,
  video: {
    facingMode: "user"
  }
}

async function init(){
  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    const video = document.querySelector("#video");
    const videoTracks = stream.getVideoTracks();
    window.stream = stream;
    video.srcObject = stream;
  }
  catch{
    alert("カメラ使用を許可して下さい");
  }
}

window.onload = init;