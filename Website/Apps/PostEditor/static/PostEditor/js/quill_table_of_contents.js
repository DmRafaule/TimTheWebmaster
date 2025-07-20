class TableOfContents extends Quill.import('blots/block'){
    static create(value){
        let node = super.create(value);
        return node
    }
    constructor(scroll, domNode){
        super(scroll, domNode)
        var header = document.createElement('h2')
        header.innerText = document.querySelector('#table_of_content_text').innerText
        header.style.marginTop = '0'
        header.style.borderBottom = '2px solid gray'
        header.style.marginBottom = '0'
        domNode.insertAdjacentElement('beforeend', header)

        document.querySelectorAll('h2,h3,h4,h5,h6').forEach( (heading) => {
            if (!heading.classList.contains('table_of_contents')){
                var container_headers_element = document.createElement('div')
                let tag_name  = heading.nodeName.toLowerCase()
                let padding = "padder-5"
                if( tag_name  == 'h2')
                    padding = "padder-5"
                else if (tag_name  == 'h3')
                    padding = "padder-10"
                else if (tag_name  == 'h4')
                    padding = "padder-15"
                else if (tag_name  == 'h5')
                    padding = "padder-20"
                else if (tag_name  == 'h6')
                    padding = "padder-25"
                container_headers_element.classList.add(padding)
                container_headers_element.style.display = 'flex'
                container_headers_element.style.gap = '8px'
                container_headers_element.style.alignItems = 'center'
                container_headers_element.style.marginTop = '10px'
                
                var container_headers_sign = document.createElement('p')
                container_headers_sign.innerText = tag_name
                container_headers_sign.style.border = '1px solid grey'
                container_headers_sign.style.borderRadius = '50%'
                container_headers_sign.style.padding = '5px'
                container_headers_sign.style.color = 'grey'
                container_headers_sign.style.fontSize = '10px'
                var container_headers_text = document.createElement('p')
                container_headers_text.innerText = heading.innerText
                container_headers_element.insertAdjacentElement('beforeend', container_headers_sign)
                container_headers_element.insertAdjacentElement('beforeend', container_headers_text)
                
                this.domNode.insertAdjacentElement('beforeend', container_headers_element)
            }
        })
    }
}
TableOfContents.tagName = 'div'
TableOfContents.blotName = 'table_of_contents'
TableOfContents.className = 'table_of_contents'

Quill.register({'formats/table_of_contents': TableOfContents})

function RunTableOfContents(){
    let range = quill.getSelection()
    let blot = Quill.find(quill.getLeaf(range.index)[0].domNode).parent
    let DOMnode = blot.domNode
    switch (DOMnode.tagName){
        case 'H2':
        case 'H3':
        case 'H4':
        case 'H5':
        case 'H6':
            document.querySelectorAll('.table_of_contents').forEach((el) => {
                let prev = quill.scroll.find(el)
                if (prev){
                    prev.remove()
                }
            })
            var container = quill.scroll.create(TableOfContents.blotName)
            var ref = quill.scroll.children.head
            quill.scroll.insertBefore(container, ref)
            break
    }
}

function InitTableOfContents(quill, options) {
    quill.on(Quill.events.TEXT_CHANGE, RunTableOfContents);
}
  
Quill.register('modules/table_of_contents', InitTableOfContents);
document.querySelector('#toc_module').addEventListener('click', (event)=>{
    
    if (event.target.checked){
        quill.emitter.addListener(Quill.events.TEXT_CHANGE, RunTableOfContents, quill.emitter) 
    }else{
        quill.emitter.removeListener(Quill.events.TEXT_CHANGE, RunTableOfContents, quill.emitter, false) 
    }
})