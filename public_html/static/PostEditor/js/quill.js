// Load custom icons for custom formaters
var icons = Quill.import("ui/icons");
icons["abbr"] = null
icons["code-block"] = null
icons["table"] = null 
icons["bold"] = null
icons["italic"] = null
icons["strike"] = null
icons["underline"] = null
icons["image"] = null 
icons["video"] = null 
//icons["list-decimal"] = readFile(`${PATH}PostEditor/img/list-decimal.svg`)

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

let Bold = Quill.import('formats/bold')
Bold.tagName = 'b'
Quill.register(Bold, true)

let Italic = Quill.import('formats/italic')
Italic.tagName = 'i'
Quill.register(Italic, true)

class HorizontalLine extends Quill.import('blots/block'){}
HorizontalLine.tagName = 'hr'
HorizontalLine.blotName = 'horizontal-line'
Quill.register({'formats/horizontal-line': HorizontalLine})

const bindings = {
    indent: {
        key: 'Tab',
        handler(range) {
            let blot = Quill.find(this.quill.getLeaf(range.index)[0].domNode).parent
            let domNode = blot.domNode
            var indent_depth = 5
            var indent_start_check_counter = 0
            for (var i = 1; i <= indent_depth; i++){
                if (!domNode.classList.contains(`indent-${i}`)){
                    indent_start_check_counter++
                }
            }
            if (indent_start_check_counter === indent_depth){
                domNode.classList.add(`indent-0`)
            }

            for (var i = 0; i < 5; i++){
                if (domNode.classList.contains(`indent-${i}`)){
                    domNode.classList.remove(`indent-${i}`)
                    domNode.classList.add(`indent-${i+1}`)
                    break
                }
            }
            return false;
        },
    },
    outdent: {
        key: 'Tab',
        shiftKey: true,
        handler(range) {
            let blot = Quill.find(this.quill.getLeaf(range.index)[0].domNode).parent
            let domNode = blot.domNode
            for (var i = 1; i <= 5; i++ ){
                if (domNode.classList.contains(`indent-${i}`)){
                    domNode.classList.remove(`indent-${i}`)
                    if (i != 1)
                        domNode.classList.add(`indent-${i-1}`)
                    break
                }
            }
            return false;
        },
    },
}

const quill = new Quill('#editor', {
    modules: {
        keyboard: {
            bindings: bindings
        },
        syntax: true,
        clipboard: true,
        table: true,
        table_of_contents: true,
        toolbar: {
            container: '#editor-side-menu',
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
    let blot = Quill.find(quill.getLeaf(range.index)[0].domNode).parent
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
            case 'VIDEO':
                var tooltip = new VideoTooltip(quill, blot.domNode)
                tooltip.show()
                break
            default:
                TableTooltip.remove()
                AbbrTooltip.remove()
                LinkTooltip.remove()
                VideoTooltip.remove()
        }
        if (blot.domNode.classList.contains('ql-code-block') || blot.domNode.classList.contains('ql-token')){
            var cBlock = blot.domNode
            if (cBlock.classList.contains('ql-token')){
                cBlock = cBlock.parentElement
            } 
            cBlock.classList.toggle('code-block_selected')
        }
    }
});


// Override behavior of hat buttons. They will not closed if clicked outside of them
//onClickOutsideHat = (button, body, callback) => {}