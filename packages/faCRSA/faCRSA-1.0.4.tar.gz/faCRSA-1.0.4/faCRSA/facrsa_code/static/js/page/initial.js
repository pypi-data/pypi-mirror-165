$("#initial").click(function () {
    'use strict';
    var pageInitialForm = $('#initialForm');
    if (pageInitialForm.length) {
        pageInitialForm.validate({
            rules: {
                'user': {
                    required: true
                },
                'password': {
                    required: true
                },
                'host': {
                    required: true
                }
            },
            submitHandler: function () {
                initialMail()
            }
        });
    }
});

function initialMail() {
    $.ajax({
        type: "post",
        url: "/api/initial",
        dataType: "json",
        data: {user: $("#user").val(), password: $("#password").val(), host: $("#host").val()},
        beforeSend: function () {
            waitAlert();
        },
        success: function (result) {
            if (result.code == 200) {
                var sentence = "Success";
                successToast(sentence);
            } else {
                var sentence = 'Please check whether your mail address is correct';
                errorToast(sentence);
            }
        }
    });
}

function waitAlert() {
    var timerInterval;
    Swal.fire({
        title: 'Initializing',
        timer: 100000,
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