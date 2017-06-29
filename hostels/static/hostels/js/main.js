function dayDiff(datestr1, datestr2) {
    diff = new Date(datestr2) - new Date(datestr1);
    return diff / (24*60*60*1000);
}

function todayStr() {
    var today = new Date();
    var yyyy = today.getFullYear().toString();
    var mm = (today.getMonth()+1).toString(); // getMonth() is zero-based
    var dd  = today.getDate().toString();
    return yyyy + '-' + (mm[1]?mm:"0"+mm[0]) + '-' + (dd[1]?dd:"0"+dd[0]); // padding
};

$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
         }
     } 
});