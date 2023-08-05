from contextlib import nullcontext
import json
import logging
from uuid import uuid4
from copy import deepcopy
from requests import Request, Session
from django.db import models
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from analytics.jinja_renderer.jinja_renderer import render_jinja_template
from django.db import connection, connections
from analytics.config import (
    FIGURE_CHOICES,
    METHOD_CHOICES,
    DEFAULT_JINJA_FIGURE_SCRIPT,
    TITLE_JINJA_TEMPLATE,
    CARD_JINJA_TEMPLATE,
    BUBBLE_JINJA_TEMPLATE,
    DOUGHNUT_JINJA_TEMPLATE,
    LINE_JINJA_TEMPLATE,
    POLARAREA_JINJA_TEMPLATE,
    RADAR_JINJA_TEMPLATE,
    SCATTER_JINJA_TEMPLATE,
    BAR_JINJA_TEMPLATE,
    DEFAULT_API_BODY,
    QUERY_DEFAULT,
)
from colorfield.fields import ColorField

log = logging.getLogger("analytics")

class JinjaRender(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4,
                          editable=False, verbose_name="ID")


class Dashboard(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    dashboard_id = models.CharField(
        max_length=100, null=False, blank=False, unique=True, default=""
    )
    name = models.CharField(null=False, unique=True, max_length=100)
    created_date = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
    )
    backgroundColor = ColorField(default='#FFFFFF',)
    dataset = models.OneToOneField(
        to="Dataset",
        related_name="dashboardDataset",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    update_at = models.DateTimeField(
        auto_now_add=False, auto_now=True, null=False, blank=False
    )
    figures = models.ManyToManyField(
        to="Figure",
        blank=True,
        related_name="dashboardFigures",
    )
    apiCall = models.ManyToManyField(
        to="ApiCall",
        blank=True,
        related_name="dashboardApiCAll",
    )
    image = models.CharField(
        max_length=500, default=None, null=True, blank=True
    )
    usersAllowed = models.ManyToManyField(
        to=User,
        blank=True,
        related_name="users_allowed",
        verbose_name="Users Allowed",
    )

    # MANAGERS
    objects = models.Manager()

    def process_query(self, request=None) -> list:
        # responsável por processar as consultas sql de um dashboard
        new_dataset = list()
        try:
            log.info(
                f"[analytics] {self.name} -> Iniciando processamentos de Consultas Sql."
            )
            # buscando as querys do dashboard
            querys = Query.objects.filter(dashboard=self.id)

            # validando se não existem querys
            if not querys:
                log.info(
                    f"[analytics] {self.name} -> Lista vazia. nenhuma query para ser processada."
                )
                return False
            else:
                log.info(
                    f"[analytics] {self.name} -> Busca query, {len(querys)} foram encontradas."
                )
                pass

            for query in querys:
                log.info(
                    f"[analytics] {self.name} -> Processando Query {query.key}."
                )
                #  processando a query
                data = query.run(request=request)
                if request:
                    messages.success(
                        request,
                        f"Consulta Sql {query.key}  processada com sucesso",
                    )
                #  guardando o resultado
                new_dataset.append(data)

            # copiando o dataset ja existente
            tmp: list = deepcopy(self.dataset.data)
            tmp["database"] = new_dataset

            self.dataset.data = tmp
            self.dataset.save()

            log.info(
                f"[analytics] {self.name} -> Novo dataset com consulta via banco de dados gerado."
            )
            pass
        except Exception as exc:
            log.error(
                f"[analytics] {self.name} -> Erro ao processar Consulta Sql {exc}."
            )
            if request:
                messages.error(
                    request,
                    f"Erro ao processar Consulta Sql {self.name} | {exc}",
                )

    def process_apiCall(self, request=None) -> list:
        #  responsável por processar apicalls de um dashboard
        new_dataset = list()
        try:
            log.info(
                f"[analytics] {self.name} -> Iniciando processamentos de Api Calls."
            )

            apiCalls = ApiCall.objects.filter(dashboard=self.id)

            if not apiCalls:
                log.info(
                    f"[analytics] {self.name} -> Lista vazia. nenhuma Api Call para ser processada."
                )
                return False
            else:
                log.info(
                    f"[analytics] {self.name} -> Busca ApiCalls, {len(apiCalls)} foram encontradas."
                )
                pass

            for apiCall in apiCalls:
                log.info(
                    f"[analytics] {self.name} -> Processando Api Call {apiCall}."
                )
                status_code, new_data = apiCall.run(
                    request=request,
                )

                new_dataset.append(
                    {
                        "apiCallId": apiCall.id,
                        "result": new_data,
                        "url": apiCall.url,
                        "status_code": status_code,
                    }
                )

            self.dataset.data = {"apiCalls": new_dataset}
            self.dataset.save()
            log.info(
                f"[analytics] {self.name} -> Novo dataset com consultas via HTTP gerado."
            )
            pass
        except Exception as exc:
            log.error(
                f"[analytics] {self.name} -> Erro ao processar ApiCall {exc}."
            )
            if request:
                messages.error(
                    request,
                    f"Erro ao processar Api Calls {self.name} | {exc}",
                )

    def create_context(self, request) -> dict:
        # buscando as figuras do dashboard
        figures_from_dashboards = Figure.objects.filter(dashboard=self.id)
        # buscando o dataset do dashboard
        dataset_from_dashboard = Dataset.objects.filter(
            dashboard=self.id
        ).first()

        # validando se existe um dataset válido
        if not dataset_from_dashboard:
            context = {
                "error": "Nenhum dataset disponível como fonte de dados"
            }
            return context

        try:
            figures = list()
            for fig in figures_from_dashboards:
                new_figure_context = fig.create_context(
                    dataset=dataset_from_dashboard
                )
                figures.append(new_figure_context)

            context = {
                "dashboardContext": {
                    "dashboardName": self.name,
                    "backgroundColor": self.backgroundColor,
                    "context": figures,
                }
            }

            return context
        except Exception as exc:
            messages.error(
                request,
                f"Erro ao gerar contexto para uma figura {exc}.",
            )
            return dict()

    def save(self, *args, **kwargs):
        dataset, created = Dataset.objects.get_or_create(dashboard=self)
        if created:
            self.dataset = dataset
        return super().save(*args, **kwargs)

    # META CLASS
    class Meta:
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboards"

    # TO STRING METHOD
    def __str__(self):
        return f"{self.name} | {self.dashboard_id}"


class Query(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    key = models.CharField(
        null=False,
        unique=True,
        blank=False,
        max_length=100,
        help_text="Nome do parâmetro que sera adicionado no contexto com o resultado desta query",
    )

    query = models.TextField(
        null=True,
        blank=True,
        default=QUERY_DEFAULT,
    )

    database = models.CharField(
        null=False,
        max_length=100,
        blank=False,
        default="default",
        help_text="Nome de um database conectado ao projeto",
    )

    dashboard = models.ForeignKey(
        to="Dashboard",
        on_delete=models.CASCADE,
        related_name="dashboardQuery",
        verbose_name="dashboard",
        default=None,
    )
    created_date = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
    )
    position = models.PositiveSmallIntegerField(
        "Position",
        null=True,
        help_text="Posição de processamento",
    )
    update_at = models.DateTimeField(
        auto_now_add=False, auto_now=True, null=False, blank=False
    )
    objects = models.Manager()

    @staticmethod
    def dictfetchall(cursor) -> list:
        # https://docs.djangoproject.com/pt-br/4.0/topics/db/sql/
        """Return all rows from a cursor as a dict"""
        columns = [col[0] for col in cursor.description]

        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def validate_query(query: str) -> bool:
        """
        percorre as palavras da query para validar se existe
        algum comando não permitido,
        """
        is_valid = True

        for bad_word in [
            "delete",
            "update",
            "update",
            "alter",
            "DELETE",
            "UPDATE",
            "ALTER",
        ]:
            try:
                if bad_word in query:
                    is_valid = False
            except Exception:
                ...

        if is_valid:
            return True
        else:
            log.warning(
                "[ Query contendo comando não permitido encontrado,"
                + f" ignorando execução da consulta ]\n -> query: {query}"
            )
            return False

    @staticmethod
    def extract_parameters_from_query(query):
        """
        para que o filtro retorne um valor válido, é necessário que a condição na query
        siga restritamente este formato
        {% where | campo | operador | valor %}
        exemplo {% where | status | = | ok %}
        exemplo {% where | response | like | %ok% %}
        """
        qry: str = query
        prms: list = list()

        # validando se existem parametros para serem extraidos
        l: int = len(qry.upper().split("WHERE")) - 1

        for _ in range(0, l):
            try:
                comand: str = (qry.split("{%"))[1].split("%}")[0]
                parameters: list = comand.split("|")
                if len(parameters) == 4:
                    qry = qry.replace(
                        "{%" + comand + "%}",
                        f"{parameters[0]} {parameters[1]} {parameters[2]} %s"
                        if _ == 0
                        else f"{parameters[1]} {parameters[2]} %s",
                    )
                    prms.append((comand, parameters, qry))
                else:
                    raise Exception(
                        f" [ Parametros incorretos para realizar replace ] -> {qry} "
                    )
            except:
                "NENHUM COMANDO ENCONTRADO, IGNORANDO EXTRAÇÃO"

        if prms:
            args = [i[1][3] for i in prms]
            return prms[-1][2], args
        else:
            return False, False

    def run_django_sql(self, string_query, database) -> list:
        """reposável por realizar consultas sql e retornar um contexto"""

        qry = string_query
        query, params = self.extract_parameters_from_query(qry)
        qry = qry if not query else query

        if self.validate_query(qry):
            with connections[database].cursor() as cursor:
                try:
                    f_query = (
                        str(qry)
                        .replace("{{filters}}", " ")
                        .replace("{{and_filters}}", " ")
                    )

                    cursor.execute(
                        f_query, params=params if params else list()
                    )

                    data = self.dictfetchall(cursor)

                    return data
                except Exception as exc:
                    connection._rollback()
                    raise Exception(exc)

    def run(self, request=None):
        try:
            result = self.run_django_sql(self.query, self.database)
            return {self.key: result}
        except Exception as exc:
            if request:
                messages.error(
                    request,
                    f"Consulta Sql {self.key} {self.query} falhou ao ser processada {exc}",
                )
            log.error(
                f"[analytics] {self.dashboard.name} -> Consulta Sql [{self.key}] {self.query} falhou ao ser processada {exc}"
            )
            return {self.key: str(exc)}

    # META CLASS
    class Meta:
        ordering = ["position"]
        verbose_name = "Consulta Sql"
        verbose_name_plural = "Consultas Sql"

    # TO STRING METHOD
    def __str__(self):
        return f"{self.key} "


class ApiCall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    method = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        choices=METHOD_CHOICES,
        help_text="Tipo do método desejado",
        default=METHOD_CHOICES[0][0],
    )
    created_date = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
    )
    body = models.TextField(
        null=True,
        blank=True,
        default=DEFAULT_API_BODY,
        help_text="Template Jinja que gerar um corpo que sera enviado com a requisição",
    )
    url = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        default="http://127.0.0.1:8000/analytics/v1/data",
        unique=False,
        help_text="Fonte de dados desta figura",
    )
    position = models.PositiveSmallIntegerField(
        "Position",
        null=True,
        help_text="Posição de processamento",
    )
    dashboard = models.ForeignKey(
        to="Dashboard",
        on_delete=models.CASCADE,
        related_name="dashboardApiCall",
        verbose_name="dashboard",
        default=None,
    )
    update_at = models.DateTimeField(
        auto_now_add=False, auto_now=True, null=False, blank=False
    )
    objects = models.Manager()

    # META CLASS
    class Meta:
        ordering = ["position"]
        verbose_name = "Consulta HTTP"
        verbose_name_plural = "Consultas HTTP"

    @staticmethod
    def process_response(response, url, request=None):
        if request:
            if response.status_code in [200, 201]:
                messages.success(
                    request,
                    f"Api Call {url} processada com um retorno positivo",
                )
            else:
                messages.warning(
                    request,
                    f"Api Call {url} processada com um retorno {response.status_code} - {response.json()}",
                )
        return response.status_code, response.json()

    def run(self, request=None):
        try:
            session = Session()

            jinja_body = json.loads(
                render_jinja_template(self.body).strip().replace("'", '"')
            )

            if not jinja_body:
                jinja_body = dict()

            req = Request(
                self.method, self.url, data=jinja_body, headers=None
            )
            prepped = req.prepare()
            resp = session.send(prepped)

            log.info(
                f"[analytics] {self.dashboard.name} -> Api Call [{self.method}] {self.url} processada com sucesso {resp.status_code}"
            )

            return self.process_response(
                request=request, response=resp, url=self.url
            )
        except Exception as exc:
            log.error(
                f"[analytics] {self.dashboard.name} -> Erro ao processar Api Call {self.method} {self.url} - status: {exc}."
            )
            return 500, exc

    # TO STRING METHOD
    def __str__(self):
        return f"{self.method} | {self.url}"


class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_date = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
    )
    update_at = models.DateTimeField(
        auto_now_add=False, auto_now=True, null=False, blank=False
    )
    dashboard = models.ForeignKey(
        to=Dashboard,
        on_delete=models.CASCADE,
        related_name="dashboardDataset",
        verbose_name="dashboard",
    )
    data = models.JSONField(
        encoder=DjangoJSONEncoder,
        null=True,
        blank=True,
        default=dict,
        help_text="",
    )
    # MANAGERS
    objects = models.Manager()

    # META CLASS
    class Meta:
        verbose_name = "Dataset"
        verbose_name_plural = "Datasets"

    # TO STRING METHOD
    def __str__(self):
        return f"{self.dashboard} | atualizado em {self.update_at}"


class Figure(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    title = models.CharField(
        max_length=100, null=False, blank=False, default="", unique=True
    )
    description = models.CharField(
        max_length=50, null=False, blank=True, default=""
    )
    type = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        choices=FIGURE_CHOICES,
        help_text="Tipo do gráfico desejado",
        default=FIGURE_CHOICES[0][0],
    )
    dashboard = models.ForeignKey(
        to=Dashboard,
        on_delete=models.CASCADE,
        related_name="dashboardFigures",
        verbose_name="dashboard",
    )
    created_date = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
    )
    eventJinja = models.TextField(
        verbose_name="Event Jinja",
        blank=True,
        help_text="Template Jinja utilizado para tratar o dataset do dashboard",
    )

    position = models.PositiveSmallIntegerField(
        "Position",
        null=True,
        help_text="Posição desta figura em relação aos outros objetos",
    )

    update_at = models.DateTimeField(
        auto_now_add=False, auto_now=True, null=False, blank=False
    )

    # MANAGERS
    objects = models.Manager()

    # META CLASS
    class Meta:
        ordering = ["position"]
        verbose_name = "Visual"
        verbose_name_plural = "Visuais"

    # TO STRING METHOD
    def __str__(self):
        return f"{self.title} | {self.type}"

    def create_context(self, dataset):
        try:
            jinja_template =render_jinja_template(
                        self.eventJinja, {"dataset": dataset.data}
                    ).strip().replace("'", '"')
            return {
                "type": self.type,
                "title": self.title,
                "config": json.loads(
                    jinja_template
                ),
            }
        except Exception as exc:
            try:
                log.error(f"[analytics] Erro ao processar o contexto de um visual {self.type} com o contexto {jinja_template}")
            except:...
            return {"type": self.type, "error": str(exc)}

    def save(self, *args, **kwargs):
        def handler(type: str) -> str:
            if type == "title_box":
                event = TITLE_JINJA_TEMPLATE
            elif type == "card_box":
                event = CARD_JINJA_TEMPLATE
            elif type == "polar_area_chart":
                event = POLARAREA_JINJA_TEMPLATE
            elif type == "bar_chart":
                event = BAR_JINJA_TEMPLATE
            elif type == "bubble_chart":
                event = BUBBLE_JINJA_TEMPLATE
            elif type == "doughnut_and_pie_charts":
                event = DOUGHNUT_JINJA_TEMPLATE
            elif type == "line_chart":
                event = LINE_JINJA_TEMPLATE
            elif type == "radar_chart":
                event = RADAR_JINJA_TEMPLATE
            elif type == "scatter_chart":
                event = SCATTER_JINJA_TEMPLATE
            else:
                event = DEFAULT_JINJA_FIGURE_SCRIPT
            return event

        try:
            if not self.eventJinja:
                log.info(
                    f"[analytics] Salvando um novo EventJinja {self} . Template jinja default selecionado para a figura"
                )
                self.eventJinja = handler(self.type)
            self.full_clean()
            return super().save(*args, **kwargs)
        except Exception as exc:
            log.error(
                f"[analytics] Erro ao escolher template jinja para a figura {self}. \n{exc}"
            )
            return False
