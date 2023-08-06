var clipboard = new ClipboardJS('#clipboard');
clipboard.on('success', function(e) {
    layer.msg('Copied!');
});

$(window).on('load', function () {
    let checkFlag = 0;
    let id = setInterval(checkStatus, 5000);

    function checkStatus() {
        let tid = document.getElementById('tid').getAttribute('value');
        let res = detectSchedule(tid);
        if (res == 1) {
            window.location.href = "/result/" + tid;
            clearInterval(id);
        } else if (res == 0) {
            window.location.href = "/error/" + tid;
            clearInterval(id);
        }
    }

    var FLAG = 2

    function detectSchedule(tid) {
        $.ajax({
            type: "get",
            url: "/api/getSchedule/" + tid,
            dataType: "json",
            success: function (result) {
                if (result.status == '1') {
                    FLAG = 1;
                } else if (result.status == '0') {
                    FLAG = 0;
                }
            }
        });
        return FLAG;
    }
})