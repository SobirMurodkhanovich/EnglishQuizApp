from django.db import models


class Test(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('elementary', 'Elementary'),
        ('pre_intermediate', 'Pre-Intermediate'),
        ('intermediate', 'Intermediate'),
        ('ielts', 'IELTS'),
    ]

    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.level} Test"


class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_option = models.PositiveIntegerField()

    def __str__(self):
        return self.question_text
