// Code block 
class MyCodeBlockContainer extends Quill.import('formats/code-block-container'){
    static create(value){
        let node = super.create(value);
        let ui_buttons = document.querySelector('.ql-ui')
        return node
    }
    constructor(scroll, domNode) {
        super(scroll, domNode);
        let legend = document.createElement('legend')
        legend.classList.add('code')
        let legend_icon = createIcon(PATH+'PostEditor/img/blockCode.svg')
        legend_icon.dataset.src = PATH+'PostEditor/img/blockCode.svg'
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