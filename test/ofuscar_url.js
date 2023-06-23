function ofuscarUrl(url) {
  var fecha = Date.now();
  return fecha + url;
}

function getType(name) {
  var re = /(?:\.([^.]+))?$/;
  var nameEx = re.exec(name)[1];
  var type = "";
  extensionsVideo = ["m4v", "avi", "mpg", "mp4", "webm"];
  extensionsImage = ["jpg", "gif", "bmp", "png"];

  for (var i = 0; i < extensionsVideo.length; i++) {
    if (nameEx == extensionsVideo[i]) {
      type = "video";
    }
  }
  for (var i = 0; i < extensionsImage.length; i++) {
    if (nameEx == extensionsImage[i]) {
      type = "image";
    }
  }
  if (type == "") {
    alert("tipo de archivo no soportado");
    return "None";
  }
  return type;
}

function showSubmit() {
  if (document.getElementById("file").value == "") {
    alert("tienes que seleccionar un fichero");
    return;
  } else {
    document.getElementById("botonSubmit").style.visibility = "visible";
  }
}

console.log(ofuscarUrl("cors.txt"))
console.log(getType("cars.avi"))
console.log(getType("mochila.png"))
