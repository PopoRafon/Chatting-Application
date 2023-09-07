from rest_framework import serializers
from main.models import Profile
from chat.models import ChatMessage, Chat, Request
from django.contrib.auth.models import User


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = ['email', 'username', 'alias', 'avatar', 'description']

    def update(self, instance, validated_data):
        email = validated_data.pop('email', None)
        username = validated_data.pop('username', None)

        if email is not None:
            instance.user.email = email
            instance.user.save()
        if username is not None:
            instance.user.username = username
            instance.user.save()

        return super().update(instance, validated_data)
        
    def validate(self, data):
        username = data['username']
        email = data['email']
        check_username_in_db = User.objects.filter(username=username).first()
        check_email_in_db = User.objects.filter(email=email).first()
        context = self.context['request']

        if email is not None and len(email) <= 8 and len(email) >= 60:
            raise serializers.ValidationError({'Email': 'Email address need to be between 8-60 characters.'})
        
        if username is not None and len(username) <= 4 and len(username) >= 16:
            raise serializers.ValidationError({'Username': 'Username address need to be between 4-16 characters.'})
        
        if check_username_in_db and check_username_in_db != context.user:
            raise serializers.ValidationError({'Username': 'Username adress already exist.'})
        
        if check_email_in_db and check_email_in_db != context.user:
            raise serializers.ValidationError({'Email': 'Email adress already exist.'})
        
        return data


class UserRetrieveSerializer(serializers.ModelSerializer):
    identifier = serializers.IntegerField(source='user.id')

    class Meta:
        model = Profile
        fields = ['identifier', 'alias', 'avatar', 'description']


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
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['receiver']
