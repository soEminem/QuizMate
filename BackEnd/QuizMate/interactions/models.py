from django.contrib.auth.models import AbstractUser
from django.db import models

# User model (esteso per futura flessibilità)
class User(AbstractUser):
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# Documento caricato dall'utente
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    extracted_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Quiz generato da un documento
class Quiz(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='quizzes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_retake = models.BooleanField(default=False)
    original_quiz = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='retakes')

    def __str__(self):
        return f"Quiz {self.id} - {self.document.title}"

# Domande generate per un quiz
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    options = models.JSONField()
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"Question {self.id} - Quiz {self.quiz.id}"

# Risposta data dall'utente a una domanda
class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    selected_option = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user.username} to Question {self.question.id}"
