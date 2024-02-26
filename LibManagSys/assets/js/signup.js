function createAdminFields() {
    var dynamicField = document.getElementById("dynamicFields");
    if (!dynamicField) {
        console.error("Error: dynamicFields not found");
        return;
    }
    // console.log("1");

    dynamicField.innerHTML = '';
    dynamicField.style.marginTop = "70px";

    // console.log("2");

    // Username
    var userlabelEl = createLabel("name", "Username");
    var usernameInputEl = createInput("name", "Enter your Username");
    usernameInputEl.id = "name";

    // Password
    var passlabelEl = createLabel("pass", "Password");
    var passInputEl = createInput("pass", "Enter your Password", "password");
    passInputEl.id = "pass";

    // console.log("3");

    // Submit Button
    var submitBtn = createSubmitButton("Submit");
    submitBtn.addEventListener("click", function () {
        var username = document.getElementById("name").value;
        var password = document.getElementById("pass").value;

        if (validateAdminCredentials(username, password)) {
            console.log("Entered Admin Field");
            window.location.href = '/adminUI/';
        } else {
            alert("Incorrect credentials. Please try again.");
        }
    });

    dynamicField.appendChild(userlabelEl);
    dynamicField.appendChild(createBreak());
    dynamicField.appendChild(usernameInputEl);
    dynamicField.appendChild(createBreak(2));

    dynamicField.appendChild(passlabelEl);
    dynamicField.appendChild(createBreak());
    dynamicField.appendChild(passInputEl);
    dynamicField.appendChild(createBreak(2));


    dynamicField.appendChild(submitBtn);
}

function createLabel(forId, text) {
    var labelEl = document.createElement("label");
    labelEl.setAttribute("for", forId);
    labelEl.textContent = text;
    labelEl.style.margin = "3px";
    return labelEl;
}

function createInput(id, placeholder, type = "text",applyStyles = true) {
    var inputEl = document.createElement("input");
    inputEl.classList.add("inputName");
    inputEl.id = id;
    inputEl.type = type;
    inputEl.style.width = "400px";
    inputEl.style.height = "30px";
    inputEl.style.marginBottom = "5px";
    inputEl.placeholder = placeholder;
    


    if (!applyStyles) {
        inputEl.classList.add("inputName");
        inputEl.style.width = "300px";
        inputEl.style.height = "30px";
        inputEl.style.marginBottom = "15px";
        inputEl.style.border = "none";
        inputEl.style.marginTop = "5px";
    }

    return inputEl;
}

function createSubmitButton(text) {
    var submitBtn = document.createElement("button");
    submitBtn.classList.add("choice-btn");
    submitBtn.textContent = text;
    submitBtn.style.marginTop = "12px";
    submitBtn.style.marginLeft = "5px";
    submitBtn.style.backgroundColor = "black";
    submitBtn.style.color = "#fff";
    return submitBtn;
}

function createBreak(times = 1) {
    var breaks = document.createDocumentFragment();
    for (var i = 0; i < times; i++) {
        breaks.appendChild(document.createElement("br"));
    }
    return breaks;
}



function createUserFields() {
    var dynamicField = document.getElementById("dynamicFields");
    if (!dynamicField) {
        console.error("Error: dynamicFields not found");
        return;
    }

    dynamicField.innerHTML = '';  
    dynamicField.style.marginTop = "30px";

    // Username
    var userlabelEl = createLabel("name", "Username");
    var usernameInputEl = createInput("name", "Enter your Username");
    usernameInputEl.name = "username";

    // Password
    var passlabelEl = createLabel("pass", "Password");
    var passInputEl = createInput("pass", "Enter your Password", "password");
    passInputEl.name = "password";

    // Confirm Password
    var confirmPasslabelEl = createLabel("confirmPass", "Confirm Password");
    var confirmPassInputEl = createInput("confirmPass", "Confirm your Password", "password");
    confirmPassInputEl.name = "confirm_password";


    // Email
    var emailLabelEl = createLabel("email", "Email");
    var emailInputEl = createInput("email", "Enter your Email", "email");
    emailInputEl.name = "email";


    var userImageLabelEl = createLabel("image", "User Image");
    var userImageInputEl = createInput("image", "Upload your Picture", "file", false);
    userImageInputEl.name = "user_image";
    userImageInputEl.accept = "image/*";


    // Submit Button
    var submitBtn = createSubmitButton("Submit");
    submitBtn.addEventListener('click',function(){
        var userNameValue = usernameInputEl.value;
        var passValue = passInputEl.value;
        var confPassValue =  confirmPassInputEl.value;
        var emailValue = emailInputEl.value;


        var formData = new FormData();
        formData.append("userName", userNameValue);
        formData.append("passWord", passValue);
        formData.append("email", emailValue);
        formData.append("userImage", userImageInputEl.files[0]);


        if(passValue === confPassValue){
            sendAddUserRequest(formData);
        }
        else{
            alert("Confirm Password and Password Not Matched!!!");
        }

    })


    

    dynamicField.appendChild(userlabelEl);
    dynamicField.appendChild(createBreak());
    dynamicField.appendChild(usernameInputEl);
    dynamicField.appendChild(createBreak(2));

    dynamicField.appendChild(passlabelEl);
    dynamicField.appendChild(createBreak());
    dynamicField.appendChild(passInputEl);
    dynamicField.appendChild(createBreak(2));

    dynamicField.appendChild(confirmPasslabelEl);
    dynamicField.appendChild(createBreak());
    dynamicField.appendChild(confirmPassInputEl);
    dynamicField.appendChild(createBreak(2));

    dynamicField.appendChild(emailLabelEl);
    dynamicField.appendChild(createBreak());
    dynamicField.appendChild(emailInputEl);
    dynamicField.appendChild(createBreak(2));

    dynamicField.appendChild(userImageLabelEl);
    dynamicField.appendChild(createBreak());
    dynamicField.appendChild(userImageInputEl);
    dynamicField.appendChild(createBreak(1));

    dynamicField.appendChild(submitBtn);
    
}


function sendAddUserRequest(formData){
    console.log("This is User Object ", formData);

    fetch('/adding-new-user/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === 'success') {
            window.location.href = '/';
        } else if (data.result === 'error') {
            alert('Error adding user: ' + data.message);
        }
    })
    .catch(error => {
        console.error("Error sending data:", error);
    });
}



function validateAdminCredentials(username, password) {
    const adminUsername = "SaiKiran";
    const adminPassword = "Kalvinsk@123";

    return username === adminUsername && password === adminPassword;
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