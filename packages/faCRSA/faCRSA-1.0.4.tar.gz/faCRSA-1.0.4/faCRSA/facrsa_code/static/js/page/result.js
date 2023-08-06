layui.use('table', function () {
    var table = layui.table;
    table.render({
        elem: '#result',
        url: "/api/getResult/" + document.getElementById('tid').getAttribute('value'),
        toolbar: '#toolbarDemo',
        title: 'Analysis Result',
        unresize: true,
        text: "System Error",
        cols: [
            [{
                field: 'tid',
                title: 'ID',
                width: 80,
                templet: '#xuhao',
                unresize: true,
                sort: true,
                align: 'center',
                type: 'numbers'
            }, {
                field: 'image',
                title: 'Image',
                //templet: '#imageUrl',
                width: 150,
                align: 'center'
            }, {
                field: 'out_image',
                title: 'Output Image',
                width: 150,
                templet: function (d) {
                    let rid = d.rid
                    let tid = d.tid
                    return '<span onclick="viewImage(' + '\'' + rid + ''  + '\',\'' + ''  + tid + '\'' + ')" style="color: #018749">View</span>'
                },
                align: 'center'
            }, {
                field: 'trl',
                title: 'Total Root Length(cm)',
                width: 180,
                align: 'center',
                sort: true
            }, {
                field: 'trpa',
                title: 'Total Root Projected Area(cm²)',
                width: 180,
                align: 'center',
                sort: true
            }, {
                field: 'tsa',
                title: 'Total Root Surface Area(cm²)',
                width: 180,
                align: 'center',
                sort: true
            }, {
                field: 'trv',
                title: 'Total Root Volume(cm³)',
                width: 180,
                align: 'center',
                sort: true
            }, {
                field: 'mrl',
                title: 'Primary Root Length(mm)',
                width: 180,
                sort: true,
                align: 'center'
            }, {
                field: 'mrpa',
                title: 'Primary Root Projected Area(cm²)',
                width: 180,
                align: 'center',
                sort: true
            }, {
                field: 'msa',
                title: 'Primary Root Surface Area(cm²)',
                width: 180,
                align: 'center',
                sort: true
            }, {
                field: 'mrv',
                title: 'Primary Root Volume(cm³)',
                width: 180,
                align: 'center',
                sort: true
            }, {
                field: 'cha',
                title: 'Convex Hull Area(cm²)',
                width: 180,
                align: 'center',
                sort: true
            }, {
                field: 'al',
                title: 'Angle_Left(°)',
                width: 180,
                align: 'center',
                sort: true
            }, {
                field: 'ac',
                title: 'Angle_Center(°)',
                width: 180,
                align: 'center',
                sort: true
            }, {
                field: 'ar',
                title: 'Angle_Right(°)',
                width: 180,
                align: 'center',
                sort: true
            }, {
                field: 'mrd',
                title: 'Max Root Depth(cm)',
                width: 180,
                align: 'center',
                sort: true
            }]
        ],
        page: true
    });
    table.on('toolbar(test)', function (obj) {
    });
});

function viewImage(rid,tid) {
    console.log(rid)
    console.log(tid)
    var index = layer.open({
        type: 2,
        title: "Output Image",
        content: '/showimg/' + rid + '/' + tid,
        area: ['320px', '195px'],
        maxmin: true
    });
    layer.full(index);
}