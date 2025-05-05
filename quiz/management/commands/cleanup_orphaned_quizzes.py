from django.core.management.base import BaseCommand
from quiz.models import Quiz

class Command(BaseCommand):
    help = 'Clean up quizzes that have no associated module (orphaned quizzes)'

    def handle(self, *args, **kwargs):
        # Get all quizzes with null modules
        orphaned_quizzes = Quiz.objects.filter(module__isnull=True)
        count = orphaned_quizzes.count()
        
        if count > 0:
            # Delete the orphaned quizzes
            orphaned_quizzes.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {count} orphaned quiz(es)')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('No orphaned quizzes found')
            ) 