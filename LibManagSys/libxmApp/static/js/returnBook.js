function goBack() {
    window.history.back();
}



function payReturnBook(loanId){
    // var loanId = loan.id;
    console.log("My Loan Id: ", loanId);
    var csrftoken = getCookie('csrftoken');

    fetch('/pay-return-book/' + loanId + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        // Add any additional data you need to send
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
        window.location.href = '/'
    })
    .catch(error => {
        console.error('Error sending data to server:', error);
        // Handle the error as needed
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