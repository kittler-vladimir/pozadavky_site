from django.contrib import admin
from .models import ZaznamKnihaProvozu, HistorieKnihaProvozu

TRACKED_FIELDS = ['den', 'cas', 'kde_server', 'dir', 'popis', 'text', 'kdo', 'poznamka']


class HistorieKnihaProvozuInline(admin.TabularInline):
    model = HistorieKnihaProvozu
    fk_name = 'zaznam_id'
    extra = 0
    readonly_fields = ('date_run', 'changed_by', 'field_name', 'old_value', 'new_value', 'note')
    can_delete = False
    ordering = ('-date_run',)


@admin.register(ZaznamKnihaProvozu)
class ZaznamKnihaProvozuAdmin(admin.ModelAdmin):
    list_display = ('den', 'cas', 'kde_server', 'dir', 'kdo', 'added')
    list_filter = ('kde_server', 'kdo')
    search_fields = ('kde_server', 'dir', 'popis', 'text', 'kdo', 'poznamka')
    inlines = [HistorieKnihaProvozuInline]

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = ZaznamKnihaProvozu.objects.get(pk=obj.pk)
            for field in TRACKED_FIELDS:
                old_value = getattr(old_obj, field)
                new_value = getattr(obj, field)
                if old_value != new_value:
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
