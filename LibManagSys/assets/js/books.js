var modalContainer = null; 

function openModal(bookTitle) {
    var body = document.body;

    if (!modalContainer) {
        modalContainer = document.createElement("div");
        modalContainer.id = "modalContainer";
        modalContainer.style.position = "fixed";
        modalContainer.style.top = "50%";
        modalContainer.style.left = "50%";
        modalContainer.style.transform = "translate(-50%, -50%)";
        modalContainer.style.height = "550px";
        modalContainer.style.width = "750px";
        modalContainer.style.borderRadius = "15px";
        modalContainer.style.border = "0.5px solid black";
        modalContainer.style.backgroundColor = "rgba(212, 244, 244, 0.8)";
        modalContainer.style.display = "flex" ; 
        modalContainer.style.flexDirection = "column";
        modalContainer.style.justifyContent = "center";
        modalContainer.style.alignItems = "center";
    }

    modalContainer.innerHTML = "";

    var message = document.createElement("h3");
    message.innerHTML = "Do you want to issue this book: " + bookTitle;
    message.style.fontSize = "30px";
    message.style.color = "black";
    message.style.fontFamily = "Roboto";
    modalContainer.appendChild(message);


    var confirmBtn = document.createElement("button");
    confirmBtn.textContent = "Confirm Book Issue";
    confirmBtn.style.width = "160px";
    confirmBtn.style.height = "45px";
    confirmBtn.style.textAlign ="center";
    confirmBtn.style.borderRadius = "8px";
    confirmBtn.style.padding = "5px";
    confirmBtn.style.outline = "none";
    confirmBtn.style.cursor = "pointer";
    confirmBtn.style.fontSize = "15px";
    confirmBtn.style.border = "none";
    confirmBtn.style.marginTop = "20px";
    confirmBtn.style.color ="#fff";
    confirmBtn.style.backgroundColor = "red";
    modalContainer.appendChild(confirmBtn);




    var closeModalBtn = document.createElement("button");
    closeModalBtn.textContent = "Close";
    closeModalBtn.style.width = "80px";
    closeModalBtn.style.height = "30px";
    closeModalBtn.style.textAlign ="center";
    closeModalBtn.style.borderRadius = "8px";
    closeModalBtn.style.padding = "2px";
    closeModalBtn.style.outline = "none";
    closeModalBtn.style.cursor = "pointer";
    closeModalBtn.style.fontSize = "10px";
    closeModalBtn.style.border = "none";
    closeModalBtn.style.marginTop = "20px";
    closeModalBtn.style.color ="#fff";
    closeModalBtn.style.backgroundColor = "green";
    closeModalBtn.addEventListener('click',function(){
        modalContainer.classList.add('hidden');
    });

    modalContainer.appendChild(closeModalBtn);


    



    confirmBtn.addEventListener('click',function(){
        var bookTitleEl = bookTitle;
        var loggedUsername = window.loggedUsername;
        // console.log("Username: ", loggedUsername);

        userHasBorrowedBook(bookTitleEl, loggedUsername)
            .then(hasBorrowed => {
                if (hasBorrowed) {
                    alert('You have already borrowed this book.');
                }
                else {
                    
                    var issueDetails = {
                        bookTitle: bookTitleEl,
                        username: loggedUsername,
                    };
                    var csrftoken = getCookie('csrftoken');
                    modalContainer.classList.add('hidden');

                    fetch('/issue-member-book/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken,
                        },
                        body: JSON.stringify(issueDetails),
                    })
                        .then(response => response.json())
                        .then(data => {
                            console.log('Server response:', data);
                        })
                        .catch(error => {
                            console.error('Error sending data to server:', error);
                        });
                }
            });
    });

    function userHasBorrowedBook(bookTitle, username) {
        return fetch('/check-borrowed-book/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ bookTitle, username }),
        })
            .then(response => response.json())
            .then(data => data.hasBorrowed);
    }

    if (!modalContainer.parentElement) {
        body.appendChild(modalContainer);
    }
    
    
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