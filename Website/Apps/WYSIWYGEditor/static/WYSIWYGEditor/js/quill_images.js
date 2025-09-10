import Quill from './quill-engine.js'
import { updateImagesForServer } from './editor_media_handler.js'

export class ImageTooltip{
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
        ImageTooltip.create(node)
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
        var value = this.boundsContainer.dataset.src
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
            tooltip.boundsContainer.classList.add('do-not-change')
            tooltip.boundsContainer.src = value
            tooltip.boundsContainer.dataset.src = value
            updateImagesForServer()
        }
        ImageTooltip.remove();
    }
    remove(tooltip){
        tooltip.hide();
        tooltip.boundsContainer.remove()
        updateImagesForServer()
        ImageTooltip.remove();
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


class CustomImage extends Quill.import('blots/block'){
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.classList.add('image')
        domNode.classList.add('rounded-2xl')
        domNode.classList.add('dynamic_image')
        domNode.classList.add('image-bordered')
        if (!domNode.classList.contains('do-not-change')){
            domNode.src = `${PATH}loading.svg`
        }
        domNode.addEventListener('click', ()=>{
            let tooltip = new ImageTooltip(domNode, 'https://someref.to/picture/')
            tooltip.show()
        })
    }
}
CustomImage.tagName = 'img'
CustomImage.blotName = 'my-image'
Quill.register({'formats/image': CustomImage})

// Text under image
class TextUnderImage extends Quill.import('blots/block'){}
TextUnderImage.tagName = 'div'
TextUnderImage.blotName = "text-under-image"
TextUnderImage.className = "ttw-explain_under"
Quill.register({'formats/text-under-image': TextUnderImage})