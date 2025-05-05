from django.core.management.base import BaseCommand
from quiz.models import Quiz
from courses.models import Course, Module
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Fix quiz relationships with modules and courses'

    def handle(self, *args, **kwargs):
        # Get the quiz
        try:
            quiz = Quiz.objects.get(id=9)
            self.stdout.write(f'Found quiz: {quiz.title}')
            
            # Get the first available course
            course = Course.objects.first()
            if not course:
                self.stdout.write(self.style.ERROR('No courses found'))
                return
                
            self.stdout.write(f'Found course: {course.title}')
            
            # Get or create a module
            module = course.modules.first()
            if not module:
                module = course.modules.create(title="Module 1")
                self.stdout.write('Created new module: Module 1')
            else:
                self.stdout.write(f'Found existing module: {module.title}')
            
            # Assign the module to the quiz
            quiz.module = module
            quiz.save()
            
            self.stdout.write(self.style.SUCCESS(f'Successfully fixed relationships for quiz {quiz.id}'))
            self.stdout.write(f'Quiz is now in module {module.title} of course {course.title}')
            
        except Quiz.DoesNotExist:
            self.stdout.write(self.style.ERROR('Quiz with ID 9 not found')) 