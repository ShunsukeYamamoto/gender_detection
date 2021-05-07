var video = document.getElementById("video")
var canvas = document.getElementById("canvas")
var img = document.getElementById("detect")

video.addEventListener("loadedmetadata",function(e){
  var width = canvas.width = video.videoWidth
  var height = canvas.height = video.videoHeight
  
  var ctx = canvas.getContext("2d")

  var data = new FormData()
  
  setInterval(function(){
    ctx.drawImage(video,0,0,width,height)
    canvas.toBlob(function(blob){
      data.set("video",blob)
      $.ajax({
        url: "/get_frame",
        type: "POST",
        processData: false,
        contentType: false,
        data: data,
        dataType: "text"
      })
      .done(function(data){
        var img_src = "data:image/jpeg;base64," + data
        console.log(img_src)
        img.src = img_src
      })
    },"image/jpeg")
  },100)
})