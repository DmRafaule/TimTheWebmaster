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


const quill = new Quill('#editor', {
    modules: {
        syntax: true,
        clipboard: true,
        table: true,
        table_of_contents: true,
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
            default:
                TableTooltip.remove()
                AbbrTooltip.remove()
                LinkTooltip.remove()
        }
    }
});


// Override behavior of hat buttons. They will not closed if clicked outside of them
onClickOutsideHat = (button, body, callback) => {}