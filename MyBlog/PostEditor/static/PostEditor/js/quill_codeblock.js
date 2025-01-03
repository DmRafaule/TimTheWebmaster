// Code block 
class MyCodeBlockContainer extends Quill.import('formats/code-block-container'){
    static create(value){
        let node = super.create(value);
        return node
    }
    constructor(scroll, domNode) {
        super(scroll, domNode);
        let legend = document.createElement('legend')
        legend.classList.add('code')
        legend.classList.add('padder')
        let legend_icon = createIcon(PATH+'Post/img/blockCode.svg')
        legend_icon.dataset.src = PATH+'Post/img/blockCode.svg'
        let copy_icon = createIcon(PATH + 'Post/img/copy.svg')
        copy_icon.dataset.src = PATH+'Post/img/copy.svg'
        copy_icon.classList.add('code-block_copy')
        copy_icon.classList.add('button')
        copy_icon.classList.add('bordered_button')
        copy_icon.classList.add('squered_button')
        copy_icon.setAttribute('onclick', "var text = '' ;this.parentElement.parentElement.querySelectorAll('.ql-code-block').forEach((line)=>{ text += line.innerText + '\\n'}); navigator.clipboard.writeText(text); notificator.notify('Copied','success')")
        let legend_separator = document.createElement('div')
        legend_separator.classList.add('code-block-legend_separator')
        legend.insertAdjacentElement('afterbegin', copy_icon)
        legend.insertAdjacentElement('afterbegin', legend_separator)
        legend.insertAdjacentElement('afterbegin', legend_icon)
        domNode.insertAdjacentElement('afterbegin', legend)
        
    }
}


MyCodeBlockContainer.tagName = 'fieldset'
Quill.register(MyCodeBlockContainer, true)


class MyCodeBlock extends Quill.import('formats/code-block'){
    static create(value){
        let node = super.create(value);
        node.dataset.language = value
        return node
    }
    constructor(scroll, domNode) {
        super(scroll, domNode);
    }
}
Quill.register(MyCodeBlock, true)