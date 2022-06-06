from rest_framework.serializers import ModelSerializer


class AdminSerializer(ModelSerializer):
    class Meta:
        model = None
        fields = "__all__"

