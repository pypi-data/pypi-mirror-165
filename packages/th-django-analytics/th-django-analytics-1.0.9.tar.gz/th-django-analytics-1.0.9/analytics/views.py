from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from analytics.models import Dashboard, Dataset
from django.http import JsonResponse


class AnalyticView:
    @login_required(login_url="/admin/login/?next=/admin/")
    def dashboard(request, dashId=None):
        # buscando pelo dashboard passado como parâmetro
        if dashId:
            dash_from_user = Dashboard.objects.filter(
                usersAllowed=request.user, dashboard_id=str(dashId)
            ).first()
        else:
            # caso não exista o dashboard com o id buscado
            # renderizamos o primeiro dashboard disponível do usuário
            dash_from_user = Dashboard.objects.filter(
                usersAllowed=request.user
            ).first()

        #  caso o usuário não tenha permissão para acessar nenhum dashboard
        #  ele é redirecionado para a página admin do django
        if not dash_from_user:
            messages.warning(
                request,
                f"Dashboard {dashId} não encontrado",
            )
            return redirect("/admin/analytics/dashboard/")

        #  criando um contexto para enviar ao frontend
        #  contendo os gráficos e seus dados
        context = dash_from_user.create_context(request=request)

        return render(
            request=request, context=context, template_name="analytics.html"
        )
import json 

class JinjaView:
    @login_required(login_url="/admin/login/?next=/admin/")
    def render(request,*args, **kwargs):
        my_json = request.body.decode('utf8').replace("'", '"')

        # Load the JSON to a Python list & dump it back out as formatted JSON
        data = json.loads(my_json)

        dashId = data["dashId"] or None
        jinjaText = data["jinjaText"] or None
        
        try:
            from analytics.jinja_renderer.jinja_renderer import render_jinja_template

            dashboard = Dashboard.objects.filter(id=dashId).first()
            dataset = Dataset.objects.filter(dashboard=dashboard).first()

            if not dataset:
                dataset = list()
                
            response = render_jinja_template(jinjaText, dataset.data)
            
            return JsonResponse({"response": response})
        except Exception as exc:
            return JsonResponse({"response": f"Erro ao renderizar jinja template: {exc}"})
