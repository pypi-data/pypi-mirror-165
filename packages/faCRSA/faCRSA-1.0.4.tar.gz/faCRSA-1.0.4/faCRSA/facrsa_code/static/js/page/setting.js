$("#changeUserName").click(function () {
    'use strict';
    var pagechangeUserNameForm = $('#changeUserNameForm');
    if (pagechangeUserNameForm.length) {
        pagechangeUserNameForm.validate({
            rules: {
                'username': {
                    required: true,
                    maxlength: 16,
                    minlength: 5,
                    remote: {
                        type: "post",
                        url: "/api/checkUserName",
                        data: {
                            username: function () {
                                return $("#username").val();
                            }
                        },
                        dataType: "html",
                        dataFilter: function (data, type) {
                            if (data == 404)
                                return true;
                            else
                                return false;
                        }
                    }
                },
                'co-username': {
                    required: true,
                    maxlength: 16,
                    minlength: 5,
                    equalTo: "#username"
                }
            },
            submitHandler: function (form) {
                $.ajax({
                    type: "post",
                    url: "/api/changeUserName",
                    dataType: "json",
                    data: {username: $("#username").val()},
                    beforeSend: function () {
                        waitAlert();
                    },
                    success: function (result) {
                        if (result == 200) {
                            var sentence = "Success";
                            successToast(sentence);
                        } else {
                            var sentence = 'Please try again later!';
                            errorToast(sentence);
                        }
                    }
                });
                ;
            }
        });
    }
});

$("#changePWD").click(function () {
    'use strict';
    var pagechangePWDForm = $('#changePWDForm');
    if (pagechangePWDForm.length) {
        pagechangePWDForm.validate({
            rules: {
                'password': {
                    required: true,
                    maxlength: 16,
                    minlength: 5,
                },
                'con-password': {
                    required: true,
                    maxlength: 16,
                    minlength: 5,
                    equalTo: "#password"
                }
            },
            submitHandler: function (form) {
                $.ajax({
                    type: "post",
                    url: "/api/changePWD",
                    dataType: "json",
                    data: {password: $("#password").val()},
                    beforeSend: function () {
                        waitAlert();
                    },
                    success: function (result) {
                        if (result == 200) {
                            var sentence = "Success";
                            successToast(sentence);
                        } else {
                            var sentence = 'Please try again later!';
                            errorToast(sentence);
                        }
                    }
                });
                ;
            }
        });
    }
});

function waitAlert() {
    var timerInterval;
    Swal.fire({
        title: 'Validating',
        timer: 10000,
        timerProgressBar: false,
        didOpen: () => {
            Swal.showLoading();
            timerInterval = setInterval(() => {
                const content = Swal.getHtmlContainer();
                if (content) {
                    const b = content.querySelector('b');
                    if (b) {
                        b.textContent = Swal.getTimerLeft();
                    }
                }
            }, 100);
        },
        willClose: () => {
            clearInterval(timerInterval);
        }
    }).then(result => {
        errorToast('Please try again later!')
    });
}

function errorToast(sentence) {
    Swal.fire({
        toast: true,
        icon: 'error',
        title: sentence,
        timer: 3000,
        showCloseButton: true,
        showConfirmButton: false
    })
}


function successToast(sentence) {
    Swal.fire({
        toast: true,
        icon: 'success',
        title: sentence,
        timer: 2500,
        showCloseButton: true,
        showConfirmButton: false,
        willClose: () => {
            window.location.href =
                "/login";
        }
    })
}