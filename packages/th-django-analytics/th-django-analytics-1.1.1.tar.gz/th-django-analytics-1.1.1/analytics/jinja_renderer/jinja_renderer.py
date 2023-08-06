import os
import copy
from inspect import getmembers, isfunction

from jinja2.exceptions import TemplateSyntaxError, TemplateAssertionError
from jinja2 import Environment, FileSystemLoader, Undefined, meta

from analytics.jinja_renderer import jinja_filters
from analytics.jinja_renderer import jinja_globals

import logging

logger = logging.getLogger("analytics")


class SilentUndefined(Undefined):
    """
    Class to suppress jinja2 errors and warnings
    """

    def _fail_with_undefined_error(self, *args, **kwargs):
        return "undefined"

    __add__ = (
        __radd__
    ) = (
        __mul__
    ) = (
        __rmul__
    ) = (
        __div__
    ) = (
        __rdiv__
    ) = (
        __truediv__
    ) = (
        __rtruediv__
    ) = (
        __floordiv__
    ) = (
        __rfloordiv__
    ) = (
        __mod__
    ) = (
        __rmod__
    ) = (
        __pos__
    ) = (
        __neg__
    ) = (
        __call__
    ) = (
        __getitem__
    ) = (
        __lt__
    ) = (
        __le__
    ) = (
        __gt__
    ) = (
        __ge__
    ) = (
        __int__
    ) = (
        __float__
    ) = __complex__ = __pow__ = __rpow__ = _fail_with_undefined_error


def create_jinja_env():
    path = os.path.join(
        os.path.dirname(os.path.abspath("__file__")), "app/endpoint/templates"
    )
    env = Environment(
        loader=FileSystemLoader(path),
        extensions=[
            "jinja2_time.TimeExtension",
            "jinja2.ext.loopcontrols",
            "jinja2.ext.do",
        ],
        trim_blocks=True,
    )
    env.undefined(SilentUndefined)
    for name, function in [
        i for i in getmembers(jinja_filters) if isfunction(i[1])
    ]:
        env.filters[name] = function
    for name, function in [
        i for i in getmembers(jinja_globals) if isfunction(i[1])
    ]:
        env.globals[name] = function
    return env


def make_template(string: str):
    env = create_jinja_env()
    # TODO : remove \n\t from template string?
    template = env.from_string(string)
    return template


def render_jinja_template(jinja_template, *args, **kwargs):
    """Intermediate function for jinja rendering to better handle errors
    The errors raised by jinja are very hard to debug, as the traceback has little to no context
    """
    try:
        template = make_template(jinja_template)
    except (TemplateAssertionError, TemplateSyntaxError) as exc:
        logger.error(
            f"Received error [{exc}] while compiling a jinja template"
            f"Could not make the following template [{jinja_template}] with arguments [{args}] and [{kwargs}]"
        )
        raise exc

    try:
        """
        Existe um problema em passar contextos mutáveis para o renderizador jinja, como listas e dicionarios
        O contexto a princípio não deveria ser modificado, mas alguns objetos mais complexos são
        Alguns casos, como o valor de um campo ser um dicionário, permite alterar o valor do contexto via template
        ex:
                context = {"value":{"inner_value":1}}
                template_jinja = '{% do value.update({"inner_value":2}) %}'
                template = make_template(template_jinja)
                r=template.render(**context)
                context == {"value":{"inner_value: 2}}
        Devido a isso, vamos copiar o contexto atual para um novo dicionário, mantendo o contexto original intacto
        Utilizando apenas a cópia na renderização do template
        """
        context = dict(*args, **kwargs)
        context_copy = copy.deepcopy(context)
        result = template.render(**context_copy)
    except Exception as exc:
        logger.error(
            f"Received error [{exc}] while rendering a jinja template"
            # f"Could not render the following template [{jinja_template}] with arguments [{args}] and [{kwargs}]"
        )
        raise exc
    return result


def get_jinja_variables(string: str):
    env = create_jinja_env()
    ast = env.parse(string)
    return list(meta.find_undeclared_variables(ast))
