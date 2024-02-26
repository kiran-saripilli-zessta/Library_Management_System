var searchEl = document.getElementById("search-box");
var cardEl = document.getElementById("myCard1");


searchEl.addEventListener("change",function(event){
    console.log(event.target.value);
});

document.getElementById('signupBtn').addEventListener('click', function() {
    window.location.href = '/signup/';  
});

cardEl.addEventListener("click",function(){
    alert("Opened");
});

document.getElementById("availableCardBtn").addEventListener('click',function(){
    window.location.href = '/available/';
});

document.getElementById("authorCardBtn").addEventListener('click',function(){
    window.location.href = "/author/";
});

document.getElementById("genreCardBtn").addEventListener('click',function(){
    window.location.href = '/genre/';
});

document.getElementById("loginBtn").addEventListener('click',function(){
    window.location.href = "/login/";
});

checkAuthenticationStatus();

function checkAuthenticationStatus() {
    console.log("Checking authentication status...");
    fetch('/get-auth-status/')
        .then(response => response.json())
        .then(data => {
            console.log("Authentication status:", data.isAuthenticated);
        })
        .catch(error => {
            console.error("Error checking authentication status:", error);
        });
}

