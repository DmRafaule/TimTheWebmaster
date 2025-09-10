    const fileInput = document.getElementById('uploaded_file');

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = function(e) {
                const fileContent = e.target.result; // The content of the file
                let editor = document.querySelector('#editor>.ql-editor')
                editor.innerHTML = ""
                editor.insertAdjacentHTML('afterbegin', fileContent)
            };

            reader.onerror = function(e) {
                toaster.notify(`Error reading file: ${e.target.error}`, 'error');
            };

            reader.readAsText(file)
        }
    });