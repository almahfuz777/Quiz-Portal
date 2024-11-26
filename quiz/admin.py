from django.contrib import admin
from .models import Quiz, Question, QuizStats

# register models
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuizStats)
