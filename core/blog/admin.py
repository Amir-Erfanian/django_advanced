from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "post_count")
    search_fields = ("name",)
    ordering = ("name",)

    @admin.display(description=_("Posts"))
    def post_count(self, obj):
        return obj.post_set.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "status",
        "published_date",
        "created_date",
        "thumbnail",
    )
    list_filter = ("status", "category", "author", "created_date", "published_date")
    search_fields = ("title", "content", "author__email")
    ordering = ("-published_date",)
    date_hierarchy = "published_date"
    list_select_related = ("author", "category")   # avoids N+1
    list_per_page = 25

    readonly_fields = ("created_date", "updated_date", "image_preview")
    autocomplete_fields = ("author", "category")   # nice pickers instead of huge dropdowns

    fieldsets = (
        (None, {
            "fields": ("title", "author", "category", "status", "published_date")
        }),
        (_("Content"), {
            "fields": ("content",)
        }),
        (_("Media"), {
            "fields": ("image", "image_preview")
        }),
        (_("Timestamps"), {
            "classes": ("collapse",),
            "fields": ("created_date", "updated_date"),
        }),
    )

    # ---- image preview in change form ----
    @admin.display(description=_("Preview"))
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:150px;border-radius:6px;" />',
                obj.image.url,
            )
        return "—"

    # ---- thumbnail in changelist ----
    @admin.display(description=_("Image"))
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px;" />',
                obj.image.url,
            )
        return "—"

    # ---- auto-fill published_date when first published ----
    def save_model(self, request, obj, form, change):
        from django.utils import timezone

        if obj.status and not obj.published_date:
            obj.published_date = timezone.now()
        super().save_model(request, obj, form, change)