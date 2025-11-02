function onTab(tabnavitems, tab){
    // Меняем состояние
    history.pushState(null, '',`${tab.getAttribute('href')}`)
    const targetId = tab.getAttribute('href').substring(1);
    const targetElement = document.getElementById(targetId);

    if (targetElement) {
    // Плавный скролл к элементу, чтобы он появился на экране
        targetElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
	tabnavitems.forEach((tabitem) => {
		tabitem.classList.remove('ttw-tab_active')
		tabitem.classList.remove('ref-int_no-sign')
	})
	tab.classList.add('ttw-tab_active')
	tab.classList.add('ref-int_no-sign')
}
// grab and stash elements
export function initTabs(){
    const tabgroups = document.querySelectorAll('tabs')
    tabgroups.forEach( tabgroup => {
        var anchor = window.location.hash.substring(1);
        let previousScrollLeft = 0;
        var tabnav = tabgroup.querySelector(':scope .ttw-tabs-navigation')  
        var tabnext_button_nav = tabnav.querySelector(':scope .ttw-tabs-next-tab')
        var tabprev_button_nav = tabnav.querySelector(':scope .ttw-tabs-prev-tab')
        var tabbody = tabgroup.querySelector(':scope .ttw-tabs-body')  
        var tabnavitems  = tabnav.querySelectorAll(':scope .ttw-tabs-navigation-tab ')
        /*
        for each nav link
        - animate color based on the scroll timeline
        - color is active when its the current index*/
        tabnavitems.forEach(navitem => {
            navitem.addEventListener('click', (event)=>{
                // Предотвращаем скачок к цели
                event.preventDefault();
                navitem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                onTab(tabnavitems, navitem)
            })
            if (anchor === navitem.getAttribute('href').substring(1)){
                onTab(tabnavitems, navitem)
            }
            // Добавить переключение при скролинге при помощи клавиатуры
        })
        tabbody.addEventListener('scroll', (event)=>{
            var anchor = window.location.hash;
            var navitem = tabnav.firstElementChild
            if (anchor.length > 0){
                var navitem = tabnav.querySelector(`:scope a[href="${anchor}"]`)
            }
            const currentScrollLeft = tabbody.scrollLeft;
            // Прокрутка на право
            if (currentScrollLeft > previousScrollLeft) {
                if (navitem.nextElementSibling){
                    if (!navitem.nextElementSibling.classList.contains('ttw-tabs-navigation-buttons')){
                        navitem.nextElementSibling.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                        onTab(tabnavitems, navitem.nextElementSibling)
                    }
                }
            // Прокрутка на лево
            } else if (currentScrollLeft < previousScrollLeft) {
                if (navitem.previousElementSibling){
                    if (!navitem.previousElementSibling.classList.contains('ttw-tabs-navigation-buttons')){
                        navitem.previousElementSibling.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                        onTab(tabnavitems, navitem.previousElementSibling)
                    }
                }
            }
            previousScrollLeft = currentScrollLeft;
        })
        // Добавим возможность переключать табы по кнопкам
        if (tabnext_button_nav){
            tabnext_button_nav.addEventListener('click', (event)=>{
                var anchor = window.location.hash;
                var navitem = tabnav.firstElementChild
                if (anchor.length > 0){
                    var toProceed = false
                    tabnavitems.forEach((item)=>{
                        if (item.getAttribute('href') === anchor){
                            toProceed = true
                        }
                    })
                    if (toProceed)
                        var navitem = tabnav.querySelector(`:scope a[href="${anchor}"]`)
                }
                if (navitem.nextElementSibling){
                    if (!navitem.nextElementSibling.classList.contains('ttw-tabs-navigation-buttons')){
                        navitem.nextElementSibling.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                        onTab(tabnavitems, navitem.nextElementSibling)
                    }
                }

            })
        }
        // Добавим возможность переключать табы по кнопкам
        if (tabprev_button_nav){
            tabprev_button_nav.addEventListener('click', (event)=>{
                var anchor = window.location.hash;
                var navitem = tabnav.firstElementChild
                if (anchor.length > 0){
                    var toProceed = false
                    tabnavitems.forEach((item)=>{
                        if (item.getAttribute('href') === anchor){
                            toProceed = true
                        }
                    })
                    if (toProceed){
                        var navitem = tabnav.querySelector(`:scope a[href="${anchor}"]`)
                    }
                }
                if (navitem.previousElementSibling){
                    if (!navitem.previousElementSibling.classList.contains('ttw-tabs-navigation-buttons') ){
                        navitem.previousElementSibling.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                        onTab(tabnavitems, navitem.previousElementSibling)
                    }
                }
            })
        }
    })
}