from rest_framework import serializers
from main.models import Profile
from chat.models import ChatMessage, Chat


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'alias', 'avatar', 'description']


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.profile.alias', read_only=True)
    avatar = serializers.ImageField(source='sender.profile.avatar', read_only=True)
    created = serializers.SerializerMethodField()
    modified = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'avatar', 'body', 'created', 'modified']

    def get_created(self, obj):
        return obj.created.strftime("%Y-%m-%d %H:%M")

    def get_modified(self, obj):
        return obj.modified.strftime("%Y-%m-%d %H:%M")


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
