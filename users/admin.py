from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html

from users.models.user import UserProfile
from review.models.review import Review


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


# Overload User admin model
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('show_reviews', )
    inlines = (UserProfileInline,)

    def show_reviews(self, obj):
        count = Review.objects.filter(user=obj).count()
        url = reverse('admin:review_review_changelist') + f'?user__id={obj.id}'
        plural = 's' if count != 1 else ''
        return format_html('<a href="{}">{} Review{}</a>', url, count, plural)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(UserAdmin, self).get_inline_instances(request, obj)


# Register new User admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
