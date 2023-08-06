$("#login").click(function () {
    'use strict';
    var pageLoginForm = $('#loginform');
    if (pageLoginForm.length) {
        pageLoginForm.validate({
            rules: {
                'username': {
                    required: true
                },
                'password': {
                    required: true
                }
            },
            submitHandler: function () {
                validateDataLogin()
            }
        });
    }
});

$("#register").click(function () {
    'use strict';
    var pageLoginForm = $('#regform');
    if (pageLoginForm.length) {
        pageLoginForm.validate({
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
                validateDataReg();
            }
        });
    }
});

$("#forgetpwd").click(function () {
    'use strict';
    var pageLoginForm = $('.auth-forgot-password-form');
    if (pageLoginForm.length) {
        pageLoginForm.validate({
            rules: {
                'email': {
                    required: true,
                    email: true
                },
            },
            submitHandler: function (form) {
                forgetPwd();
            }
        });
    }
});


function validateDataLogin() {
    if ($("input[type='checkbox']").is(':checked')) {
        var checked = "yes";
    }
    $.ajax({
        type: "post",
        url: "/api/login",
        dataType: "json",
        data: {username: $("#username").val(), password: $("#password").val(), remember: checked},
        success: function (result) {
            if (result.code == 200) {
                var sentence = 'Welcome to faCRSA 🎉';
                successToast(sentence);
            } else if (result.code == 400) {
                var sentence = 'Account name or password is incorrect';
                errorToast(sentence);
            } else {
                var sentence = 'System error';
                errorToast(sentence);
            }
        }
    });
}

function validateDataReg() {
    $.ajax({
        type: "post",
        url: "/api/register",
        dataType: "json",
        data: {username: $("#username").val(), password: $("#password").val()},
        beforeSend: function () {
            waitAlert();
        },
        success: function (result) {
            if (result == 200) {
                var sentence = "Success";
                successToastReg(sentence);
            } else {
                var sentence = 'Please check the information entered!';
                errorToast(sentence);
            }
        }
    });
}

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
        showConfirmButton: false,
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
                "/";
        }
    })
}

function successToastReg(sentence) {
    Swal.fire({
        toast: true,
        icon: 'success',
        title: sentence,
        timer: 3000,
        showCloseButton: true,
        showConfirmButton: false,
        willClose: () => {
            window.location.href =
                "/login";
        }
    })
}
