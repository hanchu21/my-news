function confirm_delete_keyword(kid) {
    if (confirm("Are you sure you want to delete this keyword? This action cannot be reversed.")) {
        window.location.href = "/deletekeyword/" + kid;
    }
}

function fill_edit_form(kid, keyword) {
    document.querySelector("#keyword-id").value = kid;
    document.querySelector("#save-keyword").value = keyword;
;
}

function confirm_delete_source(sid) {
    if (confirm("Are you sure you want to delete this source? This action cannot be reversed.")) {
        window.location.href = "/deletesource/" + sid;
    }
}