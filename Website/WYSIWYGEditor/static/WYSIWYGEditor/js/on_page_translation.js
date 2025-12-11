
var sourceLng = language_code;
var targetLng = "";
if (sourceLng === "en")
    targetLng = "ru"
else
    targetLng = "en"

const fetchTranslator = async function() { // Анонимная async-функция
    const translator = await Translator.create({
        sourceLanguage: sourceLng,
        targetLanguage: targetLng,
    });

    return translator;
};

const fetchTranslation = async function(translator, text){
    return await translator.translate(text);
}


/**
 * Проходит по всем текстовым узлам и собирает промисы перевода.
 * @param {HTMLElement} element - Элемент, внутри которого ищем текст.
 * @param {object} translator - Объект переводчика.
 * @returns {Array<{node: Node, promise: Promise<string>}>} Массив задач.
 */
function collectTranslationPromises(element, translator) {
    const translationTasks = [];
    
    // Используем TreeWalker для поиска только текстовых узлов (NodeFilter.SHOW_TEXT)
    const walker = document.createTreeWalker(
        element,
        NodeFilter.SHOW_TEXT,
        null, 
        false
    );

    let node;
    while (node = walker.nextNode()) {
        const textContent = node.nodeValue;
        
        if (textContent.trim().length > 0) {
            translationTasks.push({
                node: node, // Ссылка на узел, который нужно обновить
                // Запускаем асинхронную операцию перевода, но не ждем ее
                promise: fetchTranslation(translator, textContent) 
            });
        }
    }
    return translationTasks;
}

const translateBtn = document.querySelector('#translate-file')
translateBtn.addEventListener('click', async (event) => {
    try {
        const translator = await fetchTranslator();
        let editor = document.querySelector('.ql-editor');
        
        let allTranslationTasks = [];
        window.modalLoader.startLoad();
        // 1. СБОР ПРОМИСОВ (ЗАПУСК ПАРАЛЛЕЛЬНОГО ПЕРЕВОДА)
        // Проходим по верхнеуровневым элементам и собираем все задачи
        for (let i = 0; i < editor.children.length; i++) {
            const currentElement = editor.children[i];
            
            const elementTasks = collectTranslationPromises(currentElement, translator);
            // Добавляем задачи текущего элемента в общий массив
            allTranslationTasks.push(...elementTasks); 
        }

        // Если нет текста для перевода, выходим
        if (allTranslationTasks.length === 0) {
            window.toaster.notify(gettext('Нет текста для перевода'), 'info');
            return;
        }

        // Отделяем массив промисов от массива узлов
        const nodesToUpdate = allTranslationTasks.map(task => task.node);
        const promises = allTranslationTasks.map(task => task.promise);
        
        // 2. ОЖИДАНИЕ ВСЕХ РЕЗУЛЬТАТОВ
        // Promise.all ждет, пока ВСЕ промисы в массиве будут выполнены
        const translatedTexts = await Promise.all(promises);
        window.toaster.notify(gettext('Перевод страницы завершён.'), 'info', 14);
        window.toaster.notify(gettext('Начинаю вставлять переведённый текст.'), 'warning', 14);
        // 3. ОБНОВЛЕНИЕ DOM (Единая пакетная операция)
        // Обновляем все текстовые узлы сразу, как только все переводы готовы
        translatedTexts.forEach((text, index) => {
            nodesToUpdate[index].nodeValue = text;
        });
        window.modalLoader.stopLoad();
        window.toaster.notify(gettext('Страница обновлена.'), 'success', 14);

    } catch (error) {
        // Если хотя бы один промис в Promise.all отклонится, он немедленно перейдет сюда
        window.toaster.notify(gettext('Один из блоков не удалось перевести'), 'warning');
    }
});