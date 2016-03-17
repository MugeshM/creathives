from rest_framework import serializers
from app.home.models import User,projects
from app.home.jwt_helper import get_json_web_token


class SignupSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(allow_blank=False, write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password', 'user_name',)
        write_only_fields = ('password',)

    def validate(self, data):
        flag=0
        for k, v in data.items():
            if v == '':
                flag=1
                break
        if flag==1:
            raise serializers.ValidationError("Some fields are missing")

        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('get_json_web_token')
    class Meta:
        model = User
        fields = ('token',)

    def get_json_web_token(self, obj):
       return get_json_web_token(obj)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = projects
        fields = ('project_title','project_desc','user_id','posted_date','thumbnail_url','project_url')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('user_name','contact_number','aboutme','profile_url','location','gender')
