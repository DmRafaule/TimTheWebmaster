import Quill from './quill-engine.js'
export class LinkTooltip{
    static create(value){
        let prev = document.querySelector('#ql-custom-tooltip')
        if (prev){
            prev.classList.remove('hidden')
        }
    }
    static remove(){
        let prev = document.querySelector('#ql-custom-tooltip')
        if (prev){
            prev.classList.add('hidden')
        }
    }
    constructor(node, placeholder){
        LinkTooltip.create(node)
        this.boundsContainer = node
        this.root = document.querySelector('#ql-custom-tooltip')
        this.root.innerText = ""
        this.insertTextInput(placeholder)
        this.insertBtn(this.save, gettext("Сохранить"))
        this.insertBtn(this.copy, gettext("Копировать"))
        this.insertBtn(this.remove, gettext("Удалить"))
    }

    insertTextInput(placeholder){
        this.textbox = document.createElement('input')
        this.textbox.setAttribute('type', 'text')
        this.textbox.classList.add('link-input-ql-editor')
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
              this.hide();
              event.preventDefault();
            } else if (event.key === 'Escape') {
              this.hide();
              event.preventDefault();
            }
        });
        this.root.insertAdjacentElement('beforeend', this.textbox)
    }
    insertBtn(callback, text){
        let add = document.createElement('div')
        add.classList.add('ttw-button')
        add.classList.add('ttw-button_action')
        add.classList.add('ttw-button_squared')
        add.addEventListener('click', () => {callback(this)})
        let add_text_cont = document.createElement('div')
        add_text_cont.classList.add('ttw-button_squared')
        add_text_cont.classList.add('p-2')
        add_text_cont.innerText = text 
        add.insertAdjacentElement('afterbegin',add_text_cont)
        this.root.insertAdjacentElement('beforeend', add)
    }
    copy(tooltip){
        var link = tooltip.boundsContainer.getAttribute('href')
        navigator.clipboard.writeText(link);
        LinkTooltip.remove();
    }
    save(tooltip) {
        let value = tooltip.textbox.value;
        if (value.length > 0){
            tooltip.boundsContainer.parentElement.classList.add('ref')
            tooltip.boundsContainer.classList.add('do_not_updateDownloadablesForServer')
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
    show(){
        if(this.root){
            this.root.classList.remove('hidden')
        }
    }
    hide(){
        if(this.root){
            this.root.classList.add('hidden')
        }
    }

    


}

class InternalLink extends Quill.import('blots/inline'){
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.addEventListener('click', (ev) => { 
            domNode.setAttribute('ref', 'me')
            let tooltip = new LinkTooltip(this.domNode, '#ID_SOME')
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
            let tooltip = new LinkTooltip(this.domNode, '?')
            tooltip.show()
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
            let tooltip = new LinkTooltip(this.domNode, 'http(s)://website.com')
            tooltip.show()
        })
    }
    
}
ExternalLink.tagName  = 'a'
ExternalLink.className  = 'ref-ext'
ExternalLink.blotName = 'external-link'
Quill.register({'formats/external-link': ExternalLink})