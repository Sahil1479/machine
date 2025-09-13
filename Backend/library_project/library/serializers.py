class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id']

    # field-level validation for "title"
    ''' In DRF, you can add field-level validation methods to a serializer.
    The method signature must be:

    def validate_<fieldname>(self, value):
        # custom validation logic
        return value

    So if you have a field named title, DRF will automatically call validate_title during .is_valid().
    '''
    def validate_title(self, value):
        if(len(value) < 5):
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value