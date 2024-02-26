var searchEl = document.getElementById("search-box");
var cardEl = document.getElementById("myCard1");

function handleEnterPressEvent(event) {
  if (event.key === "ENTER") {
    fetchEnteredQuery();
  }
}

function fetchEnteredQuery() {
  var userQuery = searchEl.value;
  sendUserBookRequest(userQuery);
}

function sendUserBookRequest(userQuery) {
  var csrftoken = getCookie("csrftoken");

  fetch("/search-user-book-query/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ userQuery: userQuery }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.result === "success") {
        
        window.location.href = "/available/";
      } else if (data.result === "not_found") {
        alert("Book not found!");
      }
    })
    .catch((error) => {
      console.error("Error sending data:", error);
    });
}

document.getElementById("signupBtn").addEventListener("click", function () {
  
  window.location.href = "/signup/";
});

document
  .getElementById("newArrivalCardBtn")
  .addEventListener("click", function () {
    
    window.location.href = "/newBooks/";
  });

document
  .getElementById("availableCardBtn")
  .addEventListener("click", function () {
    
    window.location.href = "/available/";
  });

document.getElementById("authorCardBtn").addEventListener("click", function () {
  
  window.location.href = "/author/";
});

document.getElementById("genreCardBtn").addEventListener("click", function () {
  
  window.location.href = "/genre/";
});

document.getElementById("loginBtn").addEventListener("click", function () {
  
  window.location.href = "/login/";
});

checkAuthenticationStatus();

function checkAuthenticationStatus() {
  fetch("/get-auth-status/")
    .then((response) => response.json())
    .then((data) => {
      console.log("Authentication status:", data.isAuthenticated);
    })
    .catch((error) => {
      console.error("Error checking authentication status:", error);
    });
}

var currentUser = localStorage.getItem("username");

var myProfile = document.getElementById("myProfile");

var modalContainer = null;

myProfile.addEventListener("click", function () {
  if (!modalContainer) {
    modalContainer = document.createElement("div");
    modalContainer.id = "modalContainer";
    modalContainer.style.position = "fixed";
    modalContainer.style.top = "50%";
    modalContainer.style.left = "50%";
    modalContainer.style.transform = "translate(-50%, -50%)";
    modalContainer.style.height = "640px";
    modalContainer.style.width = "1028px";
    modalContainer.style.borderRadius = "15px";
    modalContainer.style.border = "0.5px solid black";
    modalContainer.style.backgroundColor = "rgba(212, 244, 244, 0.6)";
    modalContainer.style.display = "flex";
    modalContainer.style.flexDirection = "column";
    modalContainer.style.justifyContent = "center";
    modalContainer.style.alignItems = "center";
  } else {
    console.log("Modal Present");
    modalContainer.style.display = "flex";
  }

  modalContainer.innerHTML = "";

  var profilePic = document.createElement("img");
  profilePic.style.width = "250px";
  profilePic.style.height = "250px";
  profilePic.style.backgroundColor = "#000";
  profilePic.style.borderRadius = "50%";
  profilePic.style.marginBottom = "50px";
  modalContainer.appendChild(profilePic);
  var object_key = `${currentUser}.jpg`;

  var username = document.createElement("h3");
  var upperCaseName = currentUser.toUpperCase();
  username.innerHTML = "Name : " + upperCaseName;
  username.style.fontSize = "30px";
  username.style.color = "black";
  username.style.fontFamily = "Roboto";
  modalContainer.appendChild(username);

  var modalCloseBtn = document.createElement("button");
  modalCloseBtn.textContent = "Close";
  modalCloseBtn.style.width = "160px";
  modalCloseBtn.style.height = "45px";
  modalCloseBtn.style.textAlign = "center";
  modalCloseBtn.style.borderRadius = "8px";
  modalCloseBtn.style.padding = "5px";
  modalCloseBtn.style.outline = "none";
  modalCloseBtn.style.cursor = "pointer";
  modalCloseBtn.style.fontSize = "15px";
  modalCloseBtn.style.border = "none";
  modalCloseBtn.style.marginTop = "50px";
  modalCloseBtn.style.color = "#fff";
  modalCloseBtn.style.backgroundColor = "red";
  modalCloseBtn.addEventListener("click", function () {
    modalContainer.style.display = "none";
  });
  modalContainer.appendChild(modalCloseBtn);

  document.body.appendChild(modalContainer);
});

// console.log("Current User: ", currentUser);

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

