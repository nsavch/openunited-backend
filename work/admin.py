from django.contrib import admin
from work.models import Product, Initiative, Task, Tag, Expertise, \
    Attachment, CodeRepository, CreateProductRequest, Capability


class InitiativeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'short_description', 'initiative')


admin.site.register(Attachment)
admin.site.register(Capability)
admin.site.register(CodeRepository)
admin.site.register(CreateProductRequest)
admin.site.register(Initiative, InitiativeAdmin)
admin.site.register(Product)
admin.site.register(Task, TaskAdmin)
admin.site.register(Tag)
admin.site.register(Expertise)
