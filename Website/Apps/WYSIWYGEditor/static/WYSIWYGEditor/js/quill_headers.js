import Quill from './quill-engine.js'
import { genHeaderId } from "../../../../../Main/static/Components/Containers/TableOfContent/table_of_content";

export class HeaderTooltip{
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
        HeaderTooltip.create(node)
        this.boundsContainer = node
        this.root = document.querySelector('#ql-custom-tooltip')
        this.root.innerText = ""
        this.insertTextInput(placeholder)
        this.insertBtn(this.save, gettext("Сохранить"))
        this.insertBtn(this.copy, gettext("Копировать"))
    }

    insertTextInput(placeholder){
        this.textbox = document.createElement('input')
        this.textbox.setAttribute('type', 'text')
        this.textbox.classList.add('link-input-ql-editor')
        var value = this.boundsContainer.getAttribute('id')
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
        var id = tooltip.boundsContainer.getAttribute('id')
        navigator.clipboard.writeText(id);
        HeaderTooltip.remove();
    }
    save(tooltip) {
        let value = tooltip.textbox.value;
        if (value.length > 0){
            tooltip.boundsContainer.classList.add('do_not_updateHeaderId')
            tooltip.boundsContainer.setAttribute('id', value) 
        }
        HeaderTooltip.remove();
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

let Header = Quill.import('formats/header')
class CustomHeader extends Header{
    static create(value){
        let node = super.create(value);
        if (Number(value) == 1){
            node.setAttribute('class','title');
        }
        else{
            node.setAttribute('class','paragraph');
        }


        return node;    
    }
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.addEventListener('click', (ev) => { 
            if (!domNode.classList.contains("do_not_updateHeaderId")){
                domNode.setAttribute('id', genHeaderId(domNode))
            }
            let tooltip = new HeaderTooltip(this.domNode, '#ID_SOME')
            tooltip.show()
        })
    }
}
Quill.register(CustomHeader, true)