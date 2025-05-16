// Abbreviation
// Abbreviation tooltip
class AbbrTooltip extends Quill.import('ui/tooltip'){
    static create(value){
        let node = super.create(value)
        return node
    }
    static remove(){
        let prev = document.querySelector('.abbr-tooltip')
        if (prev){
            prev.remove()
        }
        document.querySelector('footer').classList.remove('active')
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
        this.insertRemoveBtn()
        document.querySelector('footer').classList.add('active')
    }
    insertTextInput(){
        this.textbox = document.createElement('input')
        this.textbox.setAttribute('type', 'text')
        var value = this.boundsContainer.getAttribute('title')
        if (value != 'unasigned'){
            this.textbox.value = value
        }
        else{
            this.textbox.placeholder = document.querySelector('#abbr_placeholder').innerText
        }
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
            tooltip.boundsContainer.setAttribute('title', value)
        }
        AbbrTooltip.remove();
    }
    setHeight(height){
        this.root.style.height = `${height}px`
    }
    remove(tooltip){
        let text = tooltip.boundsContainer.innerText
        tooltip.boundsContainer.outerHTML = text
        tooltip.hide();
        AbbrTooltip.remove();
    }

}

class Abbr extends Quill.import('blots/inline'){
    static create(value){
        let node = super.create(value);
        node.setAttribute('title', 'unasigned')
        return node
    }
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.addEventListener('click', (ev) => { 
            let abbrTooltip = new AbbrTooltip(quill, this.domNode)
            //abbrTooltip.setHeight(document.querySelector('footer').getBoundingClientRect().height)
            abbrTooltip.setHeight(48)
            abbrTooltip.show()
        })
    }
}
Abbr.tagName = 'abbr'
Abbr.blotName = 'abbr'
Abbr.className = 'abbreviation'
Quill.register({'formats/abbr': Abbr})