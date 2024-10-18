// Load custom icons for custom formaters
var icons = Quill.import("ui/icons");
icons["abbr"] = readFile(`${PATH}PostEditor/img/abbr.svg`)
icons["external-link"] = readFile(`${PATH}PostEditor/img/link.svg`)
icons["internal-link"] = readFile(`${PATH}PostEditor/img/paragraph.svg`)
icons["downloadable-link"] = readFile(`${PATH}PostEditor/img/download.svg`)
icons["attention"] = readFile(`${PATH}PostEditor/img/blockAttention.svg`)
icons["quote"] = readFile(`${PATH}PostEditor/img/blockQuote.svg`)
icons["danger"] = readFile(`${PATH}PostEditor/img/blockDangerouse.svg`)
icons["interesting"] = readFile(`${PATH}PostEditor/img/blockInteresting.svg`)
icons["question"] = readFile(`${PATH}PostEditor/img/blockQuestion.svg`)
icons["termin"] = readFile(`${PATH}PostEditor/img/blockTermin.svg`)
icons["toggle-block"] = readFile(`${PATH}PostEditor/img/hidden-block.svg`)
icons["table"] = readFile(`${PATH}PostEditor/img/table.svg`)
icons["tabs"] = readFile(`${PATH}PostEditor/img/tabs.svg`)
icons["horizontal-line"] = readFile(`${PATH}PostEditor/img/hr.svg`)
icons["my-video"] = readFile(`${PATH}PostEditor/img/video.svg`)
icons["bold"] = readFile(`${PATH}PostEditor/img/bold.svg`)
icons["italic"] = readFile(`${PATH}PostEditor/img/italic.svg`)
icons["strikethrough"] = readFile(`${PATH}PostEditor/img/strikethrough.svg`)
icons["underline"] = readFile(`${PATH}PostEditor/img/underline.svg`)
icons["image"] = readFile(`${PATH}PostEditor/img/img.svg`)
//icons["list-decimal"] = readFile(`${PATH}PostEditor/img/list-decimal.svg`)
//icons["list-disk"] = readFile(`${PATH}PostEditor/img/list-disk.svg`)

let List = Quill.import('formats/list')
class CustomList extends List{
    static create(value) {
        const node = super.create();
        node.style.listStyleType = value
        return node;
    }
}
Quill.register(CustomList, true)


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
}
Quill.register(CustomHeader, true)

let Font = Quill.import('formats/font')
Font.whitelist = ['open-sans', 'roboto-slab', 'advent-pro']
Quill.register(Font, true)

let Size = Quill.import('attributors/style/size')
Size.whitelist = ['16px', '14px']
Quill.register(Size, true)

let Block = Quill.import('blots/block');
Block.tagName = 'div'
class TextBlock extends Block{    

    static create(value){
        let node = super.create(value);
        node.setAttribute('class','text');
        return node;    
    } 
}
Quill.register(TextBlock, true)



let Bold = Quill.import('formats/bold')
Bold.tagName = 'b'
Quill.register(Bold, true)

let Italic = Quill.import('formats/italic')
Italic.tagName = 'i'
Quill.register(Italic, true)

let Tooltip = Quill.import('ui/tooltip')
class LinkTooltip extends Tooltip{
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
        this.textbox.placeholder = placeholder
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

let Inline = Quill.import('blots/inline')
class InternalLink extends Inline{
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


class DownloadableLink extends Inline{
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

class ExternalLink extends Inline{
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


// Base block for other blocks
class SomeBlock extends Block{
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
// Code block 
let codeBlockContainer = Quill.import('formats/code-block-container')
class MyCodeBlockContainer extends codeBlockContainer{
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

let codeBlock = Quill.import('formats/code-block')
class MyCodeBlock extends codeBlock{
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

class HorizontalLine extends Block{}
HorizontalLine.tagName = 'hr'
HorizontalLine.blotName = 'horizontal-line'
Quill.register({'formats/horizontal-line': HorizontalLine})
// Abbreviation
// Abbreviation tooltip
class AbbrTooltip extends Tooltip{
    static create(value){
        let node = super.create(value)
        return node
    }
    static remove(){
        let prev = document.querySelector('.abbr-tooltip')
        if (prev){
            prev.remove()
        }
    }
    constructor(scroll, domNode ){
        let prev = document.querySelector('.abbr-tooltip')
        if (prev){
            prev.remove()
        }
        super(scroll, domNode);
        this.textbox = null
        this.root.innerText = ""
        this.root.classList.add('abbr-tooltip')
        this.insertTextInput()
        this.insertAddBtn()
    }
    insertTextInput(){
        this.textbox = document.createElement('input')
        this.textbox.setAttribute('type', 'text')
        this.textbox.placeholder = "Введите аббревиатуру"
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
        add.classList.add('ql-action')
        add.classList.add('text_button')
        add.innerText = document.querySelector('#save_text').innerText
        add.addEventListener('click', () => {this.save(this)})
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
            tooltip.boundsContainer.setAttribute('title', value)
        }
        AbbrTooltip.remove();
    }
    setHeight(height){
        this.root.style.height = `${height}px`
    }

}

class Abbr extends Inline{
    static create(value){
        let node = super.create(value);
        node.setAttribute('title', 'unasigned')
        return node
    }
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.addEventListener('click', (ev) => { 
            let abbrTooltip = new AbbrTooltip(quill, this.domNode)
            abbrTooltip.setHeight(document.querySelector('footer').getBoundingClientRect().height)
            abbrTooltip.show()
        })
    }
}
Abbr.tagName = 'abbr'
Abbr.blotName = 'abbr'
Abbr.className = 'abbreviation'
Quill.register({'formats/abbr': Abbr})

// Video
let Video = Quill.import('formats/video')
class CustomVideo extends Video{
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.classList.add('dynamic_image')
        domNode.controls = 'true'
        domNode.preload = 'metadata'
        let tooltip = new VideoTooltip(quill, domNode, 'video URL or #')
        tooltip.setHeight(document.querySelector('footer').getBoundingClientRect().height)
        tooltip.show()
    }
}
CustomVideo.tagName = 'video'
CustomVideo.className = 'my-video'
CustomVideo.blotName = 'my-video'
Quill.register(CustomVideo, true)

// Images
let Image = Quill.import('formats/image')
class CustomImage extends Image{
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.classList.add('image')
        domNode.classList.add('dynamic_image')
        domNode.classList.add('image-bordered')
    }
}
Quill.register(CustomImage, true)

// Tables
// Table tooltip
class TableTooltip extends Tooltip{
    constructor(scroll, domNode, placeholder = ''){
        let prev = document.querySelector('.table-tooltip')
        if (prev){
            prev.remove()
        }
        super(scroll, domNode);
        this.textbox = null
        this.root.innerText = ""
        this.root.classList.add('table-tooltip')
        this.insertBtn(`${PATH}PostEditor/img/table-insert-row-above.svg`, document.querySelector('#insertRowAbove_text').innerText, this.insertRowAbove)
        this.insertBtn(`${PATH}PostEditor/img/table-insert-row-after.svg`, document.querySelector('#insertRowBelow_text').innerText, this.insertRowBelow)
        this.insertBtn(`${PATH}PostEditor/img/table-insert-column-after.svg`, document.querySelector('#insertColumnAfter_text').innerText, this.insertColumnAfter)
        this.insertBtn(`${PATH}PostEditor/img/table-insert-column-before.svg`, document.querySelector('#insertColumnBefore_text').innerText, this.insertColumnBefore)
        this.insertSep()
        this.insertBtn(`${PATH}PostEditor/img/table-delete-row.svg`, document.querySelector('#removeRow_text').innerText, this.removeRow)
        this.insertBtn(`${PATH}PostEditor/img/table-delete-column.svg`, document.querySelector('#removeCol_text').innerText, this.removeCol)
        this.insertSep()
        this.insertBtn(`${PATH}PostEditor/img/table-delete.svg`, document.querySelector('#removeTable_text').innerText, this.removeTable)
    }

    insertSep(){
        let container = document.createElement('div')
        container.classList.add('el-expandable')
        this.root.insertAdjacentElement('beforeend', container)
    }

    insertBtn(iconPath, popupText, callback){
        let icon = document.createElement('img')
        icon.classList.add('icon')
        icon.classList.add('dynamic_image')
        icon.width = '32'
        icon.height = '32'
        icon.src = iconPath
        let container = document.createElement('div')
        container.classList.add('button')
        container.classList.add('squered_button')
        container.addEventListener('click', callback)
        container.insertAdjacentElement('beforeend', icon)
        let tip = document.createElement('abbr')
        tip.setAttribute('title', popupText)
        tip.insertAdjacentElement('beforeend', container)
        this.root.insertAdjacentElement('beforeend', tip)
    }

    insertRowAbove(event){
        const table = quill.getModule('table');
        table.insertRowAbove()
    }

    insertRowBelow(event){
        const table = quill.getModule('table');
        table.insertRowBelow()
    }

    insertColumnAfter(event){
        const table = quill.getModule('table');
        table.insertColumnRight()
    }

    insertColumnBefore(event){
        const table = quill.getModule('table');
        table.insertColumnLeft()
    }

    removeRow(event){
        const table = quill.getModule('table');
        table.deleteRow()
    }

    removeCol(event){
        const table = quill.getModule('table');
        table.deleteColumn()
    }

    removeTable(event){
        const table = quill.getModule('table');
        table.deleteTable()
        TableTooltip.remove()
    }

    static remove(){
        let prev = document.querySelector('.table-tooltip')
        if (prev){
            prev.remove()
        }
    }

    cancel() {
        this.hide();
        this.restoreFocus();
    }

    restoreFocus() {
        this.quill.focus({ preventScroll: true });
    }
    setHeight(height){
        this.root.style.height = `${height}px`
    }

}
let Table = Quill.import('modules/table')
class CustomTable extends Table{
    static handler(value){
        const table = quill.getModule('table');
        if (value){
            table.insertTable(1,1)
            let tooltip = new TableTooltip(quill, table.getTable()[0])
            tooltip.setHeight(document.querySelector('footer').getBoundingClientRect().height)
            tooltip.show()
        }else{
            TableTooltip.remove()
            table.deleteTable()
        }
    }
}
Quill.register(CustomTable, true)


const quill = new Quill('#editor', {
    modules: {
        syntax: true,
        clipboard: true,
        table: true,
        toolbar: {
            container: '#toolbar-container',
            handlers: {
                'attention': SomeBlockHandler,
                'danger': SomeBlockHandler,
                'interesting': SomeBlockHandler,
                'question': SomeBlockHandler,
                'termin': SomeBlockHandler,
                'quote': SomeBlockHandler,
                'table': CustomTable.handler,
            }
        }
    },
    placeholder: document.querySelector('#main_placeholder_quill').innerText,
    theme: 'snow',
});

quill.on('selection-change', (range, oldRange, source) => {
    let blot = Quill.find(event.target);
    if (blot){
        switch(blot.domNode.tagName){
            case 'TD':
                const table = quill.getModule('table');
                var tooltip = new TableTooltip(quill, table.getTable()[0])
                tooltip.show()
                break
            case 'ABBR':
                break
            case 'A':
                break
            default:
                TableTooltip.remove()
                AbbrTooltip.remove()
                LinkTooltip.remove()
        }
    }
});


// Override behavior of hat buttons. They will not closed if clicked outside of them
onClickOutsideHat = (button, body, callback) => {}