
function getAllExternalLinks(){
    var list = []
    var page = document.querySelector('#content_post_article')
    var links = page.querySelectorAll('a')
    links.forEach(link => {
        var ref = link.getAttribute('href')
        if (ref){
            if (!(ref.startsWith(`https://${DOMAIN_NAME}`)) && (ref.startsWith(`https://`) || ref.startsWith(`http://`))){
                list.push(ref)
            }
        }
    });
    return [...new Set(list)]
}


function onReady(){
    var links = getAllExternalLinks()
    var ex_link_cont = document.querySelector('#ex_links')
    var ex_link_list = document.querySelector('#ex_links_list')
    var ex_link_exmpl_cont = document.querySelector('#list_el_exmpl_cont')
    if (links.length > 0){
        ex_link_exmpl_cont.classList.remove('is_none')
        for(var i = 0; i < links.length; i++){
            var cont = ex_link_exmpl_cont.cloneNode(true)
            var link = cont.querySelector('a')
            link.setAttribute('href', links[i])
            link.innerText = links[i]
            ex_link_list.insertAdjacentElement('beforeend', cont)
        }
        ex_link_exmpl_cont.classList.add('is_none')
    }
    else{
        ex_link_cont.remove()
    }
}


if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
} else {
    onReady()
}