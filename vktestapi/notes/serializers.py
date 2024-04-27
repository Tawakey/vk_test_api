from rest_framework import serializers
from .models import Note
from rest_framework.fields import CurrentUserDefault


#Serializers for unauthenticatd users
class NoteSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ["username", "user", "title", "content", "id"]

    def get_username(self, obj):
        return obj.user.username

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


#Serializers for authenticatd users
class AuthenticatedNoteSerializer(NoteSerializer):
    is_owner = serializers.SerializerMethodField()
    

    class Meta:
        model = Note
        fields = ["id", "user", "username", "title", "content",  "is_owner"]

    def get_is_owner(self, obj):
        return self.context["request"] == obj
    
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)