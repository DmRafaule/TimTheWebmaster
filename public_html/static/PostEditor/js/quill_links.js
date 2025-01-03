class LinkTooltip extends Quill.import('ui/tooltip'){
    static create(value){
        let node = super.create(value)
        return node
    }
    static remove(){
        let prev = document.querySelector('.link-tooltip')
        if (prev){
            prev.remove()
        }
    }
    constructor(scroll, domNode, placeholder = ''){
        let prev = document.querySelector('.link-tooltip')
        if (prev){
            prev.remove()
        }
        super(scroll, domNode);
        this.textbox = null
        this.root.innerText = ""
        this.root.classList.add('link-tooltip')
        this.insertTextInput(placeholder)
        this.insertAddBtn()
        this.insertRemoveBtn()
    }
    insertTextInput(placeholder){
        this.textbox = document.createElement('input')
        this.textbox.setAttribute('type', 'text')
        var value = this.boundsContainer.getAttribute('href')
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
            tooltip.boundsContainer.parentElement.classList.add('ref')
            tooltip.boundsContainer.setAttribute('href', value)
        }
        LinkTooltip.remove();
    }
    remove(tooltip){
        let text = tooltip.boundsContainer.innerText
        tooltip.boundsContainer.outerHTML = text
        tooltip.hide();
        LinkTooltip.remove();
    }
    setHeight(height){
        this.root.style.height = `${height}px`
    }

}

class InternalLink extends Quill.import('blots/inline'){
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.addEventListener('click', (ev) => { 
            domNode.setAttribute('ref', 'me')
            let tooltip = new LinkTooltip(quill, this.domNode, '#ID_SOME')
            tooltip.setHeight(document.querySelector('footer').getBoundingClientRect().height)
            tooltip.show()
        })
    }
}
InternalLink.tagName  = 'a'
InternalLink.className  = 'ref-int'
InternalLink.blotName = 'internal-link'
Quill.register({'formats/internal-link': InternalLink})


class DownloadableLink extends Quill.import('blots/inline'){
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.setAttribute('ref', 'me')
        domNode.addEventListener('click', (ev) => { 
            let tooltip = new LinkTooltip(quill, this.domNode, '?')
            tooltip.setHeight(document.querySelector('footer').getBoundingClientRect().height)
            tooltip.show()
            tooltip.root.querySelector('input').remove()
            tooltip.root.querySelector('.add_button').remove( )
        })
    }

    
}
DownloadableLink.tagName  = 'a'
DownloadableLink.className  = 'ref-downloadable'
DownloadableLink.blotName = 'downloadable-link'
Quill.register({'formats/downloadable-link': DownloadableLink})

class ExternalLink extends Quill.import('blots/inline'){
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.setAttribute('target', '_blank')
        domNode.setAttribute('ref', 'noreferrer nofollow external')
        domNode.addEventListener('click', (ev) => { 
            let tooltip = new LinkTooltip(quill, this.domNode, 'http(s)://website.com')
            tooltip.setHeight(document.querySelector('footer').getBoundingClientRect().height)
            tooltip.show()
        })
    }
    
}
ExternalLink.tagName  = 'a'
ExternalLink.className  = 'ref-ext'
ExternalLink.blotName = 'external-link'
Quill.register({'formats/external-link': ExternalLink})