class Article(models.Model):
    # существующие поля...
    editor_type = models.CharField(
        max_length=20,
        choices=[('tinymce', 'TinyMCE'), ('simplemde', 'SimpleMDE')],
        null=True,
        blank=True
    )
    # остальные поля... 