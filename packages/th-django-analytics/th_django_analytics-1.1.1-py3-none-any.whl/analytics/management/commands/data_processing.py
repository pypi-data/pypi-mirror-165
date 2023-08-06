from django.core.management.base import BaseCommand
import logging

log = logging.getLogger("analytics")


class Command(BaseCommand):
    help = """Custom command for upload dashboard dataset."""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from analytics.models import Dashboard
        dashboards = Dashboard.objects.all()
        log.info(
            "[analytics] Iniciando processamento dos dados de todos os dashboards disponíveis.")
        try:
            for dash in dashboards:
                dash.process_apiCall()
                dash.process_query()
        except Exception:
            ...
        else:
            log.info(
                "[analytics] Processamento dos dados finalizado com sucesso.")
