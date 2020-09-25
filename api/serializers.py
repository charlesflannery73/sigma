from rest_framework import serializers

from web.models import Type, Signature


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class SigSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signature
        fields = '__all__'


class SigDetailSerializer(serializers.ModelSerializer):
    type = TypeSerializer()

    class Meta:
        model = Signature
        fields = '__all__'
