from django.contrib import admin
from django import forms
from django_middleware_global_request import get_request
from django.urls import path
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.db.models import Q

from .models import Requirement, Work_status, Requirement_type


class RequirementAdminForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        group_id = None

        if self.data.get('group_owner'):
            try:
                group_id = int(self.data.get('group_owner'))
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.group_owner_id:
            group_id = self.instance.group_owner_id

        if group_id:
            self.fields['owner'].queryset = User.objects.filter(
                groups__id=group_id,
                is_active=True
            )
        else:
            self.fields['owner'].queryset = User.objects.none()

    def save(self, commit=True):
        instance = super().save(commit=False)
        request = get_request()
        if request and request.user.is_authenticated and not instance.author_id:
            instance.author = request.user
        if commit:
            instance.save()
        return instance


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    form = RequirementAdminForm

    class Media:
        js = ('admin/js/jquery.init.js', 'js/requirement_admin.js',)

    list_display = (
        'id', 'requirement', 'author_fullname', 'group_owner',
        'owner_fullname', 'status', 'deadline', 'done',
    )

    list_filter = (
        'status', 'group_owner', 'owner', 'category', 'requirement_type','added',
    )

    search_fields = (
        'requirement', 'cislo_jednaci',
        'author__first_name', 'author__last_name', 'author__username',
        'owner__first_name', 'owner__last_name', 'owner__username',
    )

    readonly_fields = ('author_display', 'added')


    fieldsets = (
        ('Základní údaje', {'fields': (
            'requirement', 'cislo_jednaci', 'description',
        )}),
        ('Klasifikace', {'fields': (
            'category', 'requirement_type', 'status',
        )}),
        ('Přiřazení', {'fields': (
            'group_owner', 'owner', 'author_display',
        )}),
        ('Termíny', {'fields': (
            'deadline', 'done', 'added',
        )}),
    )

    # --------------------------
    # Pomocné funkce pro zobrazení celého jména
    # --------------------------
    def author_fullname(self, obj):
        if obj.author:
            full = obj.author.get_full_name()
            return full if full.strip() else obj.author.username
        return "-"
    author_fullname.short_description = "Zadal"

    def owner_fullname(self, obj):
        if obj.owner:
            full = obj.owner.get_full_name()
            return full if full.strip() else obj.owner.username
        return "-"
    owner_fullname.short_description = "Vlastník"
    
    def author_display(self, obj):
        if obj.author:
            full = obj.author.get_full_name()
            return full if full.strip() else obj.author.username
        return "-"
    author_display.short_description = "Zadal"

    # --------------------------
    # Omezení skupin v adminu
    # --------------------------
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group_owner":
            excluded_groups = ["Vedoucí", "Admins"]

            if request.user.is_superuser:
                kwargs["queryset"] = Group.objects.exclude(name__in=excluded_groups).order_by("id")
            else:
                user_groups = request.user.groups.exclude(name__in=excluded_groups)
                kwargs["queryset"] = user_groups.order_by("id")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # --------------------------
    # Omezení výpisu úkolů podle uživatele
    # --------------------------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        user_groups = request.user.groups.all()
        return qs.filter(Q(owner=request.user) | Q(group_owner__in=user_groups))

    # --------------------------
    # AJAX URL
    # --------------------------
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get_owners/', self.admin_site.admin_view(self.get_owners), name='requirement-get-owners'),
        ]
        return custom_urls + urls

    # --------------------------
    # AJAX view vrací jméno + příjmení
    # --------------------------
    def get_owners(self, request):
        group_id = request.GET.get('group_id')
        if not group_id:
            return JsonResponse([], safe=False)

        users = User.objects.filter(
            groups=group_id,
            is_active=True
        ).values('id', 'username', 'first_name', 'last_name')

        formatted = []
        for u in users:
            full_name = f"{u['first_name']} {u['last_name']}".strip()
            if not full_name:
                full_name = u['username']
            formatted.append({
                'id': u['id'],
                'name': full_name
            })

        return JsonResponse(formatted, safe=False)

    # --------------------------
    # Uložení + automatické nastavení stavu
    # --------------------------
    def save_model(self, request, obj, form, change):
        if not change and not obj.author_id:
            obj.author = request.user

        if obj.done:
            status, _ = Work_status.objects.get_or_create(
                status_text__iexact="Splněno",
                defaults={'status_text': "Splněno"},
            )
        else:
            status, _ = Work_status.objects.get_or_create(
                status_text__iexact="Rozpracováno",
                defaults={'status_text': "Rozpracováno"},
            )

        obj.status = status
        super().save_model(request, obj, form, change)


@admin.register(Work_status)
class WorkStatusAdmin(admin.ModelAdmin):
    list_display = ('status_text',)
    search_fields = ('status_text',)


@admin.register(Requirement_type)
class RequirementTypeAdmin(admin.ModelAdmin):
    list_display = ('requirement_type_text',)
    search_fields = ('requirement_type_text',)
