function onReady(){
    var save_btn = document.querySelector('#save_btn_submit')
    if (save_btn)
        save_btn.addEventListener('click', saveQuill)
    var load_btn = document.querySelector('#load_btn')
    if (load_btn)
        load_btn.addEventListener('click', listQuill)
    
}


if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
} else {
    onReady()
}