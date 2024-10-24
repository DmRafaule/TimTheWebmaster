function is_table_of_content_special(document_part){
    if (document_part.querySelectorAll('h1,h2,h3,h4,h5,h6').length >= 3 ){
        return true
    }else{
        return false
    }
}

function is_video_special(document_part){
    if (document_part.querySelector('video')){
        return true
    }
    else{
        return false
    }
}

function is_image_previewer_special(document_part){
    if (document_part.querySelector('.image')){
        return true
    }
    else{
        return false
    }
}

function is_tabs_special(document_part){
    if (document_part.querySelector('.tab_button')){
        return true
    }
    else{
        return false
    }
}

function is_code_special(document_part){
    if (document_part.querySelector('.code')){
        return true
    }
    else{
        return false
    }
}



function saveQuill( event ){
    var scope = document.querySelector('.ql-editor')
    var stylesheets = getRangeDomElements('#post_styles_exporter_top_line', '#post_styles_exporter_bottom_line')
    // Check special cases 
    var special_stylesheets = []
    stylesheets.forEach( (special_stylesheet) => {
        switch(special_stylesheet.dataset.special){
            case 'table_of_content':
                if (is_table_of_content_special(scope)){
                    special_stylesheets.push(special_stylesheet)
                }
                break
        }
    })
    // Check stylesheets for usage in document element (editor)
    stylesheets = checkStylesheets(scope, stylesheets)
    // Combine them all
    stylesheets = stylesheets.concat(special_stylesheets)
    
    var stylesheets_string = ''
    stylesheets.forEach((sheet)=>{
        stylesheets_string += sheet.outerHTML + '\n'
    })

    var scripts = getRangeDomElements('#post_script_exporter_top_line', '#post_script_exporter_bottom_line')
    var special_scripts = []
    // Check stylesheets for usage in document element (editor)
    scripts.forEach( (script) => {
        if (script.hasAttribute('type')){
            script.removeAttribute('type')
        }
        switch(script.dataset.special){
            case 'table_of_content':
                if (is_table_of_content_special(scope)){
                    special_scripts.push(script)
                }
                break
            case 'video':
                if (is_video_special(scope)){
                    special_scripts.push(script)
                }
                break
            case 'image_previewer':
                if (is_image_previewer_special(scope)){
                    special_scripts.push(script)
                }
                break
            case 'tabs':
                if (is_tabs_special(scope)){
                    special_scripts.push(script)
                }
                break
            case 'code':
                if (is_code_special(scope)){
                    special_scripts.push(script)
                }
                break
        }
    })
    scripts = special_scripts

    var scripts_string = ''
    scripts.forEach((script)=>{
        scripts_string += script.outerHTML + '\n'
    })

    updateImagesForServerClearSRC(scope)
    updateCodeBlock(scope)
    
    var content = scope.innerHTML
    var form = document.querySelector('#toSave')
    form.setAttribute('action', 'save/')
    form.querySelector('#id_content').value = content
    form.querySelector('#id_used_styles').value = stylesheets_string
    form.querySelector('#id_used_scripts').value = scripts_string

    // Set the default name
    var filename = form.querySelector('#id_filename').value
    if (String(filename).length == 0){
        var current = new Date().toISOString()
        current = current.replaceAll(':', '_').replace('.', '_')
        form.querySelector('#id_filename').value = `noname--${current}.html`
    }

    formData = new FormData(form)

    fetch('save/', {
        method: 'POST',
        body: formData,
    })
    .then( response => {
        if (!response.ok)
            return response.json().then( response => {
                notificator.notify(response['msg'],'error')        
            })
        else
            return response.json().then( response =>{
                notificator.notify(response['msg'],'success')
            })
    }) 
    .catch(error => {
        notificator.notify(error,'error')
        console.error('There was a problem with your fetch operation:', error);
    });

    closeModal(document.querySelector('#toSaveModal'))
}

function listQuill( event ){
    fetch('list/',{
        method: 'GET',
      })
      .then( response => {
        if (!response.ok)
            return response.json().then( response => {
                notificator.notify(response['msg'],'error')        
            })
        else
            return response.json().then( response => {
                var container = document.querySelector('#toList')
                container.innerHTML = ''
                var modal = document.querySelector('#toConfirmModal')
                response.templates.forEach( (template, indx) => {
                    var label = document.createElement('label')
                    label.classList.add('min_gap')
                    label.classList.add('row')
                    var input_cont = document.createElement('div')
                    input_cont.classList.add('row')
                    input_cont.classList.add('min_gap')
                    input_cont.classList.add('no_wrap')
                    var input = document.createElement('input')
                    input.setAttribute('name', 'templates')
                    input.setAttribute('type', 'radio')
                    input_cont.innerText = `${template['filename']} [${template['option']}]`
                    input_cont.insertAdjacentElement('afterbegin', input)
                    label.insertAdjacentElement('afterbegin', input_cont)
                    var action_cont = input_cont.cloneNode(false)
                    var download_link = document.createElement('a')
                    download_link.setAttribute('href', template['template'])
                    download_link.setAttribute('download', template['filename']);
                    var download = createIcon(PATH+'PostEditor/img/download.svg')
                    download.classList.add('button')
                    download_link.insertAdjacentElement('afterbegin', download)
                    var upload = createIcon(PATH+'PostEditor/img/upload.svg')
                    var down_attr = document.querySelector('#download_btn').getAttribute('download')
                    if (template['filename'] == down_attr ){
                        input.setAttribute('checked', 'true')
                        upload.classList.add('svg_icon_selected')   
                    }
                    upload.classList.add('button')
                    upload.dataset.ref = template['template']
                    upload.addEventListener('click', (ev) => {
                        uploadTemplateReq(ev, template['filename'])
                        // Update a save form, filename and selected option
                        var form = document.querySelector('#toSave')
                        form.querySelector('#id_filename').value = template['filename'] 
                        form.querySelectorAll('input[name="option"]').forEach( (opt) => {
                            opt.setAttribute('checked', false)
                        })
                        form.querySelectorAll('input[name="option"]').forEach( (opt) => {
                            if (opt.parentElement.innerText.replaceAll('\n','').replaceAll(' ', '') === template['option'].replaceAll('\n','').replaceAll(' ', '')){
                                opt.setAttribute('checked', true)
                            }
                        })
                    })
                    var delete_ic = createIcon(PATH+'PostEditor/img/delete.svg')
                    delete_ic.classList.add('button')
                    delete_ic.addEventListener('click', (ev) => {
                        var modal_confirm = modal.querySelector('#delete_btn_submit')
                        var modal_close = modal.querySelector('#close_btn')
                        openModal(modal)
                        modal_confirm.addEventListener('click', (event) => {
                            deleteTemplateReq(event, template['filename'])
                            modal_confirm.replaceWith(modal_confirm.cloneNode(true));
                            closeModal(modal)
                        })
                        modal_close.addEventListener('click', (event) => {
                            modal_confirm.replaceWith(modal_confirm.cloneNode(true));
                        })
                    })
                    action_cont.insertAdjacentElement('beforeend', download_link)
                    action_cont.insertAdjacentElement('beforeend', upload)
                    action_cont.insertAdjacentElement('beforeend', delete_ic)
                    label.insertAdjacentElement('beforeend', action_cont)
                    container.insertAdjacentElement('beforeend', label)
                })
                notificator.notify(response['msg'],'success')
              })
      })
      .catch(error => {
            notificator.notify(error,'error')
            console.error('There was a problem with your fetch operation:', error);
      });
}

function loadQuill( content ){
    var scope = document.querySelector('.ql-editor')
    scope.innerHTML = content
}

// Will download current content in ql-editor element and send it back as file
function downloadQuill(event){
    var scope = document.querySelector('.ql-editor')
    var content = scope.innerHTML

    var icon = event.target.cloneNode()
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    
    element.setAttribute('download', 'quill-editor-result.html');
    element.setAttribute('class', 'row');
    element.insertAdjacentElement('afterbegin', icon)
    event.target.parentNode.insertAdjacentElement('afterbegin', element)
    event.target.remove()
    element.click();
    notificator.notify('Downloaded successfully','info')
}

function deleteTemplateReq(event, filename){
    var formData = new FormData()
    formData.append('filename', filename)
    formData.append('csrfmiddlewaretoken', csrftoken)
    fetch('delete/', {
        method: 'POST',
        body: formData,
    })
    .then( response => {
        if (!response.ok)
            return response.json().then( response => {
                notificator.notify(response['msg'],'error')        
            })
        else
            return response.json().then( response =>{
                notificator.notify(response['msg'],'success')
                listQuill(event)
            })
    })
    .catch(error => {
        notificator.notify(error,'error')
        console.error('There was a problem with your fetch operation:', error);
    });
}

function uploadTemplateReq(event, filename){
    var formData = new FormData()
    formData.append('filename', filename)
    formData.append('csrfmiddlewaretoken', csrftoken)
    fetch('upload/', {
        method: 'POST',
        body: formData,
    })
    .then( response => {
        if (!response.ok)
            return response.json().then( response => {
                notificator.notify(response['msg'],'error')        
            })
        else
            return response.json().then( response =>{
                // Add link to download button
                var ref = event.target.dataset.ref
                var download_btn = document.querySelector('#download_btn')
                download_btn.setAttribute('href', ref)
                download_btn.setAttribute('download', filename)
                // Insert content on page
                loadQuill( response['content'])
        
                notificator.notify(response['msg'],'success')
            })
    })
    .catch(error => {
        notificator.notify(error,'error')
        console.error('There was a problem with your fetch operation:', error);
    });

    closeModal(document.querySelector('#toListModal'))
}

function onReady(){
    var download_btn_raw = document.querySelector('#download_btn_raw')
    if (download_btn_raw)
        download_btn_raw.addEventListener('click', (ev) => {
            downloadQuill(ev)
        })
}


if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
} else {
    onReady()
}
window.addEventListener('unload', saveQuill)