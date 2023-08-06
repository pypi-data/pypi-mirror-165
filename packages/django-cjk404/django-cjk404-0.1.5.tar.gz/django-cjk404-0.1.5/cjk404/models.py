from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.core.models import Page, Site


class PageNotFoundEntry(models.Model):
    site = models.ForeignKey(
        Site,
        related_name="pagenotfound_entries",
        on_delete=models.CASCADE,
        verbose_name="Site",
    )

    url = models.CharField(max_length=200, verbose_name="Redirect from URL")
    redirect_to_url = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Redirect to URL",
    )
    redirect_to_page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Redirect to Page",
    )

    created = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Created"
    )
    last_hit = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Last Hit"
    )
    hits = models.PositiveIntegerField(default=0, verbose_name="# Hits")
    permanent = models.BooleanField(default=False)

    regular_expression = models.BooleanField(default=False, verbose_name="RegExp")

    fallback_redirect = models.BooleanField(
        "Fallback redirect",
        default=False,
        help_text="This redirect is only matched after all other redirects have failed to match.<br>This allows us to define a general 'catch-all' that is only used as a fallback after more specific redirects have been attempted.",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("site"),
                FieldPanel("url"),
                FieldPanel("regular_expression"),
            ],
            heading="Old Path / Redirect From",
        ),
        MultiFieldPanel(
            [
                FieldPanel("hits"),
            ],
            heading="Hit stats",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                PageChooserPanel("redirect_to_page"),
                FieldPanel("redirect_to_url"),
                FieldPanel("permanent"),
                FieldPanel("fallback_redirect"),
            ],
            heading="New Path / Redirect To",
            classname="collapsible",
        ),
    ]

    @property
    def redirect_to(self):
        if self.redirect_to_page:
            return self.redirect_to_page.url
        return self.redirect_to_url

    def __str__(self):
        return f"{self.url} ---> {self.redirect_to}"

    class Meta:
        verbose_name_plural = "page not found redirects"
        ordering = ("-hits",)
