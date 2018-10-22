var express = require('express');
var Card = require('../Models/cardModel');

const cardRouter = express.Router();

cardRouter.route('/')
    .get((req, res) => {
        Card.find({}, (err, card) => {
            res.json(card)
        })  
    })
    .post((req, res) => {
    	let card = new Card(req.body);
    	card.save()
    	res.status(201).send(card)
    })

// Middleware to find card before opperations
cardRouter.use('/:cardName', (req, res, next) => {
	Card.findById(req.params.cardName, (err, card) => {
		if (err) {
			res.status(500).send(err)
		}
		else {
			req.card = card;
			next()
		}
	})
})

// See and modify a specific card by name
// Later I might do this by _id after getting all initially
cardRouter.route('/:cardName')
    .get((req, res) => {
    	res.json(req.card)
    })
    .put((req, res) => {
    	req.card.type = req.body.type;
		req.card.save()
		res.json(req.card)
    })
    .patch((req, res) => {
		if (req.body._id) {
			delete req.body._id;
		}

		for (let attribute in req.body) {
			req.card[attribute] = req.body[attribute];
		}
		req.card.save()
		res.json(req.card)
    })
    .delete((req, res) => {
		req.card.remove(err => {
			if (err) {
				res.status(500).send(err)
			}
			else {
				res.status(204).send("card removed")
			}
		})
    })

module.exports = cardRouter;
