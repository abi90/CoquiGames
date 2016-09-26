var gzippo = require('gzippo');
var express = require('express');
var app = express();

app.use(express.logger('dev'));
app.use(gzippo.staticGzip("" + __dirname + "/Angular-CoquiGames"));
app.get('*', function(req, res) {
    res.sendfile('./Angular-CoquiGames/index.html'); // load the single view file (angular will handle the page changes on the front-end)
});
app.listen(process.env.PORT || 5000);
