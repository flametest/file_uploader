$(document).ready(function(){
    var output_text = $("#output")[0];
    var r = new Resumable({
        target: "/upload",
        simultaneousUploads: 5,
    });

    if (!r.support) {
        output_text.innerHTML="Your browser is too old. Try <a href=\"https://www.google.com/chrome/?\">Chrome</a>";
    };

    r.assignBrowse($("#file")[0]);
    r.on("fileAdded",function (file) {
        // when you select the file and click ok
        r.upload();
    });
    r.on("fileProgress",function(file) {
        // progress
        progress_num = Math.floor(r.progress()*100);
        output_text.innerHTML = progress_num + '%';
        if (progress_num == 100) {
            output_text.innerHTML = "Server is processing your file please wait.";
        };
    });
    r.on("complete",function() {
        // upload complete
        output_text.innerHTML = "Uploaded complete!";
    });
})