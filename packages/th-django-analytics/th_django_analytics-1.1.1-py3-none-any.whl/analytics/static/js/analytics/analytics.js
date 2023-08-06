// ACTIONS
class ExpandChartAction {
  constructor() {
    window.expand_chart = this.expand_chart;
    window.collapse_chart = this.collapse_chart;
  }

  scroll_to(element, interval = 100) {
    setTimeout(() => {
      $([document.documentElement, document.body]).animate(
        {
          scrollTop: $(element).offset().top - 50,
        },
        interval
      );
    }, interval);
  }

  expand_chart = (context) => {
    var parent = $(context).parent().get(0) || null;
    var parent1 = $(parent).children().get(1) || null;
    var parent2 = $(parent).children().get(2) || null;
    $(parent2).remove();

    var parent3 = document.createElement("div");
    parent3.setAttribute("class", "collapse-chart");
    parent3.setAttribute("onClick", "collapse_chart(this)");

    $(parent1).fadeOut(100);
    parent.append(parent3);
    $(parent).animate(
      {
        width: "91.6vw",
        minHeight: "80vh",
      },
      600,
      () => {
        $(parent1).fadeIn();
        setTimeout(() => this.scroll_to(parent), 200);
      }
    );
  };

  collapse_chart = (context) => {
    var parent = $(context).parent().get(0) || null;
    var parent1 = $(parent).children().get(1) || null;
    var parent2 = $(parent).children().get(2) || null;
    $(parent2).remove();

    var parent3 = document.createElement("div");
    parent3.setAttribute("class", "expand-chart");
    parent3.setAttribute("onClick", "expand_chart(this)");

    parent.append(parent3);

    $(parent1).fadeOut(100);
    parent.append(parent3);
    $(parent).animate(
      {
        width: "45.9%",
        minHeight: "550px",
      },
      600,
      () => {
        $(parent1).fadeIn();
        setTimeout(() => this.scroll_to(parent), 200);
      }
    );
  };
}

// FIGURES
class AnalyticsFigures {
  get_available_charts() {
    return [
      "chart",
      "bar",
      "bubble",
      "doughnut",
      "pie",
      "line",
      "polarArea",
      "radar",
      "scatter",
    ];
  }

  get_available_cards() {
    return ["card"];
  }

  get_available_titles() {
    return ["title"];
  }

  get_error_html_template(
    context = null,
    error = null,
    available_cards = this.get_available_cards(),
    available_charts = this.get_available_charts()
  ) {
    switch (true) {
      case available_cards.includes(context):
        return (
          `<div class="card-box hover" style="opacity: 0.5; border: 2px solid rgba(255, 0, 0, 0.253); "><img src="https://img.icons8.com/stickers/100/000000/error.png" style="width: 80px;" /><span  style="font-size:auto !important;  margin:10px 50px !important; text-align: center;">` +
          context +
          " - " +
          error +
          `</span></div>`
        );
      case available_charts.includes(context):
        return (
          `<div class="chart-box hover" style="opacity: 0.5; border: 2px solid rgba(255, 0, 0, 0.253); display: flex; align-items: center; justify-content: center;"><img src="https://img.icons8.com/stickers/100/000000/error.png" style="width: 80px;" /><span  style="font-size:auto !important; margin:10px 50px !important; text-align: center;">` +
          context +
          " - " +
          error +
          `</span></div>`
        );
      default:
        return (
          `<div class="chart-box hover" style="opacity: 0.5;box-shadow:none;  display: flex; align-items: center; justify-content: center;"><img src="https://img.icons8.com/stickers/100/000000/error.png" style="width: 80px; margin-bottom:20px;" /><span  style="font-size:auto !important; margin:10px 50px !important; text-align: center;">Ops\n, estamos com alguns problemas por aqui...<br/>` +
          context +
          " - " +
          error +
          `</span></div>`
        );
    }
  }

  get_html_template(
    id,
    title,
    context,
    available_cards = this.get_available_cards(),
    available_charts = this.get_available_charts(),
    available_titles = this.get_available_titles()
  ) {
    // responsável por criar um template html para um visual
    //
    // @param id: id do canvas que deve ser reservado para o gráfico
    // @param title: representa o tipo de gráfico a ser gerado.
    // @param context: caso o tipo do visual seja um card, acessamos o
    //                 contexto para buscar o valor a ser renderizado no visal.
    //                 guarda o contexto da imagem, contendo todas
    //                 as informações do objeto.
    //
    // @return: HTML template - str;

    // validações
    if (context.type == "card") {
      if (typeof context.data.value == "undefined") {
        return this.get_error_html_template("card", "Contexto inválido");
      }
    }
    // gerando o template de acordo com o tipo
    var template;
    var obj_class;

    switch (true) {
      case available_charts.includes(context.type):
        obj_class = "chart-box";
        template =
          '<div class="' +
          obj_class +
          " hover draggable " +
          id +
          '"><div class="chart-header"><h1 class="header-text">' +
          title +
          '</h1></div><canvas id="' +
          id +
          '" ></canvas>' +
          '<div class="expand-chart" onClick="expand_chart(this)" ></div>' +
          "</div>";
        break;
      case available_cards.includes(context.type):
        obj_class = "card-box";
        template =
          '<div class="' +
          obj_class +
          " hover draggable " +
          id +
          '"><h1 class="l-text">' +
          context.data.value +
          '</h1><span class="p-text">' +
          title +
          "</span></div>";
        break;
      case available_titles.includes(context.type):
        obj_class = "title-box title-hover";
        template =
          '<div class="title-box title-hover ' +
          id +
          '"><h1 class="title-text">' +
          context.data.value +
          '</h1><span class="title-description-text m-text">' +
          title +
          "</span></div>";
        break;
      default:
        var error = "Tipo de objeto inválido " + context.type;
        template = this.get_error_html_template(null, error);
        break;
    }

    return template;
  }

  build_figure_context(value, index) {
    // responsável por criar um contexto padronizado para as figuras a serem renderizadas
    //
    // @param value: contexto de uma figura, contendo os seus dados e informações de configuração
    // @param index: representa a posição da figura em relação aos outros objetos.
    //               utilizamos este dado para gerar um id unico para cada figura
    //
    // @return: {id,template,type,config,};
    var figure = {
      id: null,
      template: null,
      type: null,
      config: null,
    };

    try {
      var figureType = value.type;
      var figureTypeMacro = value.type.includes("card") ? "card" : "chart";
      var figureId = figureType + "-" + index;
      var figureConfig = value.config;
      var figureTitle = value.title;

      // validando se o visual foi renderizado corretamente no backend
      // caso tenha algum erro declarado no contexto
      // já renderizamos o template de erro
      if (value.error) {
        var error_msg = "From backend " + value.error;
        figure["type"] = value.type;
        figure["template"] = this.get_error_html_template(
          figureTypeMacro,
          error_msg
        );
        return figure;
      }

      // preenchendo os valores do contexto
      figure["id"] = figureId;
      figure["config"] = figureConfig;
      figure["type"] = figureType;
      figure["title"] = figureTitle;
      figure["template"] = this.get_html_template(
        figureId,
        figureTitle,
        figureConfig
      );
    } catch (exception) {
      figure["type"] = value.type;
      figure["template"] = this.get_error_html_template(
        figureTypeMacro,
        exception
      );
    }
    return figure;
  }

  build_chart(id, type, config) {
    // responsável por criar um gráfico utilizando a biblioteca charts
    // https://www.chartjs.org/
    //
    // @param id: id do canvas que esta reservado para o gráfico
    // @param type: representa o tipo de gráfico a ser gerado.
    // @param config: configurações + dados a serem renderizados no gráfico.
    //
    // @return: bool;
    try {
      var elemt = document.getElementById(id);
      // [!!elemt] validando se existe um objeto canvas no html para incluirmos o dashboard
      // [type != "card_box"] validando se o tipo do gŕafico é um card_box, pois este tipo não é criado aqui
      // [!!config] validando se existem configurações a serem processadas
      if (!!elemt && type != "card_box" && !!config) new Chart(elemt, config);
      return true;
    } catch (exception) {
      console.error(
        "[analytics] " +
          "erro ao criar gráfico do tipo:" +
          type +
          " id:" +
          id +
          " erro:" +
          exception
      );
      return false;
    }
  }
}

// CORE
class AnalyticsCore {
  constructor(config = DASHBOARD_CONTEXT) {
    this.figures = new AnalyticsFigures();
    this.dashboard_config = this.validate(config);
    this.dashboard_backgroundColor = config.backgroundColor;
  }

  validate(config = this.dashboard_config) {
    // responsável por validar as configurações de um dashboard
    //
    // @param config: contem todos os dados necessários para o processamento do dashboard
    //
    // @return: config válidado;
    if (
      typeof config.dashboardName == "undefined" ||
      typeof config.context == "undefined"
    ) {
      $("myDashboard").append(
        this.get_error_html_template(null, "Contexto inváldo")
      );
      throw new Error("Contexto inváldo ");
    }
    return config;
  }

  process(dashboard = this.dashboard_config) {
    // processa o contexto de um dashboard a partir de parametros e configurações passadas anteriormente
    //
    // @param config: contem todos os dados necessários para o processamento do dashboard
    //
    // @return: list, contendo um contexto pronto para ser renderizado;
    var processed_context = [];
    dashboard.context.forEach((figure, index) => {
      let new_fig_context = this.figures.build_figure_context(figure, index);
      processed_context.push(new_fig_context);
    });
    return processed_context;
  }

  render(
    context,
    backgroundColor = this.dashboard_backgroundColor,
    interval = 400
  ) {
    // responsável por adicionar um contexto criado ao html
    // e então renderizar os gráficos gerados e guardados dentro do contexto
    //
    // @param context: contem todos os elementos já tratados que devem ser renderizados na página
    // @param style: pode ser utilizado para passar estilos dinamicos para o dashboard
    // @param interval: representa o delay entre adicionar o template html e criar os dashboards com charts.js
    //
    // utilizamos o metodo de interval pois notamos um comportamento estranho por parte do charts.js
    // basicamente, fazendo o processo de criar os gráficos com charts logo após adicinar o canvas
    // no template html resultava em um bug, onde o gráfico não era renderizado (acusando que o canvas não existia)
    //
    // @return: HTML template - str;
    var containerObj = document.createElement("div");
    containerObj.setAttribute("class", "container");

    // set dashboard style
    if (backgroundColor) {
      var bkgColorCss = "background-color: " + backgroundColor + " !important;";
      containerObj.setAttribute("style", bkgColorCss);
    }

    // hide container to build the dashboard and show later
    $("myDashboard").toggle();

    context.forEach((element, index) => {
      // declarando os parâmetros
      var id = element.id;
      var type = element.type;
      var config = element.config;
      var template = element.template;
      // adicionando os containers dos graficos
      containerObj.innerHTML += template;
      $("myDashboard").append(containerObj);
      setTimeout(() => this.figures.build_chart(id, type, config), interval * (index*.5));
    });

    setTimeout(() => $("myDashboard").fadeIn("slow", "linear"), interval);

    return true;
  }

  run() {
    let processed_context = this.process();
    let is_loaded = this.render(processed_context);

    //  load dashboard actions
    new ExpandChartAction();

    // new TouchInput();

    if (is_loaded)
      console.info("[analytics] dashboard renderizado com sucesso 🙂");
  }
}

$(document).ready(function () {
  var dashboard = new AnalyticsCore();
  dashboard.run();
});
