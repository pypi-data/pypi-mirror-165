from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import PageNotFoundEntry


class PageNotFoundPermissionHelper(PermissionHelper):
    def user_can_create(self, user):
        return True


@modeladmin_register
class PageNotFoundEntryAdmin(ModelAdmin):
    permission_helper_class = PageNotFoundPermissionHelper
    model = PageNotFoundEntry
    menu_label = "404 Redirects"
    menu_icon = "redirect"
    list_display = (
        "url",
        "redirect_to_url",
        "redirect_to_page",
        "hits",
        "permanent",
        "last_hit",
        "regular_expression",
    )
    list_filter = ("permanent", "regular_expression", "site")
    search_fields = ("url", "redirect_to_url")
