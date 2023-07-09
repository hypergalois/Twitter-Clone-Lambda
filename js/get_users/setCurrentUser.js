function setCurrentUser() {
  var result = "";

  // Lo vuelvo a obtener dentro, tengo que obtenerlo porque lo de arriba no se ejecuta
  var avatar = sessionStorage.getItem("avatar");
  var nombre = sessionStorage.getItem("name");

  // console.log(sessionStorage.getItem('avatar'))
  // console.log(sessionStorage.getItem('name'))

  if (sessionStorage.getItem("avatar") && sessionStorage.getItem("name")) {
    document.getElementById("avatarCurrent").src = avatar;
    document.getElementById("nameCurrent").innerHTML = nombre;
    document.getElementById("usernameCurrent").innerHTML = "@" + user;
    alert("Obteniendo avatar y nombre de caché.");
    return;
  }

  var asd = $.get(
    "https://g57gbf3yj5pwd3wt27zpa2viwu0ufnwy.lambda-url.us-east-1.on.aws/",
    {
      method: "get_user",
      user_id: user_id,
    },
    function (data) {
      function jsonEscape(str) {
        return str
          .replace(/\n/g, "\\\\n")
          .replace(/\r/g, "\\\\r")
          .replace(/\t/g, "\\\\t")
          .replace(/\\/g, "");
      }
      var json = data;
      result = json.res;
      avatar = json.avatar;
      nombre = json.name;
    }
  ).done(function () {
    if (result == "ok") {
      // Asignamos
      document.getElementById("avatarCurrent").src = avatar;
      document.getElementById("nameCurrent").innerHTML = nombre;
      document.getElementById("usernameCurrent").innerHTML = "@" + user;
      // Ponerlos en Session Storage

      sessionStorage.setItem("avatar", avatar);
      sessionStorage.setItem("name", nombre);
    } else if (result == "fail") {
      alert("Error.");
    }
  });
}
