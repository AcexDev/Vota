from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Answer, Question, Options
from django.http import HttpResponse
from django.views.generic import DetailView, CreateView, DeleteView, FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from.forms import PollCreateForm, QuestionFormSet, OptionFormSet
from django.db.models import Sum
from django.db import transaction
# Create your views here.
def homepage(request):
    poll_set = Poll.objects.all()
    polls = []
    for poll in poll_set:
        poll.question_count = poll.question_set.count()
        polls.append(poll)


    context = {
        'polls': polls,
    }

    return render(request, 'poll/home.html', context)

class PollDetailView(LoginRequiredMixin, DetailView):
    model = Poll
    template_name = 'poll/poll_detail.html'
    context_object_name = 'poll'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = self.object
        has_voted = Answer.objects.filter(poll=poll, voter=self.request.user).exists()
        question_obj = Question.objects.filter(poll=poll)

        questions_data = []
        for question in question_obj:
            option_obj = Options.objects.filter(question=question)
            total = option_obj.aggregate(total=Sum('vote_count'))['total'] or 0
            options_with_pct = [
                {
                    'option': opt,
                    'percent': round(opt.vote_count / total * 100) if total > 0 else 0
                }
                for opt in option_obj
            ]
            questions_data.append({
                'question': question,
                'options': options_with_pct,
                'total': total,
            })

        context['has_voted'] = has_voted
        context['questions_data'] = questions_data
        return context  

class PollCreateView(LoginRequiredMixin, CreateView):
    model         = Poll
    form_class    = PollCreateForm
    template_name = 'poll/create_poll_mcq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post    = self.request.POST or None
        total_q = int(post.get('questions-TOTAL_FORMS', 1)) if post else 1

        context['question_formset'] = kwargs.get('question_formset') or \
            QuestionFormSet(post, prefix='questions')

        # Only build fresh formsets on GET — POST always passes them explicitly
        context['option_formsets'] = kwargs.get('option_formsets') or (
            [] if post else
            [OptionFormSet(prefix=f'options-q{i}') for i in range(total_q)]
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form             = self.get_form()
        post             = request.POST
        total_q          = int(post.get('questions-TOTAL_FORMS', 1))

        question_formset = QuestionFormSet(post, prefix='questions')
        option_formsets  = [
            OptionFormSet(post, prefix=f'options-q{i}')
            for i in range(total_q)
        ]

        form_valid      = form.is_valid()
        questions_valid = question_formset.is_valid()
        options_valid   = all(fs.is_valid() for fs in option_formsets)

        if form_valid and questions_valid and options_valid:
            return self.form_valid(form, question_formset, option_formsets)

        return self.render_to_response(
            self.get_context_data(
                form=form,
                question_formset=question_formset,
                option_formsets=option_formsets,
            )
        )

    def form_valid(self, form, question_formset, option_formsets):
        with transaction.atomic():
            poll         = form.save(commit=False)
            poll.creator = self.request.user
            poll.save()

            question_formset.instance = poll
            questions = question_formset.save(commit=False)

            for obj in question_formset.deleted_objects:
                obj.delete()

            # Build a clean list of (question, option_formset) pairs upfront
            pairs = [
                (i, q_form) for i, q_form in enumerate(question_formset.forms)
                if q_form not in question_formset.deleted_forms
                and not q_form.cleaned_data.get('DELETE', False)
                and q_form.cleaned_data.get('text')
            ]

            for question, (i, _) in zip(questions, pairs):
                question.poll = poll
                question.type = 'MCQ'
                question.save()

                option_fs          = option_formsets[i]
                option_fs.instance = question
                option_fs.save()

        messages.success(self.request, 'Poll Successfully Created')
        return redirect(reverse_lazy('homepage'))

class PollDeleteView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
    model = Poll
    # template_name = "poll/poll_delete.html"

    def test_func(self):
        poll = self.get_object()
        if self.request.user == poll.creator:
            return True
        return False
    
    def get_success_url(self):
        messages.success(self.request, "Poll Successfully Deleted")
        return reverse_lazy('homepage')

@login_required
def poll_type_select(request):
    if request.method == 'POST':
        poll_type = request.POST.get('poll_type')
        if poll_type == 'mcq':
            return redirect('poll-create-mcq')
        elif poll_type == 'text':
            return redirect('poll-create-text')
    return render(request, 'poll/poll_type_select.html')

def create_text_poll(request):
    return render(request, 'poll/create_poll_text.html')

def create_mcq_poll(request):


    return render(request, 'poll/create_poll_mcq.html')
    
@login_required
def add_vote(request, pk):
    user = request.user
    poll_obj = get_object_or_404(Poll, pk=pk)
    has_voted = Answer.objects.filter(poll=poll_obj, voter=user).exists()
    questions = Question.objects.filter(poll=poll_obj)
    if has_voted:
        messages.error(request, "Already Voted")
        return redirect(request.META.get("HTTP_REFERER", "/"))
    
    for question in questions:
        choice_id = request.POST.get(f'choice_{question.id}')
        if not choice_id:
            return("No Choice Seleceted")        
        option_obj = Options.objects.get(id=choice_id)

        Answer.objects.create(
            poll=poll_obj,
            question=question,
            voter=user,
            selected_option=option_obj,
            text_answer=None,
        )

        option_obj.vote_count += 1
        option_obj.save()

        poll_obj.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def user_polls(request):
    active_user = request.user
    polls = Poll.objects.filter(
        creator=active_user
    )

    context = {
        "polls": polls
    }

    return render(request, "poll/user_polls.html", context)

