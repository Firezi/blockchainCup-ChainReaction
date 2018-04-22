const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();

const mysql      = require('mysql');
const db = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '',
  database : 'traders'
});
 
db.connect();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(express.static('frontend'));

app.get('/traders', (req, res) => {
  let order = req.query.order;
  console.log(req.query);
  if (order !== 'name' && order !== 'profit' && order !== 'recovery_factor' && order !== 'max_dropdown')
    order = 'profit';
    // order = 'top_position';
  console.log(order);
  db.query(`select * from traders order by ${order} ASC`, (err, data) => {
    if (err) {
      res.status(503);
      res.end();
      console.log(err);
    } else {
      let list = [];
      for (let trader of data) {
        list.push(trader);
      }
      res.status(200);
      res.end(JSON.stringify(list));
    }
  });
});
app.get('/trader', (req, res) => {
  const traderId = req.query.trader;
  if (/*typeof traderId !== 'number'*/false) {
    console.log(traderId);
    res.status(503);
    res.end();
  } else {
    db.query(`select * from traders where id = "${traderId}"`, (err, data) => {
      if (err) {
        res.status(503);
        res.end();
        console.log(err);
      } else {
        const trader = data[0];
        db.query(`select * from profit where trader = "${traderId}"`, (err, data) => {
          if (err) {
            res.status(503);
            res.end();
            console.log(err);
          } else {
            let list = [];
            // console.log(data);
            for (let trader of data) {
              list.push({});
              for (let metric in trader) {
                if (metric !== 'trader_id') {
                  list[list.length - 1][metric] = trader[metric]
                }
              }
            }
            res.status(200);
            trader.results = list;
            res.end(JSON.stringify(trader));
          }
        });
      }
    });
  }
});
app.post('/removeOldData', (req, res) => {
  fs.writeFile(__dirname + '/rowData.bin', '[]', 'utf-8', (err) => {
    if (err) {
      res.status(503);
      console.log(err);
    } else {
      res.status(200);
      res.end();
    }
  });
});

app.post('/rawData', (req, res) => {
  if (req.body === undefined) {
    res.status(503);
    res.end();
  } else {
    let newFileText;
    fs.readFile(__dirname + '/rowData.bin', (err, data) => {
      if (err) {
        newFileText = [];
      } else {
        newFileText = JSON.parse(data);
      }
      newFileText.push(req.body);
      // console.log('---')
      // console.log(newFileText);
      // console.log('---')
      fs.writeFile(__dirname + '/rowData.bin', JSON.stringify(newFileText), 'utf-8', (err) => {
        if (err) {
          res.status(503);
          console.log(err);
        } else {
          res.status(200);
          res.end();
        }
      });
    })
  }
});

app.get('/rawData', (req, res) => {
  fs.readFile(__dirname + '/rowData.bin', (err, data) => {
    if (err) {
      res.status(503);
      console.log(err);
    } else {
      res.status(200);
      res.end(data);
    }
  })
});

const names = [
'Super Trader',
'Mega trader',
'Wow trader',
'Our favourite trader'
];
const descriptions = [
`Название стратегии: СкальперПро <br/>
Стиль торговли: скальпинг <br/>
Рынок: Фортс <br/>
На что опирается: анализ потока ордеров<br/>
Опыт на рынке: 6 лет<br/>
Vk: http://vk.com <br/>
FB: https://www.facebook.com/ <br/>
Whotrades: https://whotrades.com/<br/>
Smartlab: https://smart-lab.ru/ <br/>`,
`Название стратегии: ИнтрадейПро <br/>
Стиль торговли: интрадей <br/>
Рынок: Фондовый <br/>
На что опирается: технический анализ, уровни<br/>
Опыт на рынке: 8 лет<br/>
Vk: http://vk.com <br/>
FB: https://www.facebook.com/ <br/>
Whotrades: https://whotrades.com/<br/>
Smartlab: https://smart-lab.ru/ <br/>`,
`Название стратегии: Уорен Бафет <br/>
Стиль торговли: долгосрок <br/>
Рынок: Фондовый <br/>
На что опирается: технический анализ, фундаментальный анализ<br/>
Опыт на рынке: 10 лет<br/>
Vk: http://vk.com <br/>
FB: https://www.facebook.com/ <br/>
Whotrades: https://whotrades.com/<br/>
Smartlab: https://smart-lab.ru/ <br/>`];
const randomName = () => names[Math.floor(Math.random() * names.length)];
const randomDesciption = () => descriptions[Math.floor(Math.random() * descriptions.length)];

const genDate = timestamp => {
  timestamp *= 1000;
  const date = new Date(timestamp);
  return date.getFullYear() + '-' + date.getDate() + '-' + (1 + date.getMonth()) + ' ' + date.getHours() + ':' + date.getMinutes();
}

app.post('/resultData', (req, res) => {
  if (req.body === undefined && req.body.length > 0) {
    res.status(503);
    res.end();
  } else {
    const trader = req.body[0];
    console.log(trader);

    db.query(`select count(*) from traders where id="${trader.address}"`, (err, data) => {
      if (data[0]['count(*)'] == 0) {
        db.query(`insert into traders values("${req.body[0].address}", "${randomName()}", ${trader.sumprofit}, ${trader.recovery}, ${trader.dd}, ${trader.avrprofit}, ${trader.percentWinning}, ${trader.profFactor}, 0, "${randomDesciption()}", "http://google.com")`);
      } else {
        db.query(`update traders set profit=${trader.sumprofit}, recovery_factor=${trader.recovery}, max_dropdown=${trader.dd}, average_profit_percent=${trader.avrprofit}, percent_winning=${trader.percentWinning}, profit_factor=${trader.profFactor} where id="${trader.address}"`);
      }
    });

    for (let profit of req.body) {
      db.query(`select count(*) from profit where trader="${profit.address}" and profit=${profit.dinamicProfit} and date="${genDate(profit.time)}"`, (err, response) => {
        if (response[0]['count(*)'] === 0) {
          db.query(`insert into profit values("${profit.address}", ${profit.dinamicProfit}, "${genDate(profit.time)}")`);
        }
      });
    }

    // const traders = req.body.traders;
    // db.query('delete from traders');
    // let i = 0;
    // for (let trader of traders) {
    //   db.query(`insert into traders values(${trader.id}, "${trader.name}", ${trader.profit}, ${trader.recovery}, ${trader.dropdown}, ${i}, "${trader.description}", "${trader.url}")`);
    //   i++;
    // }

    // const traders_results = req.body.traders_results;

    // db.query('delete from traders_results');
    // for (let result of traders_results)
    //   db.query(`insert into traders_results values(${result.trader_id}, ${result.recovery_factor}, ${result.payoff_ratio}, ${result.profit_factor}, ${result.max_dropdown}, ${result.average_profit_percent}, ${result.percent_winning}, ${result.profit_per_bar}, "${result.date}")`);
    
    console.log(req.body);
    res.status(200);
    res.end();
  }
});

app.listen(3000);