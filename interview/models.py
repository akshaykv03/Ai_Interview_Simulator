from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

phone_validator = RegexValidator(
    regex = r'^[6789]\d{9}$',
    message = "phone number must be 10 digits and starts with 6/7/8/9"
)

class CustomUser(AbstractUser):
    USER_TYPE = (
        ('User', 'User'),
        ('Admin', 'Admin'),
    )

    userType = models.CharField(
        max_length=20,
        choices= USER_TYPE,
        default='User'
        )
    
    date_joined = models.DateTimeField(auto_now_add=True)


class User_tbl(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=10,
        unique=True,
        validators=[phone_validator]
        )
    image = models.ImageField(
        upload_to='profile_images/'
    )
    address = models.TextField()

    def __str__(self):
        return self.name
    


class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    question = models.TextField()

    correct_answer = models.TextField()

    marks = models.IntegerField(default=10)



class UserAnswer(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    answer = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    similarity_score = models.FloatField(
        default=0
    )
    
    obtained_marks = models.FloatField(
        default=0
    )

    def __str__(self):

        return self.user.username


class CheatingLog(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    issue = models.CharField(
        max_length=200
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.issue

class InterviewRequest(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.user.username


class InterviewResult(models.Model):

    STATUS_CHOICES = (

        ('Completed', 'Completed'),

        ('Malpractice', 'Malpractice'),

        ('Pending', 'Pending')
    )

    user = models.ForeignKey(

        CustomUser,

        on_delete=models.CASCADE
    )

    category = models.ForeignKey(

        Category,

        on_delete=models.CASCADE
    )

    total_marks = models.FloatField(
        default=0
    )

    obtained_marks = models.FloatField(
        default=0
    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.user.username