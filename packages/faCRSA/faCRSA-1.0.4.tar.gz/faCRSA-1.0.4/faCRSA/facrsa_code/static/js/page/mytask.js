layui.use('table', function () {
    var table = layui.table;
    table.render({
        elem: '#task',
        url: '/api/getMyTask',
        toolbar: '#toolbarDemo',
        defaultToolbar: ['filter', 'exports', 'print'],
        title: 'data table',
        text: "System Error",
        limit: 5,
        cols: [
            [{
                field: 'tid',
                title: 'ID',
                width: 80,
                templet: function (d) {
                    return d.LAY_TABLE_INDEX + 1
                },
                unresize: true,
                sort: true,
                align: 'center',
                type: 'numbers'
            }, {
                field: 'task_name',
                title: 'Name',
                align: 'center'
            }, {
                field: 'description',
                title: 'Description',
                align: 'center'
            }, {
                field: 'create_time',
                title: 'Creat Time',
                align: 'center',
                minWidth: 150,
                sort: true
            }, {
                field: 'status',
                title: 'Status',
                templet: function (d) {
                    if (d.status == 1) {
                        return ' <div class="badge bg-success bg-gradient rounded-pill mb-2">success</div>'
                    }
                    if (d.status == 2) {
                        return ' <div class="badge bg-info bg-gradient rounded-pill mb-2">doing</div>'
                    }
                    if (d.status == 0) {
                        return ' <div class="badge bg-danger bg-gradient rounded-pill mb-2">error</div>'
                    }
                },
                align: 'center',
                sort: true,
                width: 100
            }, {
                fixed: 'right',
                title: 'Action',
                toolbar: '#barDemo',
                align: 'center',
                 width: 100
            }]
        ],
        page: true
    });
    table.on('tool(task)', function (obj) {
        var data = obj.data;
        if (obj.event === 'del') {
            layer.msg('Confirm delete？', {
                time: 0
                , btn: ['yes', 'no']
                , yes: function (index) {
                    $.ajax({
                        type: "post",
                        url: "/api/delTask",
                        dataType: "json",
                        data: {tid: data.tid},
                        success: function (result) {
                            if (result == 200) {
                                layer.msg('Delete successfully', {
                                    icon: 6, time: 1000, end: function () {
                                        obj.del();
                                    }
                                });
                                layer.close(index);
                            } else {
                                layer.msg('Error！ Please try again!', {icon: 5});
                                layer.close(index);
                            }
                        }
                    });
                }
            });
        } else if (obj.event === 'view') {
            let test = '<div class="spinner-border spinner-border-sm text-success" role="status"><span class="visually-hidden">Loading...</span></div>';
            if (data.status == 2) {
                window.location.href = "/schedule/" + data.tid;
            } else if (data.status == 1) {
                window.location.href = "/result/" + data.tid;
            }
        }
    });

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
        showConfirmButton: false
    })
}