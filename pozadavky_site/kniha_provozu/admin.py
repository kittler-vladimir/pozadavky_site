from django.contrib import admin
from .models import ZaznamKnihaProvozu, HistorieKnihaProvozu


class HistorieKnihaProvozuInline(admin.TabularInline):
    model = HistorieKnihaProvozu
    fk_name = 'zaznam_id'
    extra = 0
    readonly_fields = ('date_run', 'changed_by', 'field_name', 'old_value', 'new_value', 'note')
    can_delete = False
    ordering = ('-date_run',)


@admin.register(ZaznamKnihaProvozu)
class ZaznamKnihaProvozuAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'author', 'status', 'type_of_launch', 'added')
    list_filter = ('status', 'type_of_launch', 'trigger_frequency')
    search_fields = ('name', 'version', 'author', 'description')
    inlines = [HistorieKnihaProvozuInline]

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = ZaznamKnihaProvozu.objects.get(pk=obj.pk)
            tracked_fields = [
                'name', 'version', 'author', 'location', 'command',
                'type_of_launch', 'trigger_frequency', 'description',
                'link_to_details', 'status',
            ]
            for field in tracked_fields:
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
