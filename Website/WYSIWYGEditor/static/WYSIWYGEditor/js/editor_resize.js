function onReady(){

    // Изменяем высоту редактора при необходимости
    const resizeObserver = new ResizeObserver(entries => {
        for (const entry of entries) {
            // 'entry' represents a ResizeObserverEntry for the observed element.
            // You can access its new dimensions via 'contentRect' or 'contentBoxSize'.
            const newHeight = entry.contentRect.height;
            const editorSideMenuHeight = parseFloat(window.getComputedStyle(document.querySelector('#editor-side-menu')).height)
            const editorBottomPaddingInPixels = parseFloat(window.getComputedStyle(document.querySelector('#editor')).paddingBottom)
            var height_setter = document.querySelector('#editor-height-setter')
            height_setter.style.height = `${newHeight + editorSideMenuHeight + editorBottomPaddingInPixels}px`

            // You can also compare with a previous height if you stored it.
            // if (newHeight !== previousHeight) {
            //     // Do something specific when height changes
            // }
        }
    });
    resizeObserver.observe(document.querySelector('#editor'));
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
} else {
    onReady()
}
