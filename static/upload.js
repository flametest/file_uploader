$(document).ready(function(){
    var output_text = document.getElementById("output")
    var r = new Resumable({
        target: "/upload",
        simultaneousUploads: 5,
    });

    if (!r.support) {
        output_text.innerHTML="Your browser is too old. Try <a href=\"https://www.google.com/chrome/?\">Chrome</a>";
    };

    r.assignBrowse($("#file")[0]);
    r.on("fileAdded",function (file) {
        // body...
        r.upload();
    });
});