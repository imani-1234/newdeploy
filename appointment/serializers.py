from rest_framework import serializers
from .models import User, Doctor, Patient, Appointment
from django.contrib.auth import authenticate
from .models import User, Doctor, Patient
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_doctor', 'is_patient']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['is_doctor'] and data['is_patient']:
            raise serializers.ValidationError("A user cannot be both a doctor and a patient.")
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        if user.is_doctor:
            Doctor.objects.create(user=user)
        elif user.is_patient:
            Patient.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            print(f"Attempting to authenticate user: {username}")  # Debug print
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                data['user'] = user
            else:
                print("Authentication failed")  # Debug print
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        return data

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
