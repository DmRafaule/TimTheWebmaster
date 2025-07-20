function onReady(){
    var tds = document.querySelectorAll('.td')
    tds.forEach((td) => {
        var phrases = td.dataset.phrases
        if (phrases){
            var ref = td.getAttribute('id')
            // Вставит по одной анкорной ссылке на фразу 
            // И вставить только по одной анкорной ссылке на блок текста
            String(phrases).split(',').forEach((phrase) => {
                var text_blocks = document.querySelectorAll('.text:not(.ref_internal,.ref_downloadables,.ref)')
                for (var j = 0; j < text_blocks.length; j++){
                    var pos = text_blocks[j].innerHTML.toLowerCase().search(phrase)
                    if (pos != -1 ){
                        text_blocks[j].innerHTML = text_blocks[j].innerHTML.replace(phrase,`<a class='${ref}' href="#${ref}">${phrase}</a>`)
                        text_blocks[j].classList.add('ref_internal')
                        break
                    }
                }
            })
            // Перемещаемся к определению
            document.querySelectorAll(`.${ref}`).forEach( (inn_ref) => {
                inn_ref.addEventListener('click', (ev) =>{
                    // Предотвращаем скачок к цели
                    ev.preventDefault();
                    // Меняем состояние
                    history.pushState(null, '',`#${ref}`)
                    // Прыгаем к цели
                    var target = document.querySelector(`#${ref}`)
                    target.scrollIntoView({behavior: "smooth", block: "center", inline: "center"});
                })
            })
        }
    })
}


if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
} else {
    onReady()
}