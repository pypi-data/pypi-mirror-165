import logging
import nested_admin
from django.contrib import admin, messages
from django.shortcuts import HttpResponseRedirect
from django.utils.html import format_html
from analytics.models import Dashboard, Figure, ApiCall, Dataset, Query, JinjaRender
from analytics.adminUtils import (
    ApiCAllInline,
    DatasetInline,
    FiguresInline,
    DashboardFilter,
    QueryInline,

)


log = logging.getLogger("analytics")


@admin.register(JinjaRender)
class JinjaRenderModelAdmin(admin.ModelAdmin):
    # class Media:
    # css = {
    #     'all': ['lumiaDiagram/css/html.css']
    # }
    # js = ['lumiaDiagram/js/html.js',
    #       'lumiaDiagram/js/joint.js',
    #       'lumiaDiagram/js/joint.shapes.html.js',
    #       'lumiaDiagram/js/graph_function.js']

    model = JinjaRender
    change_list_template = "jinja_render.html"

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        dashboards = Dashboard.objects.filter(usersAllowed=request.user)
        _dashboards = list()
        if dashboards:
            _dashboards = [{"id": str(dashboard.id), "name": dashboard.name}
                           for dashboard in dashboards]

        return super().changelist_view(request, extra_context={"dashboards": _dashboards, })


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    readonly_fields = ("data",)
    list_display = [
        "dashboard",
        "update_at",
    ]
    list_filter = [
        DashboardFilter,
    ]


# @admin.register(Query)
# class QueryAdmin(admin.ModelAdmin):
#     list_filter = [
#         DashboardFilter,
#     ]


# @admin.register(ApiCall)
# class ApiCallAdmin(admin.ModelAdmin):
#     list_filter = [
#         DashboardFilter,
#     ]


# @admin.register(Figure)
# class FigureAdmin(admin.ModelAdmin):
#     list_filter = [DashboardFilter, "type"]
#     code_mirror_fields = [
#         "eventJinja",
#     ]


@admin.register(Dashboard)
class DashboardAdmin(nested_admin.NestedModelAdmin, admin.ModelAdmin):
    list_display = [
        "name",
        "created_date",
        "view",
        "dashboard_id",
    ]
    change_form_template = "dashboard_change_template.html"
    inlines = [ApiCAllInline, QueryInline, FiguresInline]

    # readonly_fields = ("dataset",)
    fieldsets = (
        (
            "INFORMAÇÕES",
            {
                "description": "Informações gerais sobre esta movimentação",
                "fields": (
                    ("name", "dashboard_id",), ("usersAllowed",  "backgroundColor",),
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "FONTE DE DADOS",
            {
                "description": "Configurações Básicas",
                "fields": ("dataset",),
                "classes": ("collapse",),
            },
        ),
    )

    def view(self, obj):
        return format_html(
            f'<a class="button" href="/analytics/{obj.dashboard_id}">ACESSAR</a>&nbsp;',
            None,
        )

    def response_change(self, request, obj):
        dashboard_admin_url = f"/admin/analytics/dashboard/{obj.id}/change/"
        dashboard_url = f"/analytics/{obj.dashboard_id}"
        try:
            if "_processData" in request.POST:
                log.info(
                    f"[analytics] {obj} -> Solicitação de processamento dos dados recebida."
                )
                obj.process_apiCall(request=request)
                obj.process_query(request=request)

                return HttpResponseRedirect(dashboard_admin_url)
            elif "_view" in request.POST:
                return HttpResponseRedirect(dashboard_url)
            else:
                return HttpResponseRedirect(dashboard_admin_url)
        except Exception as exc:
            log.error(
                f"[analytics] {obj} -> Erro ao processar ação em um dashboard {exc}."
            )
            messages.error(
                request,
                f"Erro ao processar ação de dashboard {obj.name} - {exc}",
            )
            return HttpResponseRedirect(dashboard_admin_url)


# from analytics.jinja_renderer.jinja_renderer import render_jinja_template
# template = "{% set options=[]%} {{options}}"
# template = """
# {% set color_pallete = "#4fc8eb"|get_gradient_color_pallete("#090751",10) %}
# {{data}}
# """
# print(render_jinja_template(template, args=[]))
