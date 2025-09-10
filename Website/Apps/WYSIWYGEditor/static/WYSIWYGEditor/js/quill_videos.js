import Quill from './quill-engine.js'
import {TextBlock} from './quill_blocks.js'

export class VideoTooltip{
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
    constructor(node, placeholder = ''){
        VideoTooltip.create(node)
        this.boundsContainer = node
        this.root = document.querySelector('#ql-custom-tooltip')
        this.root.innerText = ""
        this.insertTextInput(placeholder)
        this.insertBtn(this.save, gettext("Сохранить"))
        this.insertBtn(this.remove, gettext("Удалить"))
    }
    insertTextInput(placeholder){
        this.textbox = document.createElement('input')
        this.textbox.setAttribute('type', 'text')
        this.textbox.classList.add('link-input-ql-editor')
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


// Video
class CustomVideo extends TextBlock{
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.classList.add('dynamic_image')
        domNode.classList.add('my-video')
        domNode.controls = 'true'
        domNode.preload = 'metadata'
        let tooltip = new VideoTooltip(domNode, 'video URL or #')
        tooltip.show()
    }
}
CustomVideo.tagName = 'video'
CustomVideo.className = 'my-video'
CustomVideo.blotName = 'my-video'
Quill.register({'formats/my-video': CustomVideo})