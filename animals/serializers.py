from rest_framework import status, serializers

from animals.models import Animal

from characteristics.models import Characteristic
from characteristics.serializers import CharacterSerializer

from groups.models import Group
from groups.serializers import GroupSerializer

class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.FloatField()
    weight = serializers.FloatField()
    sex = serializers.CharField(max_length=15)

    group = GroupSerializer()
    characteristics = CharacterSerializer(many=True)


    def create(self, validated_data):
        group = validated_data.pop('group')
        characteristics = validated_data.pop('characteristics')

        group, _= Group.objects.get_or_create(group, pk=group)

        animal = Animal.objects.create(**validated_data, group=group)

        for character in characteristics:
            character:_ =Characteristic.objects.get_or_create(**character)
            animal.characteristics.add(character)

        return animal

    def update(self, instance: Animal, validated_data: dict):
        not_allowed = {'sex','group'}

        for key, value in validated_data.items():
            if key in not_allowed:
                raise KeyError(
                    {"message":f'You can not update {key} property'},
                    status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            if key == 'characteristics':
                characteristics = []
                for char in key:
                    char, _= Characteristic.objects.get_or_create(**char)
                    characteristics.set(char)
                instance.characteristics.set(characteristics)
            else:
                setattr(instance, key, value)
                instance.save()
        return instance