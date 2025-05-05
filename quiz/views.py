from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Quiz, Question, Answer, QuizAttempt
from .forms import QuizForm, QuestionForm, AnswerFormSet
from courses.models import Course

@login_required
def quiz_create(request, course_id):
    course = get_object_or_404(Course, id=course_id, owner=request.user)
    
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            # Get the last module of the course or create a new one if none exists
            module = course.modules.last()
            if not module:
                module = course.modules.create(title=f"Module 1")
            quiz.module = module
            quiz.save()
            messages.success(request, 'Quiz created successfully!')
            return redirect('quiz:quiz_edit', quiz_id=quiz.id)
    else:
        form = QuizForm()
    
    return render(request, 'quiz/quiz_form.html', {
        'form': form,
        'course': course,
        'title': 'Create Quiz'
    })

@login_required
def quiz_edit(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, module__course__owner=request.user)
    questions = quiz.questions.all().order_by('order')
    
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz updated successfully!')
            return redirect('quiz:quiz_edit', quiz_id=quiz.id)
    else:
        form = QuizForm(instance=quiz)
    
    return render(request, 'quiz/quiz_edit.html', {
        'form': form,
        'quiz': quiz,
        'questions': questions
    })

@login_required
def quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, module__course__owner=request.user)
    
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Quiz deleted successfully!')
        return redirect('quiz:my_quizzes')
    
    return redirect('quiz:my_quizzes')

@login_required
def question_create(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, module__course__owner=request.user)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.order = quiz.questions.count()
            question.save()
            
            # The form's save method will handle creating True/False answers
            form.save()
            
            messages.success(request, 'Question added successfully!')
            return redirect('quiz:quiz_edit', quiz_id=quiz.id)
    else:
        form = QuestionForm()
    
    return render(request, 'quiz/question_form.html', {
        'form': form,
        'quiz': quiz
    })

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    student = request.user
    
    # Check if student is enrolled in the course
    if not student.courses_joined.filter(id=quiz.module.course.id).exists():
        messages.error(request, 'You must be enrolled in the course to take this quiz.')
        return redirect('student_course_detail', quiz.module.course.id)
    
    # Check if student has already completed this quiz
    attempt = QuizAttempt.objects.filter(quiz=quiz, student=student).first()
    if attempt and attempt.completed_at:
        messages.info(request, 'You have already completed this quiz.')
        return redirect('quiz:quiz_results', attempt_id=attempt.id)
    
    if request.method == 'POST':
        score = 0
        total_points = 0
        
        for question in quiz.questions.all():
            total_points += question.points
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                if question.answers.get(id=answer_id).is_correct:
                    score += question.points
        
        if not attempt:
            attempt = QuizAttempt.objects.create(quiz=quiz, student=student)
        
        # Check if there are any questions/points before calculating score
        if total_points > 0:
            attempt.score = (score / total_points) * 100
        else:
            attempt.score = 0
            messages.warning(request, 'This quiz has no questions or all questions have 0 points.')
            
        attempt.completed_at = timezone.now()
        attempt.passed = attempt.score >= quiz.required_score_to_pass
        attempt.save()
        
        return redirect('quiz:quiz_results', attempt_id=attempt.id)
    
    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz,
        'attempt': attempt
    })

@login_required
def question_edit(request, question_id):
    question = get_object_or_404(Question, id=question_id, quiz__module__course__owner=request.user)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            formset = AnswerFormSet(request.POST, instance=question)
            if formset.is_valid():
                answers = formset.save(commit=False)
                for i, answer in enumerate(answers):
                    answer.answer_text = 'True' if i == 0 else 'False'
                    answer.save()
                messages.success(request, 'Question updated successfully!')
                return redirect('quiz:quiz_edit', quiz_id=question.quiz.id)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)
    
    return render(request, 'quiz/question_form.html', {
        'form': form,
        'formset': formset,
        'quiz': question.quiz,
        'question': question
    })

@login_required
def question_delete(request, question_id):
    question = get_object_or_404(Question, id=question_id, quiz__module__course__owner=request.user)
    quiz = question.quiz
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully!')
        return redirect('quiz:quiz_edit', quiz_id=quiz.id)
    
    return redirect('quiz:quiz_edit', quiz_id=quiz.id)

@login_required
def quiz_results(request, attempt_id):
    quiz_attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    
    return render(request, 'quiz/quiz_results.html', {
        'quiz_attempt': quiz_attempt
    })

@login_required
def my_quizzes(request):
    # Get quizzes where the user is the owner (through course ownership) and module still exists
    created_quizzes = Quiz.objects.filter(
        module__course__owner=request.user,
        module__isnull=False  # Only include quizzes with existing modules
    ).select_related('module', 'module__course').order_by('-created')
    
    # Get quiz attempts by the user
    attempted_quizzes = QuizAttempt.objects.filter(
        student=request.user,
        quiz__module__isnull=False  # Only include attempts for quizzes with existing modules
    ).order_by('-completed_at')
    
    return render(request, 'quiz/my_quizzes.html', {
        'created_quizzes': created_quizzes,
        'attempted_quizzes': attempted_quizzes
    }) 