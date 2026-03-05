from rest_framework import serializers
from blog.models import Article, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class ArticleSerializer(serializers.ModelSerializer):
    # user = serializers.HyperlinkedRelatedField(view_name="api:user-detail", read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    approver_users = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Article
        fields = ["pk", "name", "text", "user", "date_created","approver_users"]

    def to_representation(self, instance):
        res = super().to_representation(instance)
        return res

class UserDemoRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    motive_text = serializers.CharField(max_length=300)

    def validate_name(self, value):
        if "valera" in value.lower():
            raise serializers.ValidationError("Valera роби роботу, а не грайся в Postman")
        return value

