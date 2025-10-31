from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import DesignRequestForm
from django.shortcuts import render
from .models import DesignRequest
from django.http import HttpResponseForbidden


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            from .models import UserProfile
            UserProfile.objects.create(user=user, full_name=form.cleaned_data['full_name'])
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def create_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.save()
            return redirect('my_requests')
    else:
        form = DesignRequestForm()
    return render(request, 'create_request.html', {'form': form})


@login_required
def my_requests(request):
    status_filter = request.GET.get('status')
    queryset = DesignRequest.objects.filter(user=request.user)

    if status_filter:
        queryset = queryset.filter(status=status_filter)

    queryset = queryset.order_by('-created_at')

    return render(request, 'my_requests.html', {
        'requests': queryset,
        'status_filter': status_filter,
    })


@login_required
def delete_request(request, request_id):
    design_request = get_object_or_404(DesignRequest, id=request_id)

    if design_request.user != request.user or design_request.status != 'new':
        return HttpResponseForbidden("Удаление запрещено.")

    if request.method == 'POST':
        design_request.delete()
        return redirect('my_requests')

    return render(request, 'confirm_delete.html', {'request': design_request})