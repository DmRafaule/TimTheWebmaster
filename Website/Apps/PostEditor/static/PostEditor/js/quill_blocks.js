
class TextBlock extends Quill.import('blots/block'){    

    static create(value){
        let node = super.create(value);
        node.setAttribute('class','text');
        return node;    
    } 
}
TextBlock.tagName = 'div'
Quill.register(TextBlock, true)

// Base block for other blocks
class SomeBlock extends Quill.import('blots/block'){
    static create(value){
        let node = super.create(value);
        let values = value.split(',')
        node.dataset.type = values[1]
        node.dataset.imagepath = values[0]
        return node
    }
    constructor(scroll, domNode) {
        super(scroll, domNode);
        let legend = document.createElement('legend')
        legend.classList.add(domNode.dataset.type)
        let legend_icon = document.createElement('img')
        legend_icon.classList.add('icon')
        legend_icon.classList.add('dynamic_image')
        legend_icon.setAttribute('width', 32)
        legend_icon.setAttribute('height', 32)
        legend_icon.setAttribute('src', domNode.dataset.imagepath)
        legend_icon.dataset.src  = domNode.dataset.imagepath
        legend.insertAdjacentElement('afterbegin', legend_icon)
        domNode.insertAdjacentElement('afterbegin', legend)
    }
}

function SomeBlockHandler(value){
    let values = value.split(',')
    let frm = values[1]
    let range = quill.getSelection()
    let text = quill.getText(range.index, range.length)
    if (quill.getFormat()[frm]) {
        quill.format(quill.scroll.query(frm).prototype.constructor.blotName, false);
    } else {
        quill.format(frm, value);
    }
}

// Quote block
class QuoteBlock extends SomeBlock{
    static create(value){
        let node = super.create(value);
        return node
    }
}
QuoteBlock.blotName = 'quote'
QuoteBlock.tagName  = 'fieldset'
Quill.register({'formats/quote': QuoteBlock})
// Attention block
class AttentionBlock extends SomeBlock{
    static create(value){
        let node = super.create(value);
        return node
    }
}
AttentionBlock.blotName = 'attention'
AttentionBlock.tagName  = 'fieldset'
Quill.register({'formats/attention': AttentionBlock})
// Danger block
class DangerBlock extends SomeBlock{
    static create(value){
        let node = super.create(value);
        return node
    }
}
DangerBlock.blotName = 'danger'
DangerBlock.tagName  = 'fieldset'
Quill.register({'formats/danger': DangerBlock})
// Interesting block
class InterestingBlock extends SomeBlock{
    static create(value){
        let node = super.create(value);
        return node
    }
}
InterestingBlock.blotName = 'interesting'
InterestingBlock.tagName  = 'fieldset'
Quill.register({'formats/interesting': InterestingBlock})
// Question block
class QuestionBlock extends SomeBlock{
    static create(value){
        let node = super.create(value);
        return node
    }
}
QuestionBlock.blotName = 'question'
QuestionBlock.tagName  = 'fieldset'
Quill.register({'formats/question': QuestionBlock})
// Termin block
class TerminBlock extends SomeBlock{
    static create(value){
        let node = super.create(value);
        return node
    }
}
TerminBlock.blotName = 'termin'
TerminBlock.tagName  = 'fieldset'
Quill.register({'formats/termin': TerminBlock})