from django.contrib import admin
from .models import ZaznamKnihaProvozu, HistorieKnihaProvozu

TRACKED_FIELDS = [
    'name', 'version', 'author', 'location', 'command', 'launched_at',
    'type_of_launch', 'trigger_frequency', 'description',
    'link_to_details', 'status',
]


class HistorieKnihaProvozuInline(admin.TabularInline):
    model = HistorieKnihaProvozu
    fk_name = 'zaznam_id'
    extra = 0
    readonly_fields = ('date_run', 'changed_by', 'field_name', 'old_value', 'new_value', 'note')
    can_delete = False
    ordering = ('-date_run',)


@admin.register(ZaznamKnihaProvozu)
class ZaznamKnihaProvozuAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'version', 'author', 'location', 'launched_at', 'type_of_launch',
        'trigger_frequency', 'status', 'created_by', 'added',
    )
    list_filter = ('status', 'type_of_launch', 'trigger_frequency')
    search_fields = ('name', 'author', 'location', 'command', 'description')
    readonly_fields = ('created_by', 'added')
    inlines = [HistorieKnihaProvozuInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user.get_full_name() or request.user.username
        else:
            old_obj = ZaznamKnihaProvozu.objects.get(pk=obj.pk)
            for field in TRACKED_FIELDS:
                old_value = getattr(old_obj, field)
                new_value = getattr(obj, field)
                if (old_value or '') != (new_value or ''):
                    HistorieKnihaProvozu.objects.create(
                        zaznam_id=obj,
                        changed_by=request.user,
                        field_name=field,
                        old_value=old_value,
                        new_value=new_value,
                    )
        super().save_model(request, obj, form, change)


@admin.register(HistorieKnihaProvozu)
class HistorieKnihaProvozuAdmin(admin.ModelAdmin):
    list_display = ('zaznam_id', 'field_name', 'date_run', 'changed_by')
    list_filter = ('field_name',)
    readonly_fields = ('date_run',)
