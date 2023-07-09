function setProfileData() {
  var avatarProfile;
  var nameProfile;
  var bioProfile;
  var dateProfile;
  var usernameProfile;
  var result;

  // Boton editar vs follow
  var user_id = sessionStorage.getItem("user_id");
  var clicked_user_id = sessionStorage.getItem("clicked_user_id");

  // <button id="edit_profile_follow_button" class="button--large button-filled text-bold mt-10 center" onclick="document.location.replace('editprofile.html')">Edit profile/Follow</button>

  if (user_id == clicked_user_id) {
    // Edit profile
    document.getElementById("edit_profile_follow_button").innerHTML =
      "Edit profile";
    document
      .getElementById("edit_profile_follow_button")
      .setAttribute("onclick", 'document.location.replace("editprofile.html")');
  } else {
    // Follow
    document.getElementById("edit_profile_follow_button").innerHTML = "Follow";
    document
      .getElementById("edit_profile_follow_button")
      .setAttribute("onclick", "handleFollow()");
  }

  var asd = $.get(
    "https://6i7lime5c42iizxg3p6thm4qdi0ebvrk.lambda-url.us-east-1.on.aws/",
    {
      method: "get-profile-data",
      user_id: clicked_user_id,
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
      avatarProfile = json.profile.avatar;
      nameProfile = json.profile.name;
      bioProfile = json.profile.biography;
      dateProfile = json.profile.created_at;
      usernameProfile = json.profile.username;
    }
  ).done(function () {
    if (result == "ok") {
      // Cambiamos los datos del html
      // Falta sumarle el urlBucket
      $("#avatar-profile").attr("src", avatarProfile);
      $("#name-profile").text(nameProfile);
      $("#username-profile").text("@" + usernameProfile);
      $("#date-profile").text("Cuenta creada el " + dateProfile);
      $("#bio-profile").text(bioProfile);
      // alert('Datos del perfil obtenidos.')
    } else if (result == "fail") {
      alert("Error al obtener datos del perfil.");
    }
  });
}
