from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import ZaznamKnihaProvozu, HistorieKnihaProvozu
from .forms import ZaznamKnihaProvozuForm

TRACKED_FIELDS = [
    'name', 'version', 'author', 'location', 'command',
    'type_of_launch', 'trigger_frequency', 'description',
    'link_to_details', 'status',
]


@login_required
def zaznam_list(request):
    zaznamy = ZaznamKnihaProvozu.objects.all()
    search = request.GET.get('search', '')
    if search:
        zaznamy = zaznamy.filter(name__icontains=search)
    return render(request, 'kniha_provozu/zaznam_list.html', {
        'zaznamy': zaznamy,
        'search': search,
    })


@login_required
def zaznam_detail(request, zaznam_id):
    zaznam = get_object_or_404(ZaznamKnihaProvozu, pk=zaznam_id)
    historie = zaznam.Id.all()
    return render(request, 'kniha_provozu/zaznam_detail.html', {
        'zaznam': zaznam,
        'historie': historie,
    })


@login_required
def zaznam_create(request):
    if request.method == 'POST':
        form = ZaznamKnihaProvozuForm(request.POST)
        if form.is_valid():
            zaznam = form.save(commit=False)
            zaznam.created_by = request.user
            zaznam.save()
            messages.success(request, 'Záznam byl úspěšně vytvořen.')
            return redirect('kniha_provozu:zaznam_detail', zaznam_id=zaznam.id)
    else:
        form = ZaznamKnihaProvozuForm()
    return render(request, 'kniha_provozu/zaznam_form.html', {'form': form, 'is_new': True})


@login_required
def zaznam_update(request, zaznam_id):
    zaznam = get_object_or_404(ZaznamKnihaProvozu, pk=zaznam_id)

    if request.method == 'POST':
        old_values = {field: getattr(zaznam, field) for field in TRACKED_FIELDS}
        form = ZaznamKnihaProvozuForm(request.POST, instance=zaznam)
        if form.is_valid():
            updated_zaznam = form.save()

            for field in TRACKED_FIELDS:
                old_value = old_values[field]
                new_value = getattr(updated_zaznam, field)
                if old_value != new_value:
                    HistorieKnihaProvozu.objects.create(
                        zaznam_id=updated_zaznam,
                        changed_by=request.user,
                        field_name=field,
                        old_value=old_value,
                        new_value=new_value,
                    )
            messages.success(request, 'Záznam byl úspěšně upraven, změny zaznamenány do historie.')
            return redirect('kniha_provozu:zaznam_detail', zaznam_id=updated_zaznam.id)
    else:
        form = ZaznamKnihaProvozuForm(instance=zaznam)

    return render(request, 'kniha_provozu/zaznam_form.html', {'form': form, 'zaznam': zaznam, 'is_new': False})
