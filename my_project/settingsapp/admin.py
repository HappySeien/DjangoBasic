from django.contrib import admin

# Register your models here.


class BaseAdminSettings(admin.ModelAdmin):
    list_per_page: int = 10
    actions = ['mark_deleted', 'mark_undeleted']

    def mark_deleted(self, request, queryset) -> None:
        queryset.update(deleted=True)

    mark_deleted.short_description = 'Пометить удаленным'

    def mark_undeleted(self, request, queryset) -> None:
        queryset.update(deleted=False)

    mark_undeleted.short_description = 'Восстановить'
