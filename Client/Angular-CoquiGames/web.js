var express = require('express');

var path = require('path');
var bodyParser = require('body-parser');
var app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(express.static(path.join(__dirname, '/')));

/* GET home page. */
app.get('/', function(req, res, next) {
    //Path to your main file
    res.status(200).sendFile(path.join(__dirname+'../index.html'));
});

module.exports = app;