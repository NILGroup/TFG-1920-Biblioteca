function writeCookie (key, value, days) {
    var date = new Date();

    days = days || 1;

    date.setTime(+ date + (days * 86400000)); //24 * 60 * 60 * 1000

    window.document.cookie = key + "=" + value + "; expires=" + date.toGMTString() + "; path=/";

    return value;
};
function getRandomId()
{
    var retvalue = "";
    i = 0;
    while (i < 12)
    {
        retvalue += Math.random().toString(36).substring(2, 15);
        i++;
    }
    return retvalue;

}

$(document).ready(function() {
	$('#accept-privacity').click(function(event) {
        //document.cookie='janetWeb-privacy=true';
        writeCookie('janetWeb', JSON.stringify({accept_policy: 'true', id: getRandomId()}), 3650);
        window.location.replace($SCRIPT_ROOT);
    })
})
