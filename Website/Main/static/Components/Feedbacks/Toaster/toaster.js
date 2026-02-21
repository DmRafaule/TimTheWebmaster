class Toaster{
    constructor(){
        this.container = document.querySelector('.toaster-container')
        var header = document.querySelector("header")
        this.container.style.top = header.getBoundingClientRect().height  + "px"
        this.notification = document.querySelector('.toaster-blank').cloneNode(true)
        this.notification.classList.remove('toaster-blank')
        this.notification.classList.remove('toaster-inactive')
    }

    notify(msg, status, time = 7){
        var notif = this.notification.cloneNode(true)
        notif.querySelector(".toaster_text").innerText = msg
        notif.addEventListener('animationend', () => {
            notif.remove()
        });
        notif.style.animationDuration = time + 's'
        //
        notif.querySelector(".toaster_text").classList.add(`toaster_${status}`)
        notif.querySelector(".remove_all_action").addEventListener('click', (ev)=>{
            this.clean()
        })
        notif.querySelector('.remove_one_action').addEventListener('click', (ev)=>{
            notif.remove()
        })
        this.container.insertAdjacentElement('beforeend', notif)
    }

    clean(){
        this.container.querySelectorAll('.toaster:not(.toaster_blank)').forEach( (child) => {
            child.remove()
        })
    }
}

window.toaster = new Toaster()