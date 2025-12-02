import Quill from './quill-engine.js'
import { updateImagesForServer } from './editor_media_handler.js'

export class ImageTooltip{
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
        ImageTooltip.create(node)
        this.boundsContainer = node
        this.root = document.querySelector('#ql-custom-tooltip')
        this.root.innerText = ""
        this.insertTextInput(placeholder)
        if (is_superuser){
            var name = gettext("Загрузить")
            var callback = this.onFileSelect
            if (this.boundsContainer.dataset.serverPk){
                name = gettext("✓ | Заменить")
                callback = this.onFileChange
            }
            this.insertUploadBtn(callback, name)
        }
        this.insertBtn(this.save, gettext("Сохранить"))
        this.insertBtn(this.remove, gettext("Удалить"))
    }

    insertTextInput(placeholder){
        this.textbox = document.createElement('input')
        this.textbox.setAttribute('type', 'text')
        this.textbox.id = "tooltip_input_1"
        this.textbox.classList.add('link-input-ql-editor')
        var value = this.boundsContainer.dataset.src
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
        hidden_input.accept = "*.webp,*.png,*.jpg,*.svg,*.gif"
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


    save(tooltip) {
        let value = tooltip.textbox.value;
        if (value.length > 0){
            let document_input = document.querySelector('#uploaded_document')
            if (document_input.files.length > 0){
                if (is_superuser){
                    window.contextLoader.startLoad('load_more')
                    var id = tooltip.boundsContainer.dataset.serverPk
                    if (id){
                        ImageTooltip.addToServer(true, tooltip.boundsContainer)
                    } 
                    else{
                        ImageTooltip.addToServer(false, tooltip.boundsContainer)
                    }
                }
                else{
                    tooltip.boundsContainer.classList.add('do-not-change')
                    tooltip.boundsContainer.src = value
                    tooltip.boundsContainer.dataset.src = value
                }
            }
            else{
                if(is_superuser){
                    window.contextLoader.startLoad('load_more')
                    ImageTooltip.removeFromServer(tooltip.boundsContainer)
                }
                tooltip.boundsContainer.classList.add('do-not-change')
                tooltip.boundsContainer.src = value
                tooltip.boundsContainer.dataset.src = value
                tooltip.boundsContainer.dataset.serverPk = ""
            }
            updateImagesForServer()
        }
        ImageTooltip.remove();
    }

    remove(tooltip){
        tooltip.hide();
        if(is_superuser){
            window.contextLoader.startLoad('load_more')
            ImageTooltip.removeFromServer(tooltip.boundsContainer)
        }
        tooltip.boundsContainer.remove()
        updateImagesForServer()
        ImageTooltip.remove();
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
                    toaster.notify(gettext("Изображение уже удалено"),'info')   
                }
                else if (response.status == 403 ){
                    toaster.notify(gettext("У тебя нет достаточных прав удалять изображения"),'error')   
                }
            }
            else{
                // Удаляет изображение с холста
                toaster.notify(gettext("Изображение успешно удалено"),'success')
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
        form_data.append('type', 3) // То есть файл
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
                    toaster.notify(gettext("Изображение успешно загружено на сервер и добавленно в статью"),'success')
                    boundsContainer.classList.add('do-not-change')
                    boundsContainer.src = response['file']
                    boundsContainer.dataset.serverPk = response['id']
                    boundsContainer.dataset.src = response['file']
                    boundsContainer.alt = ""
                })
        })
        .catch(error => {
            window.contextLoader.stopLoad('load_more')
            toaster.notify(error,'error')
            console.error('There was a problem with your fetch operation:', error);
            boundsContainer.classList.add('do-not-change')
            boundsContainer.src = value
            boundsContainer.dataset.src = value
        });
    }
}


class CustomImage extends Quill.import('blots/block'){
    constructor(scroll, domNode){
        super(scroll, domNode);
        domNode.classList.add('image')
        domNode.classList.add('rounded-2xl')
        domNode.classList.add('dynamic_image')
        domNode.classList.add('image-bordered')
        if (!domNode.classList.contains('do-not-change')){
            domNode.src = `${PATH}loading.svg`
        }
        domNode.addEventListener('click', ()=>{
            let tooltip = new ImageTooltip(domNode, 'https://someref.to/picture/')
            tooltip.show()
        })
    }
}
CustomImage.tagName = 'img'
CustomImage.blotName = 'my-image'
Quill.register({'formats/image': CustomImage})

// Text under image
class TextUnderImage extends Quill.import('blots/block'){}
TextUnderImage.tagName = 'div'
TextUnderImage.blotName = "text-under-image"
TextUnderImage.className = "ttw-explain_under"
Quill.register({'formats/text-under-image': TextUnderImage})