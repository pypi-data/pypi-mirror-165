layui.use('table', function () {
    var table = layui.table;
    table.render({
        elem: '#plugin',
        url: '/api/getMyPlugin',
        toolbar: '#toolbarDemo',
        defaultToolbar: ['filter', 'exports', 'print'],
        title: 'data table',
        text: "System Error",
        limit: 5,
        cols: [
            [{
                field: 'pid',
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
                field: 'plugin_name',
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
                fixed: 'right',
                title: 'Action',
                toolbar: '#barDemo',
                align: 'center',
                width: 80
            }]
        ],
        page: true
    });
    table.on('tool(plugin)', function (obj) {
        var data = obj.data;
        if (obj.event === 'del') {
            layer.msg('Confirm delete？', {
                time: 0
                , btn: ['yes', 'no']
                , yes: function (index) {
                    $.ajax({
                        type: "post",
                        url: "/api/delPlugin",
                        dataType: "json",
                        data: {pid: data.pid},
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
        }
    });
});