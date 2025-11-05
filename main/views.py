from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import DesignRequestForm
from .models import DesignRequest
from django.http import HttpResponseForbidden
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ChangeStatusForm



def index(request):
    completed_requests = DesignRequest.objects.filter(
        status='completed'
    ).order_by('-created_at')[:4]

    in_progress_count = DesignRequest.objects.filter(
        status='in_progress'
    ).count()

    return render(request, 'index.html', {
        'completed_requests': completed_requests,
        'in_progress_count': in_progress_count,
    })


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





@staff_member_required
def change_status(request, request_id):
    design_request = get_object_or_404(DesignRequest, id=request_id)

    if design_request.status != 'new':
        return HttpResponseForbidden("Изменение статуса запрещено для этой заявки.")

    if request.method == 'POST':
        form = ChangeStatusForm(request.POST, request.FILES, instance=design_request)
        if form.is_valid():
            form.save()
            return redirect('admin_requests')
    else:
        form = ChangeStatusForm(instance=design_request)

    return render(request, 'change_status.html', {
        'form': form,
        'request_obj': design_request
    })

@staff_member_required
def admin_requests(request):
    status_filter = request.GET.get('status')
    queryset = DesignRequest.objects.all()
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    queryset = queryset.order_by('-created_at')
    return render(request, 'admin_requests.html', {
        'requests': queryset,
        'status_filter': status_filter,
    })