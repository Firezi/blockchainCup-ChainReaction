  
const genTable = data => {
  $('#result, article').css('opacity', 0);
  setTimeout(() => $('#result, article').css('opacity', 1), 0);

  let elementHtml = 
`
<table>
  <thead>
    <tr>
      <th data-order="name">Трейдер</th>
      <th data-order="profit">Доходность</th>
      <th data-order="recovery_factor">Recovery</th>
      <th data-order="max_dropdown">Максимальная просадка</th>
      <th></th>
    </tr>
  </thead>
  <tbody>`;
  for (let trader of data) {
    elementHtml += 
`<tr>
  <td>${trader.name}</td>
  <td>${trader.profit}</td>
  <td>${trader.recovery_factor}</td>
  <td>${trader.max_dropdown}</td>
  <td class="trader-about-btn waves-effect waves-light btn red" data-trader=${trader.id}>Узнать больше</td>
</tr>`;
  }
  elementHtml += 
`  </tbody>
</table>`;
  $('#result').html(elementHtml);
  $('.trader-about-btn').click(function() {
    $.get(`./trader?trader=${this.dataset.trader}`, (results) => {
      renderTrader(JSON.parse(results));
    });
  });
  $('thead th').click(function() {
    $.get(`./traders?order=${this.dataset.order}`, (traders) => {
      genTable(JSON.parse(traders));
    });
  });
}


const translates = {
  recovery_factor: 'Recovery factor',
  profit_factor: 'Profit factor',
  profit_factor: 'Доходность',
  max_dropdown: 'Максимальная просадка',
  average_profit_percent: 'Средняя доходность',
  percent_winning: 'Percent winning',
  profit_per_bar: 'Прибыль за свечу'
}

const colors = [
  '#d70206',
  '#f05b4f',
  '#f4c63d',
  '#d17905',
  '#453d3f',
  '#59922b',
  '#0544d3'
]


let currentTraderResults = [];
const renderTrader = trader => {
  $('#result, article').css('opacity', 0);
  setTimeout(() => $('#result, article').css('opacity', 1), 0);
  $('#result').html();
  $('article').css('display', 'none');
  let labels = '';
  let i = 0;
  for (let metric in trader.results[0]) {
    if (metric !== 'date') {
       labels += 
       `<label class="filter-checkbox-container">
         <input data-metric=${metric} type="checkbox" class="filled-in red" ${'checked'}>
         <span>
           ${translates[metric] !== undefined ? translates[metric] : metric}
            
         </span>
         <span class="line-label"></span>
      </label>`;
      if (i % 2 != 0) 
        labels += '<br>';
      i++;
    }
  }
  let elementHtml = 
  /*<div id="metrics-filters">
      ${labels}
    </div>*/
  `
  <h2 class="trader-title"><i class="material-icons medium">person</i> ${trader.name}</h2>
  <h5 class="trader-title"><i class="material-icons">account_balance_wallet</i> ${trader.id}</h2>
  <div class="ct-chart ct-perfect-fourth" id="profit-chart"></div>
  <p>Доходность (в рублях)</p>
  <div class="ct-chart ct-perfect-fourth" id="prfoit-prc-chart"></div>
  <p>Относительная доходность (%)</p>
  <div>
    <div class="ct-chart ct-perfect-fourth consts-chart" id="consts-chart-1"></div>
    <div class="ct-chart ct-perfect-fourth consts-chart" id="consts-chart-2"></div>
    <div class="ct-chart ct-perfect-fourth consts-chart" id="consts-chart-3"></div>
    <div class="ct-chart ct-perfect-fourth consts-chart" id="consts-chart-4"></div>
    <div class="ct-chart ct-perfect-fourth consts-chart" id="consts-chart-5"></div>
    <div class="ct-chart ct-perfect-fourth consts-chart" id="consts-chart-6"></div>
  </div>
  <p>Различные показатели трейдера</p>
  <div class="trader-description">
    ${trader.description}
  </div>
  <a href="${trader.url}">
    <div class="trader-contact right btn waves-effect waves-light red">Contact trader now <i class="material-icons right">send</i></div>
  </a>`;
  $('#result').html(elementHtml);
  $('#metrics-filters input').change(function() {
    drowGraphics();
  });
  currentTraderResults = trader.results;
  drowGraphics();
  drowGraphics('#prfoit-prc-chart', 1000);
  drowConsts(trader);
}
const drowConsts = (trader) => {
  let labels = [];
  let series = [];
  const results = trader;
  labels.push(translates['max_dropdown']);
  labels.push(translates['profit_factor']);
  labels.push(translates['percent_winning']);
  labels.push(translates['profit_per_bar']);
  labels.push(translates['recovery_factor']);
  labels.push(translates['average_profit_percent']);
  series.push(trader.max_dropdown); 
  series.push(trader.profit_factor); 
  series.push(trader.percent_winning); 
  series.push(trader.profit_per_bar); 
  series.push(trader.recovery_factor); 
  series.push(trader.average_profit_percent);
  for (let i in series) {
    if (!series[i])
      series[i] = 0;
  }
  for (let i = 1; i <= 6; i++) {
    new Chartist.Bar('#consts-chart-' + i, {
        labels: [labels[i]],
        series: [series[i]]
      }, {
        distributeSeries: true,
        width: '100px',
        height: '500px'
    }); 
  }
}
const drowGraphics = (element='#profit-chart', devider=1) => {
  let graphic = false;
  const results = currentTraderResults; 
  let labels = [];
  let series = [[]];
  for (let result of results) {
    labels.push(result.date);
    series[0].push(result.profit / devider);
    /*let i = 0;
    for (let k in result) {
      if (k === 'date') {
        labels.push(result.date);
      } else {
        if ($(`#metrics-filters input[data-metric=${k}]`).prop('checked')) {
          if (i > 0 && !results[k] && series[i - 1])
            results[k] = series[i - 1];
          if (series[i] === undefined)
            series[i] = [{meta: translates[k] !== undefined ? translates[k] : k,  value: result[k]}];
          else
            series[i].push({meta: translates[k] !== undefined ? translates[k] : k,  value: result[k]});
          i++;
        }
      }
    }*/
  }
  // console.log(labels);
  const data = {
    labels,
    series
  };
  const options = {
    showArea: true,
    // showPoint: false,
    low: 0,
    fullWidth: true,
    plugins: [
      Chartist.plugins.tooltip()
    ]
  };
  if (devider > 1)
    options.lineSmooth = Chartist.Interpolation.step();
  if (!graphic) {
    graphic = new Chartist.Line(element, data, options);
    graphic.on('draw', function(data) {
      if(data.type === 'line' || data.type === 'area' || data.type === 'point') {
        if (data.type !== 'point') {
          data.element.animate({
            d: {
              begin: 500 * data.index,
              dur: 500,
              from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
              to: data.path.clone().stringify(),
              easing: Chartist.Svg.Easing.easeOutQuint
            }
          });
        } else {
          data.element.animate({
            /*y1: {
              begin: 500 * data.index,
              dur: 500,
              from: data.axisY.axisLength,
              to: data.y,
              easing: Chartist.Svg.Easing.easeOutQuint
            }, */
            opacity: {
              begin: 500 * (data.index + 1),
              dur: 500,
              from: 0,
              to: 1,
              easing: Chartist.Svg.Easing.easeOutQuint
            }
          });
        }
      }
      if(data.type === 'line') {
        $($($(`#metrics-filters input:checked`)[data.index]).parent().find('.line-label')).css('background', colors[data.index]);
      }
    });
  } else {
    $('.line-label').css('background', 'white');
    graphic.update(data, options);
  }
}

$.get('./traders', (traders) => {
  genTable(JSON.parse(traders));
});