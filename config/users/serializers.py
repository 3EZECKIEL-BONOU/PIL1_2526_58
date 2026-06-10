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
            'email',
            'nom',
            'prenom',
            'telephone',
            'is_mentor',
            'is_mentee',
            'filiere',
            'niveau_etudes',
            'bio',
            'password',
            'password2',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        email = validated_data.get('email', '')
        base = email.split('@')[0].lower().replace('.', '_').replace('+', '')
        username = base
        counter = 1
        while Utilisateur.objects.filter(username=username).exists():
            username = f"{base}{counter}"
            counter += 1
        validated_data['username'] = username
        return Utilisateur.objects.create_user(**validated_data)


class ProfilSerializer(serializers.ModelSerializer):

    roles = serializers.SerializerMethodField()

    class Meta:
        model = Utilisateur

        fields = [
            'id',
            'username',
            'email',
            'nom',
            'prenom',
            'telephone',
            'is_mentor',
            'is_mentee',
            'roles',
            'filiere',
            'niveau_etudes',
            'bio',
            'photo_profil',
            'date_inscription'
        ]
        read_only_fields = ['roles']

    def get_roles(self, obj):
        """Retourne la liste des rôles de l'utilisateur"""
        return obj.get_roles_list()


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
