PID = document.getElementById("pid").value
layui.use(['upload', 'element', 'layer'], function () {
    var $ = layui.jquery,
        upload = layui.upload,
        element = layui.element,
        layer = layui.layer;

    var uploadListIns = upload.render({
        elem: '#selectPlugin',
        elemList: $('#imgList'),
        url: '/uploadPlugin/' + PID,
        accept: 'file',
        multiple: true,
        number: 1,
        auto: true,
        drag: true,
        exts: 'zip',
        before: function (obj) {
            var files = this.files = obj.pushFile();
        },
        choose: function (obj) {
            var that = this;
            var files = this.files = obj.pushFile(); //将每次选择的文件追加到文件队列
            $("#submitPluginForm").attr("disabled", false);
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
                        url: "/api/delPluginFile/" + PID,
                        data: {
                            plugin: file.name
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
                        $("#submitPluginForm").attr("disabled", true);
                    }
                });
                that.elemList.append(tr);
            });

        },
        allDone: function (obj) {
            if (obj.successful == obj.total) {
                console.log(obj)
                layer.msg('Upload Successful');
                $("#submitPluginForm").attr("disabled", false);
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


$("#submitPluginForm").click(function () {
    'use strict';
    var addPluginForm = $('#addPluginFrom');
    if (addPluginForm.length) {
        addPluginForm.validate({
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
                addPlugin();
            }
        });
    }
})

function addPlugin() {
    $.ajax({
        type: "post",
        url: "/api/addPlugin/" + PID,
        dataType: "json",
        data: $('#addPluginFrom').serialize(),
        success: function (result) {
            if (result.code == 200) {
                layer.msg('Submitted successfully', {
                    icon: 6, end: function () {
                        window.location.href =
                            "/myplugin";
                    }
                });

            } else {
                layer.msg('Error！ Please refresh this page and try again later!', {icon: 5});
            }
        }
    });
}

