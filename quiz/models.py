from django.db import models
from django.contrib.auth.models import User
from courses.models import Module
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.template import RequestContext

class Quiz(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='quizzes', null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    time_limit = models.IntegerField(help_text='Time limit in minutes')
    required_score_to_pass = models.IntegerField(help_text='Required score in %')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return f"{self.title}"

    def get_questions(self):
        return self.questions.all()

    def get_user_attempt(self):
        """Get the quiz attempt for the current user."""
        context = RequestContext.current()
        if context:
            user = context.request.user
            try:
                return self.attempts.get(student=user)
            except QuizAttempt.DoesNotExist:
                return None
        return None

    def has_user_attempt(self, user):
        """Check if a user has attempted this quiz."""
        return self.attempts.filter(student=user).exists()

class Question(models.Model):
    TYPES = (
        ('true-false', 'True/False'),
    )
    
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=TYPES, default='true-false')
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.question_text[:50]}..."

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.answer_text} - {'Correct' if self.is_correct else 'Incorrect'}"

class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='attempts', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='quiz_attempts', on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    passed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['quiz', 'student']

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} - {self.score}%" 