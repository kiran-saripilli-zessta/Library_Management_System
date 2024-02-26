function createAddBookFields() {
    console.log("clicked");
    var dynamicField = document.getElementsByClassName("dynamic-admin-field")[0];

    if (!dynamicField) {
        console.error("Error: dynamicFields not found");
        return;
    }

    dynamicField.innerHTML = '';

    var cardContainer = document.createElement("div");
    cardContainer.classList.add("card");


    var bookTitleInput = createInput("bookTitle", "Book Title");
    var bookAuthorInput = createInput("bookAuthor", "Book Author");
    var bookGenreInput = createInput("bookGenre", "Book Genre");
    var bookUniqueISBNInput = createInput("bookUniqueISBN", "Book Unique ISBN");
    var bookPublisherInput = createInput("bookPublisher", "Book Publisher");

    var addButton = createButton("Add Book");


    addButton.addEventListener("click", function () {
        var addBookInput = {
            bookTitle: bookTitleInput.value,
            bookAuthor: bookAuthorInput.value,
            bookGenre: bookGenreInput.value,
            bookUniqueISBN: bookUniqueISBNInput.value,
            bookPublisher: bookPublisherInput.value
        };

        sendBookDataRequest(addBookInput);
    });

    cardContainer.appendChild(bookTitleInput);
    cardContainer.appendChild(bookAuthorInput);
    cardContainer.appendChild(bookGenreInput);
    cardContainer.appendChild(bookUniqueISBNInput);
    cardContainer.appendChild(bookPublisherInput);
    cardContainer.appendChild(addButton);

    dynamicField.appendChild(cardContainer);
}


function sendBookDataRequest(addBookInput) {
    var csrftoken = getCookie('csrftoken');
    console.log("Add Book Input", addBookInput);

    fetch('/add-book/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(addBookInput),
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === 'success') {
            alert('Book added successfully!');
        } else if (data.result === 'not_found') {
            alert('Book not found!');
        }
    })
    .catch(error => {
        console.error("Error sending data:", error);
    });
}

document.getElementById('viewBooksButton').addEventListener('click', function() {
    sendViewAllBooksRequest();
});

document.getElementById('viewUserButton').addEventListener('click', function(){
    sendViewAllUsersRequest();
});
    


function sendViewAllBooksRequest() {
    var csrftoken = getCookie('csrftoken');

    fetch('/view-books-admin/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        createViewAllBooksFields(data);
    })
    .catch(error => {
        console.error("Error fetching book data:", error);
    });
}

function createViewAllBooksFields(available_books2) {
    console.log(available_books2);
    var dynamicAdminField = document.querySelector('.dynamic-admin-field');
    dynamicAdminField.innerHTML = ''; 

    var table = document.createElement('table');

    var thead = document.createElement('thead');
    var headerRow = document.createElement('tr');
    var bookTitleEl = document.createElement('th');
    bookTitleEl.textContent = "Book Title";
    var bookAuthorEl = document.createElement('th');
    bookAuthorEl.textContent = "Book Author";
    var bookGenreEl = document.createElement('th');
    bookGenreEl.textContent = "Book Genre";
    headerRow.appendChild(bookTitleEl);
    headerRow.appendChild(bookAuthorEl);
    headerRow.appendChild(bookGenreEl);

    thead.appendChild(headerRow);
    table.appendChild(thead);

    var tbody = document.createElement('tbody');

    // Check if available_books2 is defined and is an array
    if (Array.isArray(available_books2)) {
        // Iterate over the available_books2 array using forEach
        available_books2.forEach(function (book) {
            console.log("Book:", book);
            var trEl = document.createElement('tr');
            var tdEl1 = document.createElement("td");
            tdEl1.textContent = book.book_title;
            var tdEl2 = document.createElement("td");
            // tdEl2.textContent = book.book_author;
            tdEl2.textContent = book.book_author ? book.book_author.name : 'Unknown Author';
            var tdEl3 = document.createElement("td");
            tdEl3.textContent = book.book_genre ? book.book_genre.genre_name : 'Unknown Genre';
        
            trEl.appendChild(tdEl1);
            trEl.appendChild(tdEl2);
            trEl.appendChild(tdEl3);
                
            tbody.appendChild(trEl);
        });
    }
    else {
        console.error("Error: available_books2 is not defined or is not an array.");
    }

    table.appendChild(tbody);

    dynamicAdminField.appendChild(table);
}



function appendCell(row, elementType, textContent) {
    var cell = document.createElement(elementType);
    cell.textContent = textContent;
    row.appendChild(cell);
}



function sendViewAllUsersRequest() {
    var csrftoken = getCookie('csrftoken');

    fetch('/view-users-admin/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        createViewUsersFields(data);
    })
    .catch(error => {
        console.error("Error fetching users data:", error);
    });
}


function createViewUsersFields(available_users){
    var dynamicAdminField = document.querySelector('.dynamic-admin-field');
    dynamicAdminField.innerHTML = ''; 

    var table = document.createElement('table');

    var thead = document.createElement('thead');
    var headerRow = document.createElement('tr');
    var usernameEl = document.createElement('th');
    usernameEl.textContent = "Username";
    var userEmailEl = document.createElement('th');
    userEmailEl.textContent = "Email";
    headerRow.appendChild(usernameEl);
    headerRow.appendChild(userEmailEl);

    thead.appendChild(headerRow);
    table.appendChild(thead);

    var tbody = document.createElement('tbody');

    // Check if available_books2 is defined and is an array
    if (Array.isArray(available_users)) {
        // Iterate over the available_books2 array using forEach
        available_users.forEach(function (user) {
            var trEl = document.createElement('tr');
            var tdEl1 = document.createElement("td");
            tdEl1.textContent = user.username;
            var tdEl3 = document.createElement("td");
            tdEl3.textContent = user.email;
        
            trEl.appendChild(tdEl1);
            trEl.appendChild(tdEl3);
                
            tbody.appendChild(trEl);
        });
    } else {
        console.error("Error: available_users is not defined or is not an array.");
    }

    table.appendChild(tbody);

    dynamicAdminField.appendChild(table);
}

function createDeleteBookFields(){
    console.log("clicked");
    var dynamicField = document.getElementsByClassName("dynamic-admin-field")[0];
    
    if (!dynamicField) {
        console.error("Error: dynamicFields not found");
        return;
    }

    // Clear existing content
    dynamicField.innerHTML = '';
    var container = document.createElement("div");

    var serachBar = document.createElement("input");
    serachBar.type = "search";
    serachBar.name = "Search-Bar";
    serachBar.placeholder = "Enter Book Name";
    serachBar.id = "bookSearchBar";
    serachBar.style.width = "550px";


    serachBar.addEventListener('change',function(event){
        var searchItem = event.target.value;
        sendSearchRequest(searchItem);
    });

    var deleteButton = createButton("Delete Book");

    container.appendChild(serachBar);
    container.appendChild(deleteButton);

    dynamicField.appendChild(container);

}

function sendSearchRequest(searchTerm) {
    fetch(`/search-book/?term=${searchTerm}`)
        .then(response => response.json())
        .then(data => {
            if (data.result === 'success') {
                alert('Book deleted successfully!');
            } else if (data.result === 'not_found') {
                alert('Book not found!');
            }
        })
        .catch(error => {
            console.error("Error retrieving data:", error);
        });
}


function createAddUserFields(){
    console.log("clicked");
    var dynamicField = document.getElementsByClassName("dynamic-admin-field")[0];
    
    if (!dynamicField) {
        console.error("Error: dynamicFields not found");
        return;
    }

    // Clear existing content
    dynamicField.innerHTML = '';

    var cardContainer = document.createElement("div");
    cardContainer.classList.add("card");


    var userNameInput = createInput("userName", "Enter Username");
    var userPassInput = createInput("userPass", "Enter Password");
    var userEmailInput = createInput("userEmail", "Enter Email");

    // Create "Add Book" button
    var addButton = createButton("Add User");
    addButton.addEventListener("click", function () {
        
        var addUserInput = {
            userName: userNameInput.value,
            userPass: userPassInput.value,
            userEmail : userEmailInput.value
        };

        sendUserDataRequest(addUserInput);
    });

    // Append form elements and button to the card container
    cardContainer.appendChild(userNameInput);
    cardContainer.appendChild(userPassInput);
    cardContainer.appendChild(userEmailInput);
    cardContainer.appendChild(addButton);

    // Append the card container to the dynamic field
    dynamicField.appendChild(cardContainer);

}

function sendUserDataRequest(addUserInput) {
    var csrftoken = getCookie('csrftoken');
    console.log("Add User Input", addUserInput);

    fetch('/add-user/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            userName: addUserInput.userName,
            userPass: addUserInput.userPass,
            userEmail: addUserInput.userEmail,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === 'success') {
            alert('User added successfully!');
        } else if (data.result === 'error') {
            alert('Error adding user: ' + data.message);
        }
    })
    .catch(error => {
        console.error("Error sending data:", error);
    });
}


function createDeleteUserFields(){
    console.log("clicked");
    var dynamicField = document.getElementsByClassName("dynamic-admin-field")[0];
    
    if (!dynamicField) {
        console.error("Error: dynamicFields not found");
        return;
    }

    // Clear existing content
    dynamicField.innerHTML = '';
    var container = document.createElement("div");

    var serachBar = document.createElement("input");
    serachBar.type = "search";
    serachBar.name = "Search-Bar";
    serachBar.placeholder = "Enter Email Id";
    serachBar.id = "bookSearchBar";
    serachBar.style.width="550px";


    serachBar.addEventListener('change',function(event){
        var searchItem = event.target.value;
        sendSearchUserRequest(searchItem);
    });

    var deleteButton = createButton("Delete User");

    container.appendChild(serachBar);
    container.appendChild(deleteButton);

    dynamicField.appendChild(container);


}

function sendSearchUserRequest(searchTerm) {
    fetch(`/search-user/?term=${searchTerm}`)
        .then(response => response.json())
        .then(data => {
            if (data.result === 'success') {
                alert('User deleted successfully!');
            } else if (data.result === 'not_found') {
                alert('User not found!');
            }
        })
        .catch(error => {
            console.error("Error retrieving data:", error);
        });
}

function createUpdateUserFields() {
    console.log("clicked");
    var dynamicField = document.getElementsByClassName("dynamic-admin-field")[0];

    if (!dynamicField) {
        console.error("Error: dynamicFields not found");
        return;
    }

    dynamicField.innerHTML = '';

    var cardContainerr = document.createElement("div");
    cardContainerr.classList.add("card");

    var userEmailInputmain = createInput("userEmail", "Enter Email");
    userEmailInputmain.style.width = "480px";
    var addButton = createButton("Search User");
    addButton.style.width = "120px";

    addButton.addEventListener("click", function () {
        dynamicField.innerHTML = '';
        cardContainerr.innerHTML = '';

        var userNameInput = createInput("userName", "Enter Username");
        var userPassInput = createInput("userPass", "Enter Password");
        var userEmailInput = createInput("userEmail", "Enter Email");
        var updateDetailsBtn = createButton("Update Details");

        cardContainerr.appendChild(userNameInput);
        cardContainerr.appendChild(userPassInput);
        cardContainerr.appendChild(userEmailInput);
        cardContainerr.appendChild(updateDetailsBtn);

        dynamicField.appendChild(cardContainerr);

        var enteredEmail = userEmailInputmain.value;

        fetch(`/get-user-details/?email=${enteredEmail}`)
            .then(response => response.json())
            .then(data => {
                userNameInput.value = data.username;
                userPassInput.value = data.password;
                userEmailInput.value = data.email;

                updateDetailsBtn.addEventListener("click", function () {
                    var updatedUserName = userNameInput.value;
                    var updatedUserPass = userPassInput.value;
                    var updatedUserEmail = userEmailInput.value;


                    fetch(`/update-user-details/?email=${enteredEmail}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken'),
                        },
                        body: JSON.stringify({
                            userName: updatedUserName,
                            userPass: updatedUserPass,
                            userEmail: updatedUserEmail,
                        }),
                        
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.result === 'success') {
                                alert('User details updated successfully!');
                            } else {
                                alert('Error updating user details!');
                            }
                        })
                        .catch(error => {
                            console.error("Error updating user details:", error);
                        });
                });
            })
            .catch(error => {
                console.error("Error fetching user details:", error);
            });
    });

    cardContainerr.appendChild(userEmailInputmain);
    cardContainerr.appendChild(addButton);
    dynamicField.appendChild(cardContainerr);
}


function createInput(id, placeholder) {
    var input = document.createElement("input");
    input.id = id;
    input.type = "text";
    input.placeholder = placeholder;
    return input;
}

function createButton(text) {
    var button = document.createElement("button");
    button.textContent = text;
    button.style.display = "block";
    button.style.fontSize = "15px";
    button.style.fontWeight = "500";
    return button;
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
