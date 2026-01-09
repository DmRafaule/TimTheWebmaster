// Поле ввода файла для редактирования
const fileInput = document.getElementById('svginput');
// Буфер для хранения изначального изображения
let image_buffer = ""
const animation_layer_id = "smil_svg-animation-editor-layer"
// Редактор анимаций
const editor_space = ace.edit("svg-editor");
editor_space.session.setMode("ace/mode/svg");
// Редактор для просмотра исходного кода изображения
const read_only_space = ace.edit("svg-viewer");
read_only_space.session.setMode("ace/mode/svg");
read_only_space.setReadOnly(true);


function setEditor(initContent){
    document.querySelector('#download-svg').classList.remove('hidden')
    var image_previewer = document.getElementById("image-previewer")
    image_previewer.innerHTML = ""
    // Вставляем контент изображения в страницу
    image_previewer.insertAdjacentHTML('afterbegin', initContent)
    // Неизвестно какие маштабы использует данное изображение, поэтому вмещаем его в контейнер
    image_previewer.querySelector('svg').width.baseVal.valueAsString = "100%"
    image_previewer.querySelector('svg').height.baseVal.valueAsString = "100%"
    // Обновляем буфер здесь, ибо незачем обновлять постоянно ширину и высоту
    image_buffer = image_previewer.querySelector('svg').outerHTML
    read_only_space.setValue(image_buffer);
}

function wrapInEditorIdentifier(content){
    var group = document.createElement('g')
    group.id = animation_layer_id
    group.innerHTML = content
    return group
}

function onChange(delta){
    var svg = document.querySelector("#image-previewer>svg")
    // Обновляем изображение на странице
    svg.outerHTML = image_buffer;
    svg = document.querySelector("#image-previewer>svg")
    // Удаляем старый уровень анимаций, чтобы вставить новый
    var old_animation_layer = document.querySelector(`#image-previewer>svg>#${animation_layer_id}`);
    if (old_animation_layer){
        old_animation_layer.remove();
    }
    svg.insertAdjacentElement('beforeend', wrapInEditorIdentifier(editor_space.session.getValue()));
    // Обновляем редактор для просмотра кода изображения
    read_only_space.setValue(svg.outerHTML);
}

function downloadFile(filename, content, mimeType) {
  // 1. Create a Blob (file-like object) with the content and type
  const blob = new Blob([content], { type: mimeType || 'text/plain' });

  // 2. Create an object URL from the Blob
  const url = URL.createObjectURL(blob);

  // 3. Create a temporary anchor element
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename; // Set the default filename for the downloaded file
  anchor.style.display = 'none'; // Hide the element

  // 4. Append the anchor to the body, click it, and remove it
  document.body.appendChild(anchor);
  anchor.click(); // Trigger the download
  document.body.removeChild(anchor);

  // 5. Revoke the object URL to free up memory
  URL.revokeObjectURL(url);
}

fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            let svg_content = e.target.result; // Контент SVG-изображения
            setEditor(svg_content);
            let animation_layer = document.querySelector(`#image-previewer>svg>#${animation_layer_id}`)
            if (animation_layer){
                animation_layer.remove();
                var content = animation_layer.innerHTML;
                editor_space.setValue(content);
            }
            else{
                editor_space.setValue("");
            }
            editor_space.session.on('change', onChange);
        };

        reader.onerror = function(e) {
            toaster.notify(gettext(`Ошибка чтения файла: ${e.target.error}`), 'error');
            editor_space.setValue(gettext("Ошибка загрузки содержимого файла."));
        };

        reader.readAsText(file)
    }
});

document.querySelector('#download-svg').addEventListener('click', function(e){
    let svg = document.querySelector("#image-previewer>svg")
    downloadFile('result.svg', svg.outerHTML, 'image/svg+xml')
})

function onReady(){
    editor_space.setValue(gettext("Пожалуйста загрузи своё изображение"));
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
} else {
    onReady()
}

// Создаем элемент тултипа
const tooltip = document.createElement('div');
tooltip.id = 'svg-tooltip';
document.body.appendChild(tooltip);

let lastLeafTarget = null;
let currentSelectionIndex = 0;
const imagePreviewer = document.getElementById('image-previewer');

// Функция создания уникального CSS-селектора
function getSelector(el) {
    if (el.id) return `#${el.id}`;
    
    let path = [];
    while (el && el.tagName.toLowerCase() !== 'svg') {
        let index = 1;
        let sibling = el.previousElementSibling;
        while (sibling) {
            if (sibling.tagName === el.tagName) index++;
            sibling = sibling.previousElementSibling;
        }
        let tagName = el.tagName.toLowerCase();
        path.unshift(`${tagName}:nth-of-type(${index})`);
        el = el.parentElement;
    }
    return path.join(' > ');
}

// Функция получения цепочки элементов для тултипа
function getChain(leaf) {
    let chain = [];
    let current = leaf;
    while (current && current.tagName.toLowerCase() !== 'svg') {
        chain.unshift(current);
        current = current.parentElement;
    }
    return chain;
}

// Отображение тултипа при движении мыши
imagePreviewer.addEventListener('mousemove', (e) => {
    const leaf = e.target;
    if (leaf.tagName.toLowerCase() === 'svg' || leaf.id === 'image-previewer') {
        tooltip.style.display = 'none';
        return;
    }

    const chain = getChain(leaf);
    tooltip.style.display = 'block';
    tooltip.style.left = (e.clientX + 15) + 'px';
    tooltip.style.top = (e.clientY + 15) + 'px';

    // Формируем визуальную цепочку тегов
    tooltip.innerHTML = chain.map((el, index) => {
        const isSelected = (leaf === lastLeafTarget && index === currentSelectionIndex);
        return `<span class="${isSelected ? 'tooltip-tag-active' : ''}">${el.tagName.toLowerCase()}</span>`;
    }).join(' > ');
});

imagePreviewer.addEventListener('mouseleave', () => {
    tooltip.style.display = 'none';
});

// Логика клика (Inkscape style + Selector Copy)
imagePreviewer.addEventListener('click', (e) => {
    const leafElement = e.target;
    if (leafElement.tagName.toLowerCase() === 'svg') return;

    const chain = getChain(leafElement);

    if (leafElement === lastLeafTarget) {
        currentSelectionIndex = (currentSelectionIndex + 1) % chain.length;
    } else {
        lastLeafTarget = leafElement;
        currentSelectionIndex = 0;
    }

    const selectedElement = chain[currentSelectionIndex];
    
    // Визуальное выделение
    document.querySelectorAll('.inkscape-selected').forEach(el => el.classList.remove('inkscape-selected'));
    selectedElement.classList.add('inkscape-selected');

    // Получаем ID или Селектор
    const identifier = getSelector(selectedElement);
    
    // Копирование в буфер
    navigator.clipboard.writeText(identifier).then(() => {
        toaster.notify(gettext(`Скопировано: ${identifier}`), 'success');
    });

    e.preventDefault();
});