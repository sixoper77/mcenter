from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "surname",
        "role",
        "email",
        "phone",
    )
    search_fields = (
        "^first_name",
        "^last_name",
        "^username",
        "^email",
        "phone",
    )
    list_filter = ("role",)
    ordering = ("-id",)
    save_on_top = True

    @admin.display(description="Full name")
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name} {obj.surname}".strip()
