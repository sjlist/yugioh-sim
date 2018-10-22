var mongoose = require('mongoose');

const Schema = mongoose.Schema;
const cardModel = new Schema({
    name: { type: String },
    type: { type: String }
})

module.exports = mongoose.model('Card', cardModel);