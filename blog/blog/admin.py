from django.contrib import admin, messages
from .models import Article, User


def make_published(modeladmin, request, queryset):
    updated = queryset.update(is_published=True)
    modeladmin.message_user(request, f"{updated} постів було опубліковано.", messages.SUCCESS)

make_published.short_description = "Опублікувати вибрані пости"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # Tree Views
    list_display = ("user__username","user__email", "name", "date_created", "text_summarized", "is_published")
    list_display_links = ("user__email", "name", "date_created")
    list_filter = ("user", "date_created")
    search_fields = ("user__username","text")
    actions = [make_published,]

    # Form View
    # inlines = [UserInline]
    readonly_fields = ("name","user","date_created")
    fieldsets = (
        ("Article Content:", {
            "fields": ("name", "text", "user", "date_created"),
            "description": "Main datas about Article"
        }),
        ("Admin Info:", {
            "fields": ("slug", "approver_users"),
            "classes": ("collapse",)
        }),
        ("Other:", {
            "fields": ("watched_users","date"),
        })
    )

    def text_summarized(self, obj):
        return obj.text[:20]

    def get_queryset(self, request):
        return self.model.objects.all().select_related("user")