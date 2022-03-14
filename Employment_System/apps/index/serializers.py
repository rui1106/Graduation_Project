from rest_framework import serializers

from apps.jobs.models import JobInfo


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobInfo
        fields = ["name", 'salary', 'location', 'company', 'degree_required', 'number']
