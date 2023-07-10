function setCommunityTweets(avatar, user_id) {
  var result = "";
  var tweets;
  var length = 0;
  var url;
  var type;

  // var nombre = sessionStorage.getItem("name");
  // igual con el user
  // var avatar = sessionStorage.getItem("avatar");

  var urlBucket = "http://twitter-clone-utad.s3.us-east-1.amazonaws.com/";

  // var user_id = sessionStorage.getItem("user_id");
  // Obtenemos tweets y los renderizamos
  // Para cada tweet tendremos que obtener su media si lo tiene
  var asd = $.get(
    "https://2l3v6ehnpnxp7aml6o53jhypoy0hyrnb.lambda-url.us-east-1.on.aws/",
    {
      method: "get-tweets-community",
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
      tweets = json.tweets;
      length = tweets.length;
    }
  ).done(function () {
    // Iteramos por todos los tweets, miramos su attachement_id
    // Null -> TextTweet
    // x -> mandamos peticion -> ImageTweet o VideoTweet

    alert(length + " tweets encontrados.");
    console.log(tweets);
    for (let i = 0; i < length; i++) {
      var newDiv = document.createElement("div");
      newDiv.setAttribute("id", "tweet-" + i);
      document.getElementById("tweets").appendChild(newDiv);

      var avatar;
      var user;
      var nombre;

      // Tenemos que obtener los datos del usuario que ha hecho el tweet
      var asd = $.get(
        "https://awqo27cndeqwcogqdzkj7bpxqi0ukkxo.lambda-url.us-east-1.on.aws/",
        {
          method: "get-user-data",
          user_id: tweets[i].user_id,
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
          profile = json.profile;
        }
      ).done(function () {
        if (result == "ok") {
          // alert("Usuario cargado correctamente.");
          avatar = profile.avatar;
          user = profile.username;
          nombre = profile.name;
        } else if (result == "fail") {
          alert("Fallo al cargar el usuario.");
        }
      });

      if (tweets[i].attachment_id == null) {
        console.log("Creamos tweet " + i + " sin attachment");
        console.log("iteracion " + i + "");
        console.log(
          nombre,
          user,
          tweets[i].created_at,
          tweets[i].message,
          avatar,
          tweets[i].user_id,
          tweets[i].message_id
        );
        var myTweet = new PlainTweet(
          nombre,
          user,
          tweets[i].created_at,
          tweets[i].message,
          avatar,
          tweets[i].user_id,
          tweets[i].message_id
        );
        document.getElementById("tweet-" + i).innerHTML = myTweet.render();
      } else {
        console.log("Creamos tweet " + i + " con attachment");
        console.log("iteracion1 " + i + "");
        // Conseguimos attachment data
        var asd = $.get(
          "https://izrlvbgc73h7aoakrx2u4b2x740cyyuq.lambda-url.us-east-1.on.aws/",
          {
            method: "get_attachment",
            attachment_id: tweets[i].attachment_id,
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
            // Ojo hay que sumarle la url del bucket para conseguir la url completa
            url = urlBucket + json.attachment.url;
            type = json.attachment.type;
            console.log(url, type);
          }
        ).done(function () {
          // Miramos tipo video o image
          if (result == "ok") {
            if (type == "image") {
              console.log("image");
              console.log("iteracion2 " + i + "");
              console.log(tweets[i]);
              console.log(
                nombre,
                user,
                tweets[i].created_at,
                tweets[i].message,
                avatar,
                tweets[i].user_id,
                tweets[i].message_id,
                url
              );
              var myTweet = new ImageTweet(
                nombre,
                user,
                tweets[i].created_at,
                tweets[i].message,
                avatar,
                tweets[i].user_id,
                tweets[i].message_id,
                url
              );
              document.getElementById("tweet-" + i).innerHTML =
                myTweet.render();
            } else if (type == "video") {
              console.log("video");
              var myTweet = new VideoTweet(
                nombre,
                user,
                tweets[i].created_at,
                tweets[i].message,
                avatar,
                tweets[i].user_id,
                tweets[i].message_id,
                url
              );
              document.getElementById("tweet-" + i).innerHTML =
                myTweet.render();
            }
          } else if (result == "fail") {
            alert("Fallo al cargar el adjunto.");
          }
        });
      }
    }
  });
}
