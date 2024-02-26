var loginUsernameEl = document.getElementById("usernameInput");
var loginPasswordEl = document.getElementById("passwordInput");
var loginBtnEl = document.getElementById("signinLoginBtn");



loginBtnEl.addEventListener('click', function () {
    var username = loginUsernameEl.value;
    localStorage.setItem('username', username);


    var usernameValue = loginUsernameEl.value;
    var passwordValue = loginPasswordEl.value;

    var userCredObj = {
        username: usernameValue,
        password: passwordValue
    };
    console.log("Sending user data");
    sendUserCredRequest(userCredObj);
});

function sendUserCredRequest(userCredObj) {
    console.log("Entered into the function");
    var csrftoken = getCookie('csrftoken');
    console.log("User Object", userCredObj);

    fetch('/login-user/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Username': userCredObj.username, 
        },
        body: JSON.stringify({
            username: userCredObj.username,
            password: userCredObj.password,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === 'success') {
            window.location.href = '/'; 
        } else if (data.result === 'error') {
            alert('Error logging user: ' + data.message);
        }
    })
    .catch(error => {
        console.error("Error sending data:", error);
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}









