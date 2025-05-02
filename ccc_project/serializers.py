from rest_framework import serializers
from .models import User_Info , Feedback, Photo, SolutionFile
from django.core.files.base import ContentFile
import requests
from urllib.parse import urlparse

class PhotoSerializer(serializers.ModelSerializer):
    photo = serializers.URLField()  # Accept URL instead of file upload

    class Meta:
        model = Photo
        fields = ['photo', 'uploaded_at']
        read_only_fields = ['uploaded_at']

    def create(self, validated_data):
        photo_url = validated_data.pop('photo')
        # Download the file from the URL
        response = requests.get(photo_url)
        if response.status_code != 200:
            raise serializers.ValidationError(f"Failed to download photo from {photo_url}")
        
        # Extract filename from URL
        filename = urlparse(photo_url).path.split('/')[-1]
        # Create a ContentFile from the downloaded content
        photo_file = ContentFile(response.content, name=filename)
        return Photo.objects.create(photo=photo_file, **validated_data)
    
    def update(self, instance, validated_data):
        photo_url = validated_data.get('photo', instance.photo.url)
        if photo_url != instance.photo.url:
            response = requests.get(photo_url)
            if response.status_code != 200:
                raise serializers.ValidationError(f"Failed to download photo from {photo_url}")
            filename = urlparse(photo_url).path.split('/')[-1]
            photo_file = ContentFile(response.content, name=filename)
            instance.photo = photo_file
        instance.save()
        return instance
    
class SolutionFileSerializer(serializers.ModelSerializer):
    solution_file = serializers.URLField()  # Accept URL instead of file upload

    class Meta:
        model = SolutionFile
        fields = ['solution_file', 'uploaded_at']
        read_only_fields = ['uploaded_at']

    def create(self, validated_data):
        solution_file_url = validated_data.pop('solution_file')
        # Download the file from the URL
        response = requests.get(solution_file_url)
        if response.status_code != 200:
            raise serializers.ValidationError(f"Failed to download solution file from {solution_file_url}")
        
        # Extract filename from URL
        filename = urlparse(solution_file_url).path.split('/')[-1]
        # Create a ContentFile from the downloaded content
        solution_file = ContentFile(response.content, name=filename)
        return SolutionFile.objects.create(solution_file=solution_file, **validated_data)
    
    def update(self, instance, validated_data):
        solution_file_url = validated_data.get('solution_file', instance.solution_file.url)
        if solution_file_url != instance.solution_file.url:
            response = requests.get(solution_file_url)
            if response.status_code != 200:
                raise serializers.ValidationError(f"Failed to download solution file from {solution_file_url}")
            filename = urlparse(solution_file_url).path.split('/')[-1]
            solution_file = ContentFile(response.content, name=filename)
            instance.solution_file = solution_file
        instance.save()
        return instance

    
class FeedbackSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, required=False)
    solution_files = SolutionFileSerializer(many=True, required=False)
    voice_feedback = serializers.URLField(required=False, allow_null=True)  # Accept URL for voice feedback

    class Meta:
        model = Feedback
        fields = [
            'feedback_type', 'description', 'voice_feedback', 'photos', 'solution_files',
            'status', 'is_valid', 'executive_approval', 'date_of_issue',
            'problem_statement', 'fact_check', 'root_cause_analysis',
            'corrective_action', 'preventive_action', 'proposals_remarks',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def update(self, instance, validated_data):
        photos_data = validated_data.pop('photos', None)
        solution_files_data = validated_data.pop('solution_files', None)
        voice_feedback_url = validated_data.pop('voice_feedback', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if voice_feedback_url is not None:
            if voice_feedback_url:
                response = requests.get(voice_feedback_url)
                if response.status_code == 200:
                    filename = urlparse(voice_feedback_url).path.split('/')[-1]
                    voice_file = ContentFile(response.content, name=filename)
                    instance.voice_feedback = voice_file
                else:
                    raise serializers.ValidationError(f"Failed to download voice feedback from {voice_feedback_url}")
            else:
                instance.voice_feedback = None
            instance.save()
        if photos_data is not None:
            instance.photos.all().delete()
            for photo_data in photos_data:
                PhotoSerializer().create({**photo_data, 'feedback': instance})
        if solution_files_data is not None:
            instance.solution_files.all().delete()
            for solution_file_data in solution_files_data:
                SolutionFileSerializer().create({**solution_file_data, 'feedback': instance})
        return instance
    

class User_InfoSerializer(serializers.ModelSerializer):
    feedback_details = FeedbackSerializer(many=True, required=False)

    class Meta:
        model = User_Info
        fields = [
           'id' ,'uuid', 'name', 'phone_number', 'address', 'telegram_chat_id',
            'created_at', 'updated_at', 'feedback_details'
        ]
        read_only_fields = ['uuid', 'created_at', 'updated_at']

    def create(self, validated_data):
        feedback_details_data = validated_data.pop('feedback_details', [])
        user_info = User_Info.objects.create(**validated_data)

        # Create Feedback instances
        for feedback_data in feedback_details_data:
            feedback_data['user'] = user_info
            FeedbackSerializer().create(feedback_data)

        return user_info
    
    def update(self, instance, validated_data):
        feedback_details_data = validated_data.pop('feedback_details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if feedback_details_data is not None:
            for feedback_data in feedback_details_data:
                feedback_type = feedback_data.get('feedback_type')
                try:
                    feedback_instance = instance.feedback_details.get(feedback_type=feedback_type)
                    feedback_serializer = FeedbackSerializer(
                        instance=feedback_instance,
                        data=feedback_data,
                        context={'user': instance},
                        partial=True
                    )
                except Feedback.DoesNotExist:
                    feedback_serializer = FeedbackSerializer(
                        data=feedback_data,
                        context={'user': instance}
                    )
                if feedback_serializer.is_valid():
                    feedback_serializer.save()
                else:
                    raise serializers.ValidationError(feedback_serializer.errors)
        return instance