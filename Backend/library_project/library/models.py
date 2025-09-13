class Author(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    published_date = models.DateField()
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return self.title
