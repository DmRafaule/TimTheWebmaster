class VideoTooltip extends Quill.import('ui/tooltip'){
    static create(value){
        let node = super.create(value)
        return node
    }
    static remove(){
        let prev = document.querySelector('.video-tooltip')
        if (prev){
            prev.remove()
        }
        document.querySelector('footer').classList.remove('active')
    }
    constructor(scroll, domNode, placeholder = ''){
        let prev = document.querySelector('.video-tooltip')
        if (prev){
            prev.remove()
        }
        super(scroll, domNode);
        this.textbox = null
        this.root.innerText = ""
        this.root.classList.add('video-tooltip')
        this.insertTextInput(placeholder)
        this.insertAddBtn()
        this.insertRemoveBtn()
        document.querySelector('footer').classList.add('active')
    }
    insertTextInput(placeholder){
        this.textbox = document.createElement('input')
        this.textbox.setAttribute('type', 'text')
        var value = this.boundsContainer.getAttribute('src')
        if (value != null){
            this.textbox.value = value
        }
        else{
            this.textbox.placeholder = placeholder 
        }
        this.textbox.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
              this.save(this);
              event.preventDefault();
            } else if (event.key === 'Escape') {
              this.cancel();
              event.preventDefault();
            }
        });
        this.root.insertAdjacentElement('beforeend', this.textbox)
    }
    insertAddBtn(){
        let add = document.createElement('div')
        add.classList.add('add_button')
        add.classList.add('text_button')
        add.innerText = document.querySelector('#save_text').innerText
        add.addEventListener('click', () => {this.save(this)})
        this.root.insertAdjacentElement('beforeend', add)
    }
    insertRemoveBtn(){
        let add = document.createElement('div')
        add.classList.add('remove_button')
        add.classList.add('text_button')
        add.innerText = document.querySelector('#remove_text').innerText
        add.addEventListener('click', () => {this.remove(this)})
        this.root.insertAdjacentElement('beforeend', add)
    }

    cancel() {
        this.hide();
        this.restoreFocus();
    }
    restoreFocus() {
        this.quill.focus({ preventScroll: true });
    }
    save(tooltip) {
        let value = tooltip.textbox.value;
        if (value.length > 0){
            tooltip.boundsContainer.setAttribute('src', value)
            tooltip.boundsContainer.dataset.src = value
            tooltip.boundsContainer.dataset.text = ''
            tooltip.boundsContainer.classList.add('do_not_updateDownloadablesForServer')
        }
        VideoTooltip.remove();
    }
    remove(tooltip){
        let text = tooltip.boundsContainer.innerText
        tooltip.boundsContainer.outerHTML = text
        tooltip.hide();
        VideoTooltip.remove();
    }
    setHeight(height){
        this.root.style.height = `${height}px`
    }

}


// Video
class CustomVideo extends TextBlock{
    constructor(scroll, domNode){
        console.log('Here')
        super(scroll, domNode);
        domNode.classList.add('dynamic_image')
        domNode.classList.add('my-video')
        domNode.controls = 'true'
        domNode.preload = 'metadata'
        let tooltip = new VideoTooltip(quill, domNode, 'video URL or #')
        //tooltip.setHeight(document.querySelector('footer').getBoundingClientRect().height)
        tooltip.setHeight(48)
        tooltip.show()
    }
}
CustomVideo.tagName = 'video'
CustomVideo.className = 'my-video'
CustomVideo.blotName = 'my-video'
Quill.register({'formats/my-video': CustomVideo})