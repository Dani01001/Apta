from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Perfil


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ["telefono", "foto_url"]


class UsuarioSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "perfil"]

    def update(self, instance, validated_data):
        perfil_data = validated_data.pop("perfil", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if perfil_data:
            Perfil.objects.update_or_create(usuario=instance, defaults=perfil_data)
        return instance


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    telefono = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password", "telefono"]

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Ese nombre de usuario ya está en uso.")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Ese correo ya está registrado.")
        return value

    def create(self, validated_data):
        telefono = validated_data.pop("telefono", "")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Perfil.objects.create(usuario=user, telefono=telefono)
        return user
