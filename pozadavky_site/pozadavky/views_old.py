from django.shortcuts import render,  get_object_or_404
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.http import HttpResponse
from .models import Requirement
from django.contrib.auth.models import Permission, User, Group
from django.db.models import F



table_headers = [(u'č.',u'task number'),(u'Úkol',u'requirement'),(u'cislo_jednaci', u'document number'), (u'Termin','deadline'),
                     (u'Oddeleni',u'group'),(u'Vlastník','owner'),(u'Kategorie úkolu','task category'), (u'Stav úkolu','status request'),('Splneno','done')]


def home_page(request):
    content = {}
    content["info"] = "Informační systém Úkoly"
    user = request.user
    return render_to_response(
        "homepage.html", {"content": content, "user": user }#, "aktuality": aktuality}
    )


def tasks_all(request):
    content = {"info": "Úkoly – seznam"}
    user = request.user

    # Staff vidí vše
    if user.is_staff:
        task_list = Requirement.objects.all().order_by('-added')
    else:
        # běžný uživatel vidí jen své úkoly, které nejsou hotové
        task_list = Requirement.objects.filter(
            owner=user,
            done__isnull=True
        ).order_by('-added')

    paginator = Paginator(task_list, 33)
    page = request.GET.get('page', 1)

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    return render(
        request,
        'tasks.html',
        {
            "content": content,
            "tasks": tasks,
            "user": user,
            "table_headers": table_headers,
        },
    )

#https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html


def tasks_done(request):
    content = {}
    content["info"] = "Ukoly seznam"
    user = request.user
    if user.is_staff :
        # tady to neumim nadefinofat done, proto vynechavam v nabidce 
        task_list = Requirement.objects.all().filter(done = None ).order_by('added').reverse()
    else:    
        group_user = Owner.objects.get(pk=user.id,done = None).order_by('added').reverse()    
        #task_list = Requirement.objects.all().filter(owner_id=user.id).order_by('added').reverse()
        
    page = request.GET.get('page', 1)
    paginator = Paginator(task_list, 33)

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    
    return render_to_response(
        'tasks.html', {"content": content,'tasks': tasks,"user": user, 'table_headers':table_headers}
    )
    

def tasks_done_after(request):
    user = request.user
    content = {"info": "Úkoly dokončené po termínu"}

    # základní filtry: mají termín, jsou hotové, ale později než deadline
    filters = {
        "deadline__isnull": False,
        "done__isnull": False,
        "done__gt": F("deadline"),
    }

    # běžný uživatel → vidí jen své úkoly
    if not user.is_staff:
        filters["owner"] = user

    # dotaz + řazení
    task_list = Requirement.objects.filter(**filters).order_by("-added")

    # stránkování
    paginator = Paginator(task_list, 33)
    page = request.GET.get("page", 1)

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    return render(
        request,
        "tasks.html",
        {
            "content": content,
            "tasks": tasks,
            "user": user,
            "table_headers": table_headers,
        },
    )


def tasks_not_done(request):
    content = {"info": "Úkoly – nesplněné"}
    user = request.user

    # definice základních filtrů
    filters = {
        "deadline__isnull": False,   # musí mít termín
        "done__isnull": True,        # není dokončeno
    }

    # pokud je uživatel zaměstnanec (není staff), zobrazí se jen jeho úkoly
    if not user.is_staff:
        filters["owner"] = user

    # načtení seznamu úkolů podle filtrů
    task_list = Requirement.objects.filter(**filters).order_by('-added')

    # stránkování
    paginator = Paginator(task_list, 33)
    page = request.GET.get('page', 1)

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    # definuj záhlaví tabulky, pokud není globální
    # table_headers = ["Úkol", "Kategorie", "Typ", "Vlastník", "Termín", "Stav"]

    return render(
        request,
        'tasks.html',
        {
            "content": content,
            "tasks": tasks,
            "user": user,
            "table_headers": table_headers,
        },
    )


from django.utils import timezone

def tasks_not_done_after(request):
    user = request.user
    content = {"info": "Úkoly po termínu"}

    # základní filtry
    filters = {
        "deadline__isnull": False,             # musí mít termín
        "done__isnull": True,                  # není dokončeno
        "deadline__lt": timezone.now().date(), # termín už uplynul
    }

    # běžní uživatelé vidí jen své úkoly
    if not user.is_staff:
        filters["owner"] = user

    # dotaz + řazení
    task_list = Requirement.objects.filter(**filters).order_by('-added')

    # stránkování
    paginator = Paginator(task_list, 33)
    page = request.GET.get('page', 1)

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    return render(
        request,
        "tasks.html",
        {
            "content": content,
            "tasks": tasks,
            "user": user,
            "table_headers": table_headers,
        },
    )


def groups(request):
    
    content = {}
    content["info"] = "Ukoly - skupiny"
    user = request.user
    group_list = Group.objects.all().order_by('name') #.filter(owner_id = owner_id).order_by('added').reverse()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(group_list, 33)
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)

    return render_to_response(
        'groups.html', {"content": content, 'groups': groups,"user": user}   #, 'table_headers':table_headers}
    )

def authors(request):
    content = {}
    content["info"] = "Ukoly - autori"
    user = request.user
    #authors_list = User.objects.all().order_by('last_name') #.filter(owner_id = owner_id).order_by('added').reverse()
    authors_list = User.objects.all().filter(is_staff=True).order_by('last_name')  
    
    page = request.GET.get('page', 1)
    paginator = Paginator(authors_list, 33)
    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)

    return render_to_response(
        'authors.html', {"content": content, "authors": authors, "user": user}   #, 'table_headers':table_headers}
    )


def task_detail(request, requirement_id):
    # return HttpResponse("You're looking at question %s." % requirement_id)
    content = {}
    content["info"] = "Ukoly - ukol"
    user = request.user
    try:
        task = Requirement.objects.get(pk=requirement_id)   
        #task = Requirement.objects.filter(id=requirement_id)[0]
    except IndexError:
        return HttpResponseRedirect('')
    
    return render_to_response(
        'task_detail.html', {"content":content,"task": task, "user": user}
        )

def tasks_owner(request, owner_id):
    
    content = {}
    content["info"] = "Ukoly - ukol"
    user = request.user
    task_list = Requirement.objects.all().filter(owner_id = owner_id).order_by('added').reverse()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(task_list, 33)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    
    return render_to_response(
        'tasks.html', {"content": content, 'tasks': tasks,"user": user, 'table_headers':table_headers}
    )
    
    
    # return HttpResponse("You're looking at owner %s." % owner_id)

def tasks_author(request, author_id):
    
    content = {}
    content["info"] = "Ukoly - ukol"
    user = request.user
    task_list = Requirement.objects.all().filter(author_id = author_id).order_by('added').reverse()
    page = request.GET.get('page', 1)
    paginator = Paginator(task_list, 33)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    
    return render_to_response(
        'tasks.html', {"content": content, 'tasks': tasks,"user": user, 'table_headers':table_headers}
    )


def tasks_group(request, group_owner_id):
    content = {}
    content["info"] = "Ukoly - oddeleni"
    user = request.user
    #context = {'employee':employee, 'creations':creations, 'creation_count':creation_count}
  
    # try:
    #     tasks_list = Requirement.objects.all().filter(group_owner_id = group_owner_id).order_by('added').reverse()
    #
    # except tasks_list.DoesNoExist:
    #     raise Http404("tasks does not exist")
    
    task_list = Requirement.objects.all().filter(group_owner_id = group_owner_id).order_by('added').reverse()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(task_list, 33)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    
    return render_to_response(
        'tasks.html', {"content": content, 'tasks': tasks,"user": user, 'table_headers':table_headers}
    )
   
    #return HttpResponse("You're looking at group %s." % group_owner_id)


from django.contrib.auth import authenticate, login

def login_view_authorization(request):
    content = {}
    username = request.POST["username"]
    password = request.POST["password"]
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return render_to_response(
            "homepage.html", {"content": content, "user":user} 
        )
    else:
        return render(request, 'registration/invalidlogin.html')
        # return HttpResponse("Invalid login")

def logout_view(request):
        return render(request, 'registration/logout.html')
        