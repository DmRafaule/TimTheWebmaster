import Quill from './quill-engine.js'
import { SomeBlockHandler } from './quill_blocks.js'
import { CodeBlockHandler } from './quill_codeblock.js';
import { CustomTable, TableTooltip } from './quill_table.js';
import { AbbrTooltip } from './quill_abbr.js';
import { VideoTooltip } from './quill_videos.js';
import { ImageTooltip } from './quill_images.js';
import { LinkTooltip } from './quill_links.js';
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


let Font = Quill.import('formats/font')
Font.whitelist = ['open-sans', 'roboto-slab', 'advent-pro']
Quill.register(Font, true)

let Size = Quill.import('attributors/style/size')
Size.whitelist = ['64px','54px', '42px', '32px', '28px', '24px', '20px', '18px', '16px', '14px']
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
    }
}

const quill = new Quill('#editor', {
    modules: {
        keyboard: {
            bindings: bindings
        },
        tooltip: false,
        clipboard: true,
        table: true,
        toolbar: {
            container: '#editor-side-menu',
            handlers: {
                'attention': SomeBlockHandler,
                'danger': SomeBlockHandler,
                'interesting': SomeBlockHandler,
                'question': SomeBlockHandler,
                'termin': SomeBlockHandler,
                'quote': SomeBlockHandler,
                'code-block': CodeBlockHandler,
                'table': CustomTable.handler,
            }
        }
    },
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
                var abbrtooltip = new AbbrTooltip(blot.domNode, 'Описание')
                abbrtooltip.show()
                break
            case 'A':
                var linktooltip = new LinkTooltip(blot.domNode, 'http://website.com/ext-ref/#')
                linktooltip.show()
                break
            case 'VIDEO':
                var tooltip = new VideoTooltip(blot.domNode, 'video url or #')
                tooltip.show()
                break
            case 'IMG':
                var tooltip = new ImageTooltip(blot.domNode, 'https://someimt.to/link/')
                tooltip.show()
                break
            default:
                TableTooltip.remove()
                AbbrTooltip.remove()
                LinkTooltip.remove()
                VideoTooltip.remove()
                ImageTooltip.remove()
        }
    }
});

window.quill = quill
window.Quill = Quill