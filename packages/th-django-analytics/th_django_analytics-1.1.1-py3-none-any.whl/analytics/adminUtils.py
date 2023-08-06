import nested_admin
from django.contrib import admin
from analytics.models import Dashboard, Dataset, Figure, ApiCall, Query
from codemirror2.widgets import CodeMirrorEditor


class CodeMirrorAdmin:
    """
    Admin class for replacing TextArea widgets with CodeMirror for specified fields
    Based on https://pypi.org/project/django-codemirror2/

    code_mirror_options : Options can be configured from https://codemirror.net/doc/manual.html#config
    code_mirror_fields  : Specified fields to change the widget format
    """

    code_mirror_options = {"mode": "jinja2", "lineNumbers": True}
    code_mirror_fields = []

    def get_form(self, request, obj=None, **kwargs):
        kwargs.setdefault("widgets", {})
        for field in self.code_mirror_fields:
            kwargs["widgets"].update(
                {field: CodeMirrorEditor(options=self.code_mirror_options)}
            )
        return super().get_form(request, obj, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        kwargs.setdefault("widgets", {})
        for field in self.code_mirror_fields:
            kwargs["widgets"].update(
                {field: CodeMirrorEditor(options=self.code_mirror_options)}
            )
        return super().get_formset(request, obj, **kwargs)


class DashboardFilter(admin.SimpleListFilter):
    title = "Dashboard"
    parameter_name = "Dashboard"
    default_value = None

    def lookups(self, request, model_admin):
        options = []
        dashboards = Dashboard.objects.all()
        for dash in dashboards:
            options.append((str(dash.id), str(dash)))
        return options

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(dashboard=self.value())
        return queryset

    def value(self):
        value = super(DashboardFilter, self).value()
        return value


class DatasetInline(
    nested_admin.NestedTabularInline,
):
    model = Dataset
    classes = ["collapse"]
    extra = 0
    fieldsets = (
        (
            "DATASET",
            {
                "description": "Dados que alimentam o dashboard",
                "fields": ("data",),
            },
        ),
    )


class QueryInline(
    CodeMirrorAdmin,
    nested_admin.NestedStackedInline,
):
    model = Query
    classes = ["collapse"]
    sortable_field_name = "position"
    extra = 0
    # code_mirror_fields = [
    #     "query",
    # ]

    fieldsets = (
        (
            "CONSULTA",
            {
                "description": "Requisições sql que serão realizadas nas atualizações do dashboard",
                "fields": (
                    (
                        "key",
                        "database",
                        "query",
                        "position",
                    ),
                ),
            },
        ),
    )


class ApiCAllInline(
    CodeMirrorAdmin,
    nested_admin.NestedStackedInline,
):
    model = ApiCall
    classes = ["collapse"]
    sortable_field_name = "position"
    extra = 0
    code_mirror_fields = [
        "body",
    ]

    fieldsets = (
        (
            "REQUISIÇÃO",
            {
                "description": "Requisições que serão realizadas nas atualizações do dashboard",
                "fields": (
                    (
                        "url",
                        "method",
                    ),
                    (
                        "body",
                        "position",
                    ),
                ),
            },
        ),
    )


class FiguresInline(
    CodeMirrorAdmin,
    nested_admin.NestedStackedInline,
):
    model = Figure
    classes = ["collapse"]
    sortable_field_name = "position"
    extra = 0
    code_mirror_fields = [
        "eventJinja",
    ]

    fieldsets = (
        (
            "OBJETO",
            {
                "description": None,
                "fields": (
                    (
                        "title",
                        "type",
                        "position",
                    ),
                    ("eventJinja"),
                ),
            },
        ),
    )
