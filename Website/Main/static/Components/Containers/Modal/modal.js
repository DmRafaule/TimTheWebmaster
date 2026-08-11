class Modal{
    constructor(){
        this.modal = document.querySelector('modal')
        this.close_btn = this.modal.querySelector('#close_modal')
        this.close_btn.addEventListener('click', () => {this.close()})
        this.modal_window = this.modal.querySelector('#modal-window')
        this.container = this.modal.querySelector('#modal-content')
    }

    close(){
        this.modal.classList.add('not_active_modal')
        this.container.innerHTML = ""
    }

    open(msg){
        this.modal.classList.remove('not_active_modal')
        this.container.innerHTML = msg
    }
}

window.modal = new Modal()