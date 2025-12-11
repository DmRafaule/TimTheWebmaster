import Quill from './quill-engine.js'

function createIcon(path){
  let icon = document.createElement('img')
  icon.setAttribute('width', 16)
  icon.setAttribute('height', 16)
  icon.setAttribute('src', path)
  return icon;
}

const BlockEmbed = Quill.import('blots/block/embed');

class CodeBlockFormat extends BlockEmbed {
    constructor(scroll, node){
        super(scroll, node);
        node.addEventListener('dblclick', () => {
            CodeBlockFormat.openModal(node);
        });

        if (window.microlight) {
            microlight.reset && microlight.reset();
        }
    }

    static setHeight(node, code){
        const LINES = code.split('\n').length
        const MODIFIER = 15
        const INIT_HEIGHT = 100
        node.style.height = `${LINES*MODIFIER + INIT_HEIGHT}px`
    }

    static create(value) {
        const node = super.create();

        // Legend
        const legend = document.createElement('legend');
        legend.classList.add('code')
        legend.classList.add('padder')
        const legend_icon = createIcon(`${PATH}Post/img/blockCode.svg`)
        const separator = document.createElement('div')
        separator.classList.add("code-block-legend_separator")
        const copy_icon_container = `
            <div id="code-block-copy-button" class="ttw-button_action"><img width="16" height="16" src="${PATH}Post/img/copy.svg"
                onclick="
                    var text = this.parentElement.parentElement.parentElement.querySelector('.microlight').textContent ;
                    navigator.clipboard.writeText(text); toaster.notify('${gettext("Скопированно")}','success');
                "
            ></div>
        `
    
        legend.insertAdjacentElement('beforeend', legend_icon)
        legend.insertAdjacentElement('beforeend', separator)
        legend.insertAdjacentHTML('beforeend', copy_icon_container)

        // Code container
        const codeDiv = document.createElement('div');
        codeDiv.classList.add('microlight');
        codeDiv.textContent = value.code || '';
        this.setHeight(node, codeDiv.textContent)

        node.appendChild(legend);
        node.appendChild(codeDiv);

        // Double‑click to edit
        node.addEventListener('dblclick', () => {
            CodeBlockFormat.openModal(node);
        });

        return node;
    }

    static value(node) {
        return {
        icon: node.querySelector('legend')?.textContent || '',
        code: node.querySelector('.microlight')?.textContent || ''
        };
    }

    // Modal editor
    static openModal(node) {

        const modal_content = `
        <div><b>${gettext('Редактор кода')}</b></div>
        <hr>
        <textarea class="quilljs-textarea">${node.querySelector('.microlight').textContent}</textarea>
        <hr>
        <div class="flex flex-row justify-between flex-wrap">
            <div id="save_code" class="ttw-button ttw-button_action">
                <p class="rounded-lg bg-main border text-white p-2">${gettext('Сохранить')}</p>
            </div>
            <div class="ttw-button ttw-button_action" onclick="modal.close();window.modal.modal_window.classList.remove('code-editor-width')">
                <p class="rounded-lg bg-main border text-white p-2">${gettext('Отмена')}</p>
            </div>
        </div>
        `;
        window.modal.modal_window.classList.add('code-editor-width')
        window.modal.open(modal_content)

        window.modal.container.querySelector('#save_code').onclick = () => {
            const newCode = window.modal.container.querySelector('textarea').value;
            node.querySelector('.microlight').textContent = newCode;
            this.setHeight(node, newCode)
            window.modal.close();
            if (window.microlight) {
                microlight.reset && microlight.reset();
            }
            window.modal.modal_window.classList.remove('code-editor-width')
        };
    }
}

CodeBlockFormat.blotName = 'code-block';
CodeBlockFormat.tagName = 'fieldset';
CodeBlockFormat.className = 'ql-code-block-container';

Quill.register({"formats/code-block": CodeBlockFormat});

export function CodeBlockHandler(code = "// Your code goes here", icon = '💻') {
    const range = quill.getSelection();

    quill.insertEmbed(range.index, 'code-block', { code, icon }, Quill.sources.USER);
    quill.setSelection(range.index + 1, Quill.sources.SILENT);

    if (window.microlight) {
        microlight.reset && microlight.reset();
    }
}
