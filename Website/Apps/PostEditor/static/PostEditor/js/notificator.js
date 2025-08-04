class Notificator{
    constructor(){
        this.container = document.querySelector('.notificator-container')
        var header = document.getElementById("header")
        this.container.style.top = header.getBoundingClientRect().height  + "px"
        this.notification = document.querySelector('.notificator-blank').cloneNode()
        this.notification.classList.remove('notificator-blank')
        this.notification.classList.remove('notificator-inactive')
    }

    notify(msg, status, time){
        this.clean()
        var notif = this.notification.cloneNode()
        notif.innerText = msg
        if (time == null){
            time = 5
        }
        notif.style.animationDuration = time + 's'
        notif.classList.add(`notificator_${status}`)
        notif.addEventListener('animationend', (ev)=>{
            notif.remove()
        })
        this.container.insertAdjacentElement('beforeend', notif)
    }

    clean(){
        if (this.container.childNodes.length >=5){
            this.container.childNodes.forEach( (child) => {
                child.remove()
            })
        }
    }
}

let notificator = new Notificator()