var express = require('express');
var mongoose = require('mongoose');
var bodyParser = require('body-parser');
var cors = require('cors')
var morgan = require('morgan');

var cardRouter = require('./Routes/cardRouter');

const app = express();
const port = process.env.PORT || 3001;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(morgan('dev'));

//Enable all requests
app.use(cors());

const db = mongoose.connect('mongodb://localhost:27017/cards');

app.use('/api/cards', cardRouter);

// routes go here
app.listen(port, () => {
    console.log(`http://localhost:${port}`)
})
