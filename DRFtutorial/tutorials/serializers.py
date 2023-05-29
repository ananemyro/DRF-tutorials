from rest_framework import serializers
from .models import Tutorial, Teacher, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'level')


class TeacherSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True, required=False)

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name', 'skills')

    def create(self, validated_data):
        skills_data = validated_data.pop('skills', [])
        teacher = Teacher.objects.create(**validated_data)
        for skill in skills_data:
            teacher.skills.add(skill)
        return teacher


class TeacherPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name')


class TutorialSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), required=False)
    class Meta:
        model = Tutorial
        fields = ('id', 'title', 'description', 'published', 'teacher')

    def create(self, validated_data):
        teacher_id = validated_data.pop('teacher').id
        teacher = Teacher.objects.get(id=teacher_id)
        tutorial = Tutorial.objects.create(teacher=teacher, **validated_data)
        return tutorial
