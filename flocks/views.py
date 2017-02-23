from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Flock, AnimalExits
from .forms import FlockForm, AnimalExitsForm


# Create your views here.
def index(request):
    current_flocks = [obj for obj in Flock.objects.all() if obj.number_of_living_animals > 0]
    old_flocks = [obj for obj in Flock.objects.all() if obj.number_of_living_animals == 0]
    old_flocks = old_flocks[:8]
    return render(request, 'flocks/index.html', {'current_flocks': current_flocks, 'old_flocks': old_flocks})


def create(request):
    form = FlockForm()
    return render(request, 'flocks/create.html', {'form': form})


def save(request):
    form = FlockForm(request.POST)

    if form.is_valid():
        data = form.cleaned_data
        flock = Flock(entry_date=data.get('entry_date'),
                      entry_weight=data.get('entry_weight'),
                      number_of_animals=data.get('number_of_animals'))
        flock.save()
        return HttpResponseRedirect('/flocks/')

    return render(request, 'flocks/create.html', {'form': form})


def detail(request, flock_id):
    flock = get_object_or_404(Flock, pk=flock_id)
    exit_list = flock.animalexits_set.all()
    return render(request, 'flocks/detail.html', {'flock': flock, 'list_exits': exit_list})


def create_animal_death(request):
    return render(request, 'flocks/index.html')


def create_animal_exit(request):
    form = AnimalExitsForm()
    return render(request, 'animalexits/create.html', {'form': form})


def save_animal_exit(request):
    form = AnimalExitsForm(request.POST)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/flocks/detail/%d' % form.cleaned_data['flock'].id)

    return render(request, 'animalexits/create.html', {'form': form})
