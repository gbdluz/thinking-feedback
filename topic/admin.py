from django.contrib import admin
from django.contrib.auth.models import Group, User

# Register your models here.
from topic.models import Grade, Skill, Topic
from users.models import Initial_Password, Stage, Your_Stage

admin.site.register(Topic)
admin.site.register(Skill)
admin.site.unregister(Group)


class StageInline(admin.StackedInline):
    model = Your_Stage
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "password",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    inlines = [StageInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Grade)
admin.site.register(Stage)
admin.site.register(Initial_Password)
