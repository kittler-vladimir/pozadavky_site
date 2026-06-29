from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.db.models import F, Q
from django.http import JsonResponse
from .models import Requirement

table_headers = [
    (u'č.', u'task number'),
    (u'Úkol', u'requirement'),
    (u'cislo_jednaci', u'document number'),
    (u'Termín', 'deadline'),
    (u'Oddělení', u'group'),
    (u'Vlastník', 'owner'),
    (u'Kategorie úkolu', 'task category'),
    (u'Stav úkolu', 'status request'),
    ('Splněno', 'done'),
]


# ---------------------------------------------------------
# 🧩 Pomocná funkce pro všechny seznamy úkolů
# ---------------------------------------------------------
def render_task_list(request, filters, info_text, task_type=None):
    """
    Zobrazí seznam úkolů podle daných filtrů.
    - běžní uživatelé vidí své úkoly + úkoly svého oddělení
    - umožňuje vyhledávání (?q=)
    """
    user = request.user
    content = {"info": info_text}

    # 🟩 základní filtr
    query = Requirement.objects.filter(**filters)

    # # 🟦 běžní uživatelé – omezit na jejich úkoly a oddělení
    # if not user.is_staff:
    #     user_groups = user.groups.all()
    #     query = query.filter(
    #     Q(owner=user) | Q(group_owner__in=user_groups)
    # )
    
   # 🔹 Superuser – vidí všechny úkoly
    if user.is_superuser:
        pass  # žádný filtr – vidí vše
    # 🟩 Administrativní uživatelé – vidí své a oddělení
    elif user.is_staff:
        user_groups = user.groups.all()
        query = query.filter(
            Q(owner=user) | Q(group_owner__in=user_groups)
        )
    # 🟨 Běžní uživatelé – vidí jen své úkoly
    else:
        query = query.filter(owner=user)
    
    # 🧾 řazení
    task_list = query.order_by("-added")
    
         
    # 🔍 fulltext vyhledávání
    search_term = request.GET.get("q", "").strip()
    if search_term:
        query = query.filter(
            Q(requirement__icontains=search_term) |
            Q(description__icontains=search_term)
        )
        content["search_term"] = search_term
        
    # 📄 stránkování
    paginator = Paginator(task_list, 33)
    page = request.GET.get("page", 1)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
        
        
    #rint('task_type:' , task_type)        

    return render(
        request,
        "tasks.html",
        {
            "content": content,
            "tasks": tasks,
            "user": user,
            "task_type": task_type,   
            "table_headers": table_headers,
        },
    )


# ---------------------------------------------------------
# 📄 Jednotlivé pohledy
# ---------------------------------------------------------

def home_page(request):
    content = {"info": "Informační systém Úkoly"}
    user = request.user
    return render(request, "homepage.html", {"content": content, "user": user})
    

def tasks_all(request):
    filters = {}
    task_type = request.path.strip("/").split("/")[1]  
    return render_task_list(request, filters, "Všechny úkoly", task_type=task_type)


def tasks_done(request):
    filters = {
        "deadline__isnull": False,
        "done__isnull": False,
    }
    task_type = request.path.strip("/").split("/")[1]  
    return render_task_list(request, filters, "Úkoly – splněné", task_type=task_type)

def tasks_done_by(request, user_id):
    filters = {
        "deadline__isnull": False,
        "done__isnull": False,
        "owner_id": user_id,
    }
    task_type = request.path.strip("/").split("/")[1]  
    return render_task_list(request, filters, "Úkoly – splněné", task_type=task_type)

def tasks_not_done(request):
    filters = {
        "deadline__isnull": False,
        "done__isnull": True,
    }
    #return render_task_list(request, filters, "Úkoly – nesplněné")

    # název typu vyčteme z request.path
    # /tasks/nesplnene/by/4/
    # → vezmeme druhý segment
    task_type = request.path.strip("/").split("/")[1]  
    return render_task_list(request, filters,"Úkoly – nesplněné", task_type=task_type)



def tasks_not_done_by(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    filters = {
        "deadline__isnull": False,
        "done__isnull": True,
        "owner": user
    }
    title = f"Nesplněné úkoly – {user.get_full_name() or user.username}"
    task_type = request.path.strip("/").split("/")[1]  
    return render_task_list(request, filters,title,task_type=task_type)

def tasks_done_after(request):
    filters = {
        "deadline__isnull": False,
        "done__isnull": False,
        "done__gt": F("deadline"),
    }
    task_type = request.path.strip("/").split("/")[1]
    return render_task_list(request, filters, "Úkoly dokončené po termínu", task_type=task_type)

def tasks_done_after_by(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    filters = {
        "deadline__isnull": False,
        "done__isnull": False,
        "owner": user
    }
    title = f"Úkoly dokončené po termínu – {user.get_full_name() or user.username}"
    task_type = request.path.strip("/").split("/")[1]  
    return render_task_list(request, filters, title, task_type=task_type)


def tasks_not_done_after(request):
    filters = {
        "deadline__isnull": False,
        "done__isnull": True,
        "deadline__lt": timezone.now().date(),
    }
    task_type = request.path.strip("/").split("/")[1]
    return render_task_list(request, filters, "Úkoly po termínu", task_type=task_type)

def tasks_not_done_after_by(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    filters = {
        "deadline__isnull": False,
        "done__isnull": True,
        "deadline__lt": timezone.now().date(),
        "owner": user
    }
    title = f"Úkoly po termínu – {user.get_full_name() or user.username}"
    task_type = request.path.strip("/").split("/")[1]  
    return render_task_list(request, filters, title, task_type=task_type)





def users_by_group(request, group_id):
    users = User.objects.filter(groups__id=group_id, is_active=True)
    return JsonResponse(list(users.values("id", "username")), safe=False)


def groups(request):
    content = {"info": "Úkoly – skupiny"}
    user = request.user
    # 🔹 Skupiny, které nechceš zobrazovat
    excluded_groups = ["Vedoucí", "Admins"]
    # 🔸 Načti všechny skupiny kromě vyloučených
    group_list = Group.objects.exclude(name__in=excluded_groups).order_by("name")
    # 🔹 Stránkování (paginator)
    paginator = Paginator(group_list, 33)
    page = request.GET.get("page", 1)
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)

    return render(request, "groups.html", {"content": content, "groups": groups, "user": user})



def authors(request):
    content = {"info": "Úkoly – autoři"}
    user = request.user
    authors_list = User.objects.filter(is_staff=True).order_by("last_name")

    paginator = Paginator(authors_list, 33)
    page = request.GET.get("page", 1)
    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)

    return render(request, "authors.html", {"content": content, "authors": authors, "user": user})


def task_detail(request, requirement_id):
    user = request.user
    task = get_object_or_404(Requirement, pk=requirement_id)
    content = {"info": "Úkol – detail"}
    return render(request, "task_detail.html", {"content": content, "task": task, "user": user})


def tasks_owner(request, owner_id):
    filters = {"owner_id": owner_id}
    return render_task_list(request, filters, f"Úkoly vlastníka {owner_id}")

def tasks_by_owner(request, owner_id, task_type=None):
    filters = {"owner_id": owner_id}

    # Rozlišení podle task_type
    if task_type == "nesplnene":
        filters["done__isnull"] = True
    elif task_type == "splnene":
        filters["done__isnull"] = False
    elif task_type == "splnenepozde":
        filters["done__isnull"] = False
        filters["deadline__lt"] = F("done")

    return render_task_list(request, filters, f"Úkoly – {task_type}")



def tasks_author(request, author_id):
    filters = {"author_id": author_id}
    return render_task_list(request, filters, f"Úkoly autora {author_id}")


def tasks_group(request, group_owner_id):
    filters = {"group_owner_id": group_owner_id}
    return render_task_list(request, filters, f"Úkoly oddělení {group_owner_id}")


# ---------------------------------------------------------
# 🔐 Autentizace
# ---------------------------------------------------------
def login_view_authorization(request):
    content = {}
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, "homepage.html", {"content": content, "user": user})
    else:
        return render(request, "registration/invalidlogin.html")


def logout_view(request):
    return render(request, "registration/logout.html")
