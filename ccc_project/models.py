from django.db import models
import uuid
from django.utils import timezone

class User_Info(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False )
    name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True) 
    telegram_chat_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name} ({self.phone_number})"
 
class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('quality', 'Quality'),
        ('delivery', 'Delivery'),
        ('merchandising', 'Merchandising'),
        ('payment settlement', 'Payment Settlement'),
        ('resources trade tools', 'Resources Trade Tools'),
        ('competitors', 'Competitors'),
        ('salesman', 'Salesman'),
    ] 

    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User_Info, on_delete=models.CASCADE, related_name='feedback_details')
    feedback_type = models.CharField(max_length=50, choices=FEEDBACK_TYPES)
    description = models.TextField()
    voice_feedback = models.FileField(upload_to='feedback/voice/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_valid = models.BooleanField(null=True, blank=True)
    executive_approval = models.BooleanField(null=True, blank=True)
    date_of_issue = models.DateField()
    problem_statement = models.TextField()
    fact_check = models.TextField()
    root_cause_analysis = models.TextField()
    corrective_action = models.TextField()
    preventive_action = models.TextField()
    proposals_remarks = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_feedback_type_display()} - {self.user}"
    

class Photo(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='feedback/photos/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Photo for {self.feedback}"

class SolutionFile(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='solution_files')
    solution_file = models.FileField(upload_to='feedback/solutions/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Solution for {self.feedback}"
    

