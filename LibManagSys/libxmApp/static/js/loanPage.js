function goBack() {
    window.history.back();
}


function returnBook(loanId){
    var redirectUrl = '/return-book/' +
    + encodeURIComponent(loanId);

    window.location.href = redirectUrl;
}