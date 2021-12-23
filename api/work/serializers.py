from rest_framework.serializers import ModelSerializer, RelatedField
from work.models import TaskCategory, Expertise


class TaskCategorySerializer(ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = '__all__'

    def to_representation(self, instance):
        instance = super(TaskCategorySerializer, self).to_representation(instance)
        if instance["parent"] is None:
            children = TaskCategory.objects.filter(parent_id=instance["id"], active=True).all()
            instance["children"] = TaskCategorySerializer(children, many=True).data
        del instance["parent"]
        return instance


class ExpertiseSerializer(ModelSerializer):
    class Meta:
        model = Expertise
        fields = '__all__'

    def to_representation(self, instance):
        instance = super(ExpertiseSerializer, self).to_representation(instance)
        if instance["parent"] is None:
            children = Expertise.objects.filter(parent_id=instance["id"]).all()
            instance["children"] = TaskCategorySerializer(children, many=True).data
        del instance["parent"]
        return instance
