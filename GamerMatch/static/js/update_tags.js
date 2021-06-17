function update_tags(){
    var tags_str = document.getElementById('the_tags').getAttribute("data-simple-tags");
    var tags_submit = document.getElementById('id-tags');
    tags_submit.innerHTML = tags_str;
    document.getElementById("true-submit-tags").click();
}