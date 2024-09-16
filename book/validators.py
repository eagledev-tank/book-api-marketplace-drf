from rest_framework import serializers


def description_validator(description):
    if len(description) > 50:
        raise serializers.ValidationError('Description must be less than 50 characters')
    return description
