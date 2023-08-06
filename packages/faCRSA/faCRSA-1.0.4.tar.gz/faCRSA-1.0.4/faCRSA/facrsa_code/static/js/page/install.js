var clipboard = new ClipboardJS('#clipboard');
clipboard.on('success', function(e) {
    layer.msg('Copied!');
});