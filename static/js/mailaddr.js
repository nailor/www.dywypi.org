$(document).ready(function() {
    var user = 'jyrki';
    var host = 'dywypi.org';
    $('.ma').each(function() {
        var addr, text = $(this).text();
        if($(this).hasClass('s'))
            text = addr = user + '@' + host;
        else if($(this).hasClass('b'))
            text = addr = user + '+blog@' + host;
        else
            addr = user + '@' + host;
        $(this).html('<a href="mailto:' + addr + '">' + text + '</a>');
    });
});
