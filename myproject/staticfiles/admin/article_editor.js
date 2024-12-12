document.addEventListener('DOMContentLoaded', function () {
    const contentMode = document.querySelectorAll('input[name="content_mode"]');
    const textarea = document.querySelector('#id_content');
    const tinymceArea = textarea.parentElement;
    let markdownEditor;

    contentMode.forEach(mode => {
        mode.addEventListener('change', function () {
            if (this.value === 'markdown') {
                if (!markdownEditor) {
                    markdownEditor = new SimpleMDE({ element: textarea });
                }
                markdownEditor.toTextArea();
                markdownEditor = new SimpleMDE({ element: textarea });
                tinymceArea.style.display = 'none';
            } else if (this.value === 'tinymce') {
                if (markdownEditor) {
                    markdownEditor.toTextArea();
                    markdownEditor = null;
                }
                tinymceArea.style.display = 'block';
            }
        });
    });
});
