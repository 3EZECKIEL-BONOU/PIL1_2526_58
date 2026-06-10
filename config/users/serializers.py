from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

Utilisateur = get_user_model()


class InscriptionSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur

        fields = [
            'username',
            'email',
            'nom',
            'prenom',
            'telephone',
            'role',
            'filiere',
            'niveau_etudes',
            'bio',
            'password',
            'password2'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return Utilisateur.objects.create_user(**validated_data)


class ProfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Utilisateur

        fields = [
            'id',
            'username',
            'email',
            'nom',
            'prenom',
            'telephone',
            'role',
            'filiere',
            'niveau_etudes',
            'bio',
            'photo_profil',
            'date_inscription'
        ]


class ModifierMotDePasseSerializer(serializers.Serializer):

    ancien_password = serializers.CharField(write_only=True)
    nouveau_password = serializers.CharField(write_only=True, validators=[validate_password])
    nouveau_password2 = serializers.CharField(write_only=True)

    def validate_ancien_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")
        return value

    def validate(self, attrs):
        if attrs['nouveau_password'] != attrs['nouveau_password2']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['nouveau_password'])
        user.save()
        return user