TID = document.getElementById("tid").value
layui.use(['upload', 'element', 'layer'], function () {
    var $ = layui.jquery,
        upload = layui.upload,
        element = layui.element,
        layer = layui.layer;

    var uploadListIns = upload.render({
        elem: '#selectImg',
        elemList: $('#imgList'),
        url: '/uploadImg/' + TID,
        accept: 'file',
        multiple: true,
        number: 10,
        auto: true,
        drag: true,
        exts: 'jpg|png|jpeg|zip',
        before: function (obj) {
            var files = this.files = obj.pushFile();
        },
        choose: function (obj) {
            var that = this;
            var files = this.files = obj.pushFile(); //将每次选择的文件追加到文件队列
            $("#submitTaskForm").attr("disabled", false);
            obj.preview(function (index, file, result) {
                var tr = $(['<tr id="upload-' + index + '">', '<td>' + file.name +
                '</td>', '<td>' + (file.size / 1014).toFixed(1) + 'kb</td>',
                    '<td>',
                    '<button class="layui-btn layui-btn-xs demo-reload layui-hide">Re-upload</button>',
                    "<button class='btn btn-danger btn-sm demo-delete'>Delete</button>",
                    '</td>', '</tr>'
                ].join(''));
                tr.find('.demo-reload').on('click', function () {
                    obj.upload(index, file);
                });
                tr.find('.demo-delete').on('click', function () {
                    $.ajax({
                        type: "post",
                        url: "/api/delImg/" + TID,
                        data: {
                            img: file.name
                        },
                        dataType: "json",
                        success: function (result) {
                            if (result.code == 200) {
                                layer.msg('Delete Successful');
                            } else {
                                layer.msg('Delete Error');
                            }
                        }
                    });
                    delete files[index];
                    tr.remove();
                    uploadListIns.config.elem.next()[0].value = '';
                    let fileLength = Object.keys(files).length;
                    if (fileLength <= 0) {
                        $("#submitTaskForm").attr("disabled", true);
                    }
                });
                that.elemList.append(tr);
            });

        },
        allDone: function (obj) {
            if (obj.successful == obj.total) {
                layer.msg('Upload Successful');
                $("#submitTaskForm").attr("disabled", false);
                return;
            } else {
                layer.msg('Upload Error');
                return;
            }
        },
        error: function (index, upload) {
            var that = this;
            var tr = that.elemList.find('tr#upload-' + index),
                tds = tr.children();
            tds.eq(3).find('.demo-reload').removeClass('layui-hide'); //显示重传
        }
    });
});


$("#submitTaskForm").click(function () {
    'use strict';
    var addTaskForm = $('#addTaskFrom');
    if (addTaskForm.length) {
        addTaskForm.validate({
            rules: {
                'name': {
                    required: true,
                    maxlength: 20
                },
                'des': {
                    required: true,
                    maxlength: 20
                },
                'mail': {
                    email: true
                },
                'cf': {
                    required: true,
                    number: true
                }
            },
            submitHandler: function (form) {
                addTask();
            }
        });
    }
})

function addTask() {
    $.ajax({
        type: "post",
        url: "/api/addTask/" + TID,
        dataType: "json",
        data: $('#addTaskFrom').serialize(),
        success: function (result) {
            if (result.code == 200) {
                layer.msg('Submitted successfully', {
                    icon: 6, end: function () {
                        window.location.href =
                            "/schedule/" + result.tid;
                    }
                });
            } else {
                layer.msg('Error！ Please try again!', {icon: 5});
            }
        }
    });
}

