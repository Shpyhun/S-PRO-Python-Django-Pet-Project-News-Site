from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, filters

from accounts.models import User
from news.models import Comment, News, Category


class AddCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        # fields = "__all__"
        fields = ['news', 'text', 'user']
        read_only_fields = ('user',)
        # extra_kwargs = {'user': {'read_only': True}}
    #
    # def validate(self, attrs):
    #     attrs['user'] = self.context['request'].user
    #     return attrs['user']


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('title', 'content', 'time_update')


class NewsDetailSerializer(serializers.ModelSerializer):
    comments = AddCommentSerializer()

    class Meta:
        model = News
        fields = ('title', 'content', 'photo', 'likes', 'comments')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


    # def get_queryset(self):
    #     user = self.request.user
    #     return User.objects.filter(user=user)

    # def get_profile(request):
    #     data = request.data
    #     serializer = UserSerializer(instance=data, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     else:
    #         return Response({'response': 'something went wrong'})
    #
    #     return Response({'response': 'ok'})

    # def validate_email(self, value):
    #     user = self.context['request'].user
    #     if User.objects.exclude(pk=user.pk).filter(email=value).exists():
    #         raise serializers.ValidationError({"email": "This email is already in use."})
    #     return value
    #
    # def update(self, instance, validated_data):
    #     instance.first_name = validated_data['first_name']
    #     instance.last_name = validated_data['last_name']
    #
    #     instance.save()
    #
    #     return instance

    # def validate_username(self, value):
    #     user = self.context['request'].user
    #     if User.objects.exclude(pk=user.pk).filter(username=value).exists():
    #         raise serializers.ValidationError({"username": "This username is already in use."})
    #     return value
