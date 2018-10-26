var mongoose = require('mongoose');

const Schema = mongoose.Schema;
const cardModel = new Schema({
	name: { type: String, unique: true },
	type: { type: String },
/*
	effects: [{
		location: String,
		activation: { },
		cost: { type: Array, 'deafult': [{}]},
		actions: { type: Array, 'deafult': [[]]}
	}]
*/
})
// https://stackoverflow.com/questions/19695058/how-to-define-object-in-array-in-mongoose-schema-correctly-with-2d-geo-index
// https://mongoosejs.com/docs/guide.html

module.exports = mongoose.model('Card', cardModel);