from django.contrib import admin

# Register your models here.


class BaseAdminSettings(admin.ModelAdmin):
    list_per_page: int = 10
    actions = ['mark_deleted']

    def mark_deleted(self, request, queryset) -> None:
        queryset.update(deleted=True)

    mark_deleted.short_description = 'Пометить удаленным'
