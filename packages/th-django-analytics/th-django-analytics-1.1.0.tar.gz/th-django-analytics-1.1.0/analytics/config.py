from decouple import config

PBI_URL = config("PBI_REPORT_URL", default=None)
FIGURE_CHOICES = (
    # visuais customizados
    ("title_box", "Title"),
    ("card_box", "Card Box"),
    # ("area_chart", "Area Chart"),
    # ("mixed_chart_types", "Mixed Chart Types"),
    # visuais charts 
    ("bar_chart", "Bar Chart"),
    ("bubble_chart", "Bubble Chart"),
    ("doughnut_and_pie_charts", "Doughnut and Pie Charts"),
    ("line_chart", "Line Chart"),
    ("polar_area_chart", "Polar Area Chart"),
    ("radar_chart", "Radar Chart"),
    ("scatter_chart", "Scatter Chart"),
)

METHOD_CHOICES = (
    ("post", "POST"),
    ("get", "GET"),
)

QUERY_DEFAULT = """
-- Configuração de filtros dinamicos
-- 1* para consultas sem condições where {{filters}} 
-- 2* em consultas com where  {{and_filters}}

SELECT * FROM analytics_dashboard {{filters}} LIMIT 1000
"""

TITLE_JINJA_TEMPLATE = """
{# SCRIPT PARA INPUT DE DADOS EM UM VISUAL #}
{# descomente o modelo desejado para utilizar #}
{# https://www.chartjs.org/docs/latest/ #}

{#% set color_pallete = "#4fc8eb"|get_gradient_color_pallete("#090751",10) %#}
{# title model #}
{% set config = {"type":"title","data":{"value": "Clientes"}} %}
{{config}}
"""

CARD_JINJA_TEMPLATE = """
{# SCRIPT PARA INPUT DE DADOS EM UM VISUAL #}
{# descomente o modelo desejado para utilizar #}
{# https://www.chartjs.org/docs/latest/ #}

{#% set color_pallete = "#4fc8eb"|get_gradient_color_pallete("#090751",10) %#}
{% set lucro = 1000 %}
{# card model #}
{% set config = {"type":"card","data":{"value": "R$ %.2f"|format(lucro|float) }} %}
{{config}}
"""
DOUGHNUT_JINJA_TEMPLATE = """
{# SCRIPT PARA INPUT DE DADOS EM UM VISUAL #}
{# descomente o modelo desejado para utilizar #}
{# https://www.chartjs.org/docs/latest/ #}

{#% set color_pallete = "#4fc8eb"|get_gradient_color_pallete("#090751",10) %#}

{# doughnut model #}
{% set data = {"labels":["Cliente A","Cliente B","Cliente C"],"datasets":[{"label":"My First Dataset","data":[300,50,100],"backgroundColor":0,"hoverOffset":4}]} %}
{% set config = {"type":"doughnut","data":data}%}
{{config}}
"""
BUBBLE_JINJA_TEMPLATE = """
{# SCRIPT PARA INPUT DE DADOS EM UM VISUAL #}
{# descomente o modelo desejado para utilizar #}
{# https://www.chartjs.org/docs/latest/ #}

{#% set color_pallete = "#4fc8eb"|get_gradient_color_pallete("#090751",10) %#}

{# bubble model #}
{% set data = {"datasets":[{"label":"First Dataset","data":[{"x":20,"y":30,"r":15},{"x":40,"y":10,"r":10}],"backgroundColor":0}]} %}
{% set config = {"type":"bubble","data":data,"options":{}} %}
{{config}}
"""
LINE_JINJA_TEMPLATE = """
{# SCRIPT PARA INPUT DE DADOS EM UM VISUAL #}
{# descomente o modelo desejado para utilizar #}
{# https://www.chartjs.org/docs/latest/ #}

{#% set color_pallete = "#4fc8eb"|get_gradient_color_pallete("#090751",10) %#}

{% set labels = ["January", "February", "March", "April", "May", "June"] %}

{# line model #}
{% set data = {"labels":labels,"datasets":[{"label":"My First Dataset","data":[65,59,80,81,56,55,40],"borderColor":1,"fill":"true","tension":0.1}]} %}
{% set config = {"type":"line","data":data} %}
{{config}}
"""
POLARAREA_JINJA_TEMPLATE = """
{# SCRIPT PARA INPUT DE DADOS EM UM VISUAL #}
{# descomente o modelo desejado para utilizar #}
{# https://www.chartjs.org/docs/latest/ #}

{#% set color_pallete = "#4fc8eb"|get_gradient_color_pallete("#090751",10) %#}

{# polarArea model #}
{% set data = {"labels":["Red","Green","Yellow","Grey","Blue"],"datasets":[{"label":"My First Dataset","data":[11,16,7,3,14],"backgroundColor":1}]} %}
{% set config = {"type":"polarArea","data":data,"options":{}}%}
{{config}}
"""
RADAR_JINJA_TEMPLATE = """
{# SCRIPT PARA INPUT DE DADOS EM UM VISUAL #}
{# descomente o modelo desejado para utilizar #}
{# https://www.chartjs.org/docs/latest/ #}

{#% set color_pallete = "#4fc8eb"|get_gradient_color_pallete("#090751",10) %#}

{# radar model #}
{% set color = [1,2,3,4] %}
{% set data = {"labels":["Eating","Drinking","Sleeping","Designing","Coding","Cycling","Running"],"datasets":[{"label":"My First Dataset","data":[65,59,90,81,56,55,40],"fill":"true","backgroundColor":"rgba(255, 99, 132, 0.2)","borderColor":"colors"[0],"pointBackgroundColor":"colors"[0],"pointBorderColor":"#fff","pointHoverBackgroundColor":"#fff","pointHoverBorderColor":"colors"[0]},{"label":"My Second Dataset","data":[28,48,40,19,96,27,100],"fill":"true","backgroundColor":"rgba(54, 162, 235, 0.2)","borderColor":"colors"[1],"pointBackgroundColor":"colors"[1],"pointBorderColor":"#fff","pointHoverBackgroundColor":"#fff","pointHoverBorderColor":"colors"[1]}]} %}
{% set config = {"type":"radar","data":data,"options":{"elements":{"line":{"borderWidth":3}}}} %}
{{config}}
"""
SCATTER_JINJA_TEMPLATE = """
{# SCRIPT PARA INPUT DE DADOS EM UM VISUAL #}
{# descomente o modelo desejado para utilizar #}
{# https://www.chartjs.org/docs/latest/ #}

{#% set color_pallete = "#4fc8eb"|get_gradient_color_pallete("#090751",10) %#}

{# scatter model #}
{% set data = {"datasets":[{"label":"Scatter Dataset","data":[{"x":-10,"y":0},{"x":0,"y":10},{"x":10,"y":5},{"x":0.5,"y":5.5}],"backgroundColor":1}]}%}
{% set config = {"type":"scatter","data":data,"options":{"scales":{"x":{"type":"linear","position":"bottom"}}}}%}
{{config}}
"""
BAR_JINJA_TEMPLATE = """
{# SCRIPT PARA INPUT DE DADOS EM UM VISUAL #}
{# descomente o modelo desejado para utilizar #}
{# https://www.chartjs.org/docs/latest/ #}

{#% set color_pallete = "#4fc8eb"|get_gradient_color_pallete("#090751",10) %#}

{% set labels = ["January", "February", "March", "April", "May", "June"] %}

{# bar model #}
{% set data = {"labels":labels,"datasets":[{"label":"My First Dataset","data":[65,59,80,81,56,55,40],"backgroundColor":1,"borderColor":1,"borderWidth":1}]} %}
{% set config = {"type":"bar","data":data,"options":{"scales":{"y":{"beginAtZero":"true"}}}}%}
{{config}}
"""
DEFAULT_JINJA_FIGURE_SCRIPT = """
{# SCRIPT PARA INPUT DE DADOS EM UM VISUAL #}
{# descomente o modelo desejado para utilizar #}
{# https://www.chartjs.org/docs/latest/ #}

{#% set color_pallete = "#4fc8eb"|get_gradient_color_pallete("#090751",10) %#}

{% set labels = ["January", "February", "March", "April", "May", "June"] %}

{# card model #}
{% set config = {"type":"card","data":{"value": "R$ 1000.20"}} %}
{{config}}

{# doughnut model #}
{% set data = {"labels":["Cliente A","Cliente B","Cliente C"],"datasets":[{"label":"My First Dataset","data":[300,50,100],"backgroundColor":0,"hoverOffset":4}]} %}
{% set config = {"type":"doughnut","data":data}%}
{{config}}

{# bubble model #}
{% set data = {"datasets":[{"label":"First Dataset","data":[{"x":20,"y":30,"r":15},{"x":40,"y":10,"r":10}],"backgroundColor":0}]} %}
{% set config = {"type":"bubble","data":data,"options":{}} %}
{{config}}

{# line model #}
{% set data = {"labels":labels,"datasets":[{"label":"My First Dataset","data":[65,59,80,81,56,55,40],"borderColor":1,"fill":"true","tension":0.1}]} %}
{% set config = {"type":"line","data":data} %}
{{config}}

{# polarArea model #}
{% set data = {"labels":["Red","Green","Yellow","Grey","Blue"],"datasets":[{"label":"My First Dataset","data":[11,16,7,3,14],"backgroundColor":1}]} %}
{% set config = {"type":"polarArea","data":data,"options":{}}%}
{{config}}

{# radar model #}
{% set color = [1,2,3,4] %}
{% set data = {"labels":["Eating","Drinking","Sleeping","Designing","Coding","Cycling","Running"],"datasets":[{"label":"My First Dataset","data":[65,59,90,81,56,55,40],"fill":"true","backgroundColor":"rgba(255, 99, 132, 0.2)","borderColor":"colors"[0],"pointBackgroundColor":"colors"[0],"pointBorderColor":"#fff","pointHoverBackgroundColor":"#fff","pointHoverBorderColor":"colors"[0]},{"label":"My Second Dataset","data":[28,48,40,19,96,27,100],"fill":"true","backgroundColor":"rgba(54, 162, 235, 0.2)","borderColor":"colors"[1],"pointBackgroundColor":"colors"[1],"pointBorderColor":"#fff","pointHoverBackgroundColor":"#fff","pointHoverBorderColor":"colors"[1]}]} %}
{% set config = {"type":"radar","data":data,"options":{"elements":{"line":{"borderWidth":3}}}} %}
{{config}}

{# scatter model #}
{% set data = {"datasets":[{"label":"Scatter Dataset","data":[{"x":-10,"y":0},{"x":0,"y":10},{"x":10,"y":5},{"x":0.5,"y":5.5}],"backgroundColor":1}]}%}
{% set config = {"type":"scatter","data":data,"options":{"scales":{"x":{"type":"linear","position":"bottom"}}}}%}
{{config}}

{# bar model #}
{% set data = {"labels":labels,"datasets":[{"label":"My First Dataset","data":[65,59,80,81,56,55,40],"backgroundColor":1,"borderColor":1,"borderWidth":1}]} %}
{% set config = {"type":"bar","data":data,"options":{"scales":{"y":{"beginAtZero":"true"}}}}%}
{{config}}
"""
DEFAULT_API_BODY = """
{% set body = {} %}
{{body}}
"""
