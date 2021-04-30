const constraints = window.constraints = {
  audio: false,
  video: true
}

async function init(){
  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    const video = document.querySelector("#video");
    const videoTracks = stream.getVideoTracks();
    window.stream = stream;
    video.srcObject = stream;
    // e.target.disabled = true;
  }
  catch{
    alert("カメラ使用を許可して下さい");
  }
}

console.log(constraints)
// document.querySelector("#showVideo").addEventListener("click",e => init(e));
window.onload = init
console.log("window loaded")