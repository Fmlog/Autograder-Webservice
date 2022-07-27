from .models import User
from rest_framework import serializers

class UserSerializers(serializers.ModelSerializer):
    """ Serializes user data"""
    class Meta:
        """ Meta class for a typical user"""
        model = User
        """Typical user has following attributes:"""
        fields = ('id', 'name', 'email', 'password', 'is_lecturer', 'is_student', 'is_admin')
        extra_kwargs = {
            'password': {'write_only': True},
            'is_lecturer': {'write_only': True},
            'is_student': {'write_only': True},
            'is_admin': {'write_only': True},
        }
    def create (self, validated_data):
        """Creates users"""
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance