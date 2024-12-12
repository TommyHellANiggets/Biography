document.addEventListener('DOMContentLoaded', function() {
    // Настройка TinyMCE для темной темы
    if (typeof tinyMCE !== 'undefined') {
        tinyMCE.init({
            selector: '#id_content',
            skin: 'oxide-dark',
            content_css: 'dark',
            height: 500,
            // Другие настройки TinyMCE...
        });
    }

    // Добавляем подсказку о том, что поле TinyMCE обязательно
    const editorTypeSelect = document.getElementById('id_editor_type');
    const helpText = document.createElement('div');
    helpText.className = 'help';
    helpText.textContent = 'Поле TinyMCE редактора обязательно для заполнения, независимо от выбранного типа редактора.';
    helpText.style.color = '#666';
    editorTypeSelect.parentNode.appendChild(helpText);
}); 