function startTime(initJSTime) {

    // page-load JS-time
    if (typeof initJSTime === 'undefined') {
        initJSTime = new Date();
    }
    // Current JS-Time
    var todayJS = new Date();

    // Converting Server-Time when page is loaded to JS-Date
    nowDateInput = $('#todaydate').html();
    nn = nowDateInput.split(',');
    if (nn[1] == 0) {
        nn[1] = 12;
    } else {
        nn[1] = nn[1] - 1;
    }
    var today = new Date(nn[0], nn[1], nn[2], nn[3], nn[4], nn[5]);

    // Difference between Current JS-time and page-load JS-time
    var initDiffmSec = todayJS - initJSTime;

    // Setting Clock-Time as sum of Server-Time and Difference
    today.setMilliseconds(today.getMilliseconds()+initDiffmSec);

    // Output-presentation of the clock
    var h=today.getHours();
    var m=today.getMinutes();
    var s=today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('#clock').innerHTML = h+":"+m+":"+s;

    // next function call
    var t = setTimeout(function(){startTime(initJSTime)},1000);
}

function checkTime(i) {
    if (i<10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}