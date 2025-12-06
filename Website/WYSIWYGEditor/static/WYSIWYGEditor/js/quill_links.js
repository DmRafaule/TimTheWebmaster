import Quill from './quill-engine.js'
export class LinkTooltip{
    static create(value){
        let prev = document.querySelector('#ql-custom-tooltip')
        if (prev){
            prev.classList.remove('hidden')
        }
    }
    static remove(){
        let prev = document.querySelector('#ql-custom-tooltip')
        if (prev){
            prev.classList.add('hidden')
        }
    }
    constructor(node, placeholder){
        LinkTooltip.create(node)
        this.boundsContainer = node
        this.root = document.querySelector('#ql-custom-tooltip')
        this.root.innerText = ""
        this.insertTextInput(placeholder)
        this.insertBtn(this.save, gettext("Сохранить"))
        this.insertBtn(this.copy, gettext("Копировать"))
        this.insertBtn(this.remove, gettext("Удалить"))
        if (is_superuser && this.boundsContainer.classList.contains('ref-downloadable')){
            var name = gettext("Загрузить")
            var callback = this.onFileSelect
            if (this.boundsContainer.dataset.serverPk){
                name = gettext("✓ | Заменить")
                callback = this.onFileChange
            }
            this.insertUploadBtn(callback, name)
        }
    }

    insertTextInput(placeholder){
        this.textbox = document.createElement('input')
        this.textbox.setAttribute('type', 'text')
        this.textbox.id = "tooltip_input_1"
        this.textbox.classList.add('link-input-ql-editor')
        var value = this.boundsContainer.getAttribute('href')
        if (value != null){
            this.textbox.value = value
        }
        else{
            this.textbox.placeholder = placeholder 
        }
        this.textbox.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
              this.save(this);
              this.hide();
              event.preventDefault();
            } else if (event.key === 'Escape') {
              this.hide();
              event.preventDefault();
            }
        });
        this.root.insertAdjacentElement('beforeend', this.textbox)
    }
    insertBtn(callback, text){
        let add = document.createElement('div')
        add.classList.add('ttw-button')
        add.classList.add('ttw-button_action')
        add.classList.add('ttw-button_squared')
        add.addEventListener('click', () => {callback(this)})
        let add_text_cont = document.createElement('div')
        add_text_cont.classList.add('ttw-button_squared')
        add_text_cont.classList.add('p-2')
        add_text_cont.innerText = text 
        add.insertAdjacentElement('afterbegin',add_text_cont)
        this.root.insertAdjacentElement('beforeend', add)
    }
    insertUploadBtn(callback, text){
        let label = document.createElement('label')
        label.htmlFor = "uploaded_document"
        let add = document.createElement('div')
        add.classList.add('ttw-button')
        add.classList.add('ttw-button_action')
        add.classList.add('ttw-button_squared')
        let add_text_cont = document.createElement('div')
        add_text_cont.classList.add('ttw-button_squared')
        add_text_cont.classList.add('p-2')
        add_text_cont.innerText = text 
        add.insertAdjacentElement('afterbegin',add_text_cont)
        let hidden_input = document.createElement('input')
        hidden_input.addEventListener('change', callback)
        hidden_input.type = "file"
        hidden_input.id = "uploaded_document"
        hidden_input.hidden = true
        add.insertAdjacentElement('beforeend', hidden_input)
        label.insertAdjacentElement('beforeend', add)
        this.root.insertAdjacentElement('beforeend', label)
    }

    onFileSelect(event){
        const selectedFile = event.target.files[0]; // Get the first selected file
        if (selectedFile) {
            document.querySelector('#uploaded_document').parentElement.firstElementChild.textContent = gettext("✓ | Заменить")
            document.querySelector('#tooltip_input_1').value = selectedFile.name
        } else {
            console.log('No file selected.');
        }
    }
    onFileChange(event){
        const selectedFile = event.target.files[0]; // Get the first selected file
        if (selectedFile) {
            document.querySelector('#uploaded_document').parentElement.firstElementChild.textContent = gettext("✓ | Заменить")
            document.querySelector('#tooltip_input_1').value = selectedFile.name
        } else {
            console.log('No file selected.');
        }
    }

    copy(tooltip){
        var link = tooltip.boundsContainer.getAttribute('href')
        navigator.clipboard.writeText(link);
        LinkTooltip.remove();
    }
    save(tooltip) {
        let value = tooltip.textbox.value;
        if (value.length > 0){
            let document_input = document.querySelector('#uploaded_document')
            if (document_input){
                if (document_input.files.length > 0){
                    window.contextLoader.startLoad('load_more')
                    if (is_superuser && tooltip.boundsContainer.classList.contains('ref-downloadable')){
                        var id = tooltip.boundsContainer.dataset.serverPk
                        if (id){
                            LinkTooltip.addToServer(true, tooltip.boundsContainer)
                        } 
                        else{
                            LinkTooltip.addToServer(false, tooltip.boundsContainer)
                        }
                    }
                    else{
                        tooltip.boundsContainer.parentElement.classList.add('ref')
                        tooltip.boundsContainer.classList.add('do_not_updateDownloadablesForServer')
                        tooltip.boundsContainer.setAttribute('href', value)
                    }
                }
                else{
                    if(is_superuser && tooltip.boundsContainer.classList.contains('ref-downloadable')){
                        LinkTooltip.removeFromServer(tooltip.boundsContainer)
                    }
                    tooltip.boundsContainer.parentElement.classList.add('ref')
                    tooltip.boundsContainer.classList.add('do_not_updateDownloadablesForServer')
                    tooltip.boundsContainer.setAttribute('href', value)
                    tooltip.boundsContainer.dataset.serverPk = ""
                }    
            }
            else{
                if(is_superuser && tooltip.boundsContainer.classList.contains('ref-downloadable')){
                    LinkTooltip.removeFromServer(tooltip.boundsContainer)
                }
                tooltip.boundsContainer.parentElement.classList.add('ref')
                tooltip.boundsContainer.classList.add('do_not_updateDownloadablesForServer')
                tooltip.boundsContainer.setAttribute('href', value)
                tooltip.boundsContainer.dataset.serverPk = ""
            }
        }
        LinkTooltip.remove();
    }
    remove(tooltip){
        let text = tooltip.boundsContainer.innerText
        tooltip.boundsContainer.outerHTML = text
        if(is_superuser && tooltip.boundsContainer.classList.contains('ref-downloadable')){
            window.contextLoader.startLoad('load_more')
            LinkTooltip.removeFromServer(tooltip.boundsContainer)
        }
        tooltip.hide();
        LinkTooltip.remove();
    }
    show(){
        if(this.root){
            this.root.classList.remove('hidden')
        }
    }
    hide(){
        if(this.root){
            this.root.classList.add('hidden')
        }
    }

    static removeFromServer(boundsContainer){
        var id = boundsContainer.dataset.serverPk;
        fetch(`/api/v1/admin/media/${id}/`,{
            method: 'DELETE',
            headers: {
                "X-CSRFTOKEN": csrftoken
            }
        })
        .then( response => {
            window.contextLoader.stopLoad('load_more')
            if (!response.ok){
                if (response.status === 404){
                    toaster.notify(gettext("Файл уже удалён"),'info')   
                }
                else if (response.status == 403 ){
                    toaster.notify(gettext("У тебя нет достаточных прав удалять файлы"),'error')   
                }
            }
            else{
                // Удаляет изображение с холста
                toaster.notify(gettext("Файл успешно удален"),'success')
            }
        })
        .catch(error => {
            window.contextLoader.stopLoad('load_more')
            toaster.notify(error,'error')
            console.error('There was a problem with your fetch operation:', error);
        });
    }

    static addToServer(isUpdate=False, boundsContainer){
        let document_input = document.querySelector('#uploaded_document')
        var id = boundsContainer.dataset.serverPk;
        // Сохраняет изображение на сервер
        var form_data = new FormData()
        form_data.append('csrfmiddlewaretoken', csrftoken)
        form_data.append('type', 1) // То есть файл
        form_data.append('lang_type', language_code)
        form_data.append('file', document_input.files[0])
        var my_url = "/api/v1/admin/media/" 
        var my_method = "POST"
        if (isUpdate){
            my_url = `/api/v1/admin/media/${id}/` 
            my_method = "PUT"
        }
        fetch(my_url,{
            method: my_method,
            body: form_data,
            headers: {
                "X-CSRFTOKEN": csrftoken
            }
        })
        .then( response => {
            window.contextLoader.stopLoad('load_more')
            if (!response.ok)
                return response.json().then( response => {
                    toaster.notify(response['msg'],'error')   
                })
            else
                return response.json().then( response =>{
                    toaster.notify(gettext("Файл успешно загружен на сервер и добавленн в статью"),'success')
                    boundsContainer.parentElement.classList.add('ref')
                    boundsContainer.classList.add('do_not_updateDownloadablesForServer')
                    boundsContainer.setAttribute('href', response['file'])
                    boundsContainer.dataset.serverPk = response['id']
                })
        })
        .catch(error => {
            window.contextLoader.stopLoad('load_more')
            toaster.notify(error,'error')
            console.error('There was a problem with your fetch operation:', error);
            boundsContainer.parentElement.classList.add('ref')
            boundsContainer.classList.add('do_not_updateDownloadablesForServer')
            boundsContainer.setAttribute('href', value)
        });
    }



}

class InternalLink extends Quill.import('blots/inline'){
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.addEventListener('click', (ev) => { 
            domNode.setAttribute('ref', 'me')
            let tooltip = new LinkTooltip(this.domNode, '#ID_SOME')
            tooltip.show()
        })
    }
}
InternalLink.tagName  = 'a'
InternalLink.className  = 'ref-int'
InternalLink.blotName = 'internal-link'
Quill.register({'formats/internal-link': InternalLink})


class DownloadableLink extends Quill.import('blots/inline'){
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.setAttribute('ref', 'me')
        domNode.addEventListener('click', (ev) => { 
            let tooltip = new LinkTooltip(this.domNode, '?')
            tooltip.show()
        })
    }

    
}
DownloadableLink.tagName  = 'a'
DownloadableLink.className  = 'ref-downloadable'
DownloadableLink.blotName = 'downloadable-link'
Quill.register({'formats/downloadable-link': DownloadableLink})

class ExternalLink extends Quill.import('blots/inline'){
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.setAttribute('target', '_blank')
        domNode.setAttribute('ref', 'noreferrer nofollow external')
        domNode.addEventListener('click', (ev) => { 
            let tooltip = new LinkTooltip(this.domNode, 'http(s)://website.com')
            tooltip.show()
        })
    }
    
}
ExternalLink.tagName  = 'a'
ExternalLink.className  = 'ref-ext'
ExternalLink.blotName = 'external-link'
Quill.register({'formats/external-link': ExternalLink})