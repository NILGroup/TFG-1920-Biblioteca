function writeCookie (key, value, days) {
    var date = new Date();

    days = days || 1;

    date.setTime(+ date + (days * 86400000)); //24 * 60 * 60 * 1000

    window.document.cookie = key + "=" + value + "; expires=" + date.toGMTString() + "; path=/";

    return value;
};

$(document).ready(function() {
	$('#accept-privacity').click(function(event) {
        document.cookie='janetWeb-privacy=true';
        writeCookie('janetWeb-privacy', 'true', 30);
        window.location.replace('/');
    })
})
