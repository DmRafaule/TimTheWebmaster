class ModalLoader{
    constructor(){
        this.container = document.querySelector('loader')
    }
    startLoad(){
        this.container.classList.add('loader_active')
    }
    stopLoad(){
        this.container.classList.remove('loader_active')
    }
}

class ContextLoader{
    constructor(selector){
        this.containers = document.querySelectorAll(selector)
    }
    startLoad(id){
        this.containers.forEach( (container) => {
            if (container.getAttribute('id') === `context-loader-${id}`){
                container.classList.add('loader_active')
            }
        })
    }
    stopLoad(id){
        this.containers.forEach( (container) => {
            if (container.getAttribute('id') === `context-loader-${id}`){
                container.classList.remove('loader_active')
            }
        })
    }
}

window.modalLoader = new ModalLoader()
window.contextLoader = new ContextLoader('.context-loader')