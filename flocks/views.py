from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .models import Flock, AnimalSeparation
from .forms import FlockForm, AnimalExitsForm, AnimalDeathForm
from .forms import AnimalSeparationForm, SeparationDeathForm, SeparationExitForm

@login_required
def index(request):
    current_flocks = [obj for obj in Flock.objects.all() if obj.number_of_living_animals > 0]
    old_flocks = [obj for obj in Flock.objects.all().order_by('-entry_date') if obj.number_of_living_animals == 0]
    old_flocks = old_flocks[:8]
    return render(request, 'flocks/index.html', {'current_flocks': current_flocks, 'previous_flocks': old_flocks})


@login_required
def create(request):
    form = FlockForm()
    return render(request, 'flocks/create.html', {'form': form})


@login_required
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


@login_required
def detail(request, flock_id):
    flock = get_object_or_404(Flock, pk=flock_id)
    exit_list = flock.animalexits_set.all()
    death_list = flock.animaldeath_set.all()
    separation_list = flock.animalseparation_set.all()
    room_entries = flock.animalroomentry_set.all()
    room_exits = flock.animalroomexit_set.filter(number_of_animals__gt=0)

    param_list = {
        'flock': flock,
        'exits_list': exit_list,
        'death_list': death_list,
        'separation_list': separation_list,
        'room_entries': room_entries,
        'room_exits': room_exits
    }
    return render(request, 'flocks/detail.html', param_list)


@login_required
def create_animal_death(request):
    form = AnimalDeathForm()
    return render(request, 'animaldeaths/create.html', {'form': form})


@login_required
def save_animal_death(request):
    form = AnimalDeathForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/flocks/detail/%d' % form.cleaned_data['flock'].id)

    return render(request, 'animaldeaths/create.html', {'form': form})


@login_required
def create_animal_exit(request):
    form = AnimalExitsForm()
    return render(request, 'animalexits/create.html', {'form': form})


@login_required
def save_animal_exit(request):
    form = AnimalExitsForm(request.POST)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/flocks/detail/%d' % form.cleaned_data['flock'].id)

    return render(request, 'animalexits/create.html', {'form': form})


@login_required
def create_animal_separation(request):
    form = AnimalSeparationForm()
    flock_id = request.GET.get('flockid', None)
    if flock_id:
        flock = Flock.objects.filter(id=flock_id)[0]
        form = AnimalSeparationForm(initial={'flock': flock})

    return render(request, 'animal_separations/create.html', {'form': form})


@login_required
def save_animal_separation(request):
    form = AnimalSeparationForm(request.POST)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/flocks/detail/%d' % form.cleaned_data['flock'].id)

    return render(request, 'animal_separations/create.html', {'form': form})


@login_required
def view_animal_separation(request, separation_id):
    separation = get_object_or_404(AnimalSeparation, pk=separation_id)
    return render(request, 'animal_separations/detail.html', {'separation': separation})


@login_required()
def create_separation_death(request):
    separation_id = request.GET.get('separation_id', None)
    if separation_id is None:
        return HttpResponseBadRequest()
    separation = AnimalSeparation.objects.get(id=separation_id)
    form = SeparationDeathForm(separation_id=separation_id)
    parameters = {
        'form': form,
        'separation': separation
    }
    return render(request, 'animal_separations/register_death.html', parameters)


@login_required()
def save_separation_death(request):
    form = SeparationDeathForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/flocks/')
    return render(request, 'animal_separations/register_death.html', {'form': form})


@login_required()
def create_separation_exit(request):
    separation_id = request.GET.get('separation_id', None)
    if separation_id is None:
        return HttpResponseBadRequest()
    separation = AnimalSeparation.objects.get(id=separation_id)
    form = SeparationExitForm(separation_id=separation_id)
    parameters = {
        'form': form,
        'separation': separation
    }
    return render(request, 'animal_separations/register_exit.html', parameters)


@login_required()
def save_separation_exit(request):
    form = SeparationExitForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/flocks/')
    return render(request, 'animal_separations/register_exit.html', {'form': form})
