import React from 'react';
import alasql from 'alasql';
import 'whatwg-fetch';


class App extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			cards: [],
			currCard: ""
		};

		this.updateCards = this.updateCards.bind(this);
		this.updateCurrCard = this.updateCurrCard.bind(this);
	}

	componentDidMount() {
		fetch('/api/cards', {
			method: 'GET'
		})
		.then(data => data.json())
		.then(res => {
			//console.log(res);
			this.setState({ cards: res });
		})
	}

	updateCards(newCards) {
		this.setState({
			cards: newCards
		})
	}

	updateCurrCard(newid) {
		this.setState({ currCard: newid })
	}

	render() {
		return (
			<div className="App">
				<CardList cards={this.state.cards} handleCurrCardChange={this.updateCurrCard} />
				<ActiveCard cards={this.state.cards} currCard={this.state.currCard} handleCardsChange={this.updateCards} />
			</div>
		);
	}
}


class ActiveCard extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			activeCard: {
				name: "",
				type: "",
				effects: []
			},
			task: "Enter"
		};

		this.handleSubmit = this.handleSubmit.bind(this);
		this.handleActiveCardChange = this.handleActiveCardChange.bind(this);
	}

	componentDidUpdate(prevProps) {
		if (prevProps.currCard !== this.props.currCard) {
			const card = alasql("SELECT * FROM ? WHERE _id = ?", [this.props.cards, this.props.currCard]);
			// console.log("alasql active card:", card);
			this.setState({ activeCard: card[0] });
		}
	}

	handleSubmit(event) {
		event.preventDefault();

		console.log("Submitted Form, task:", this.state.task)
	}

	handleActiveCardChange (event) {
		// Works if modifying just an element of the state
		// this.setState({ [event.target.name]: event.target.value });

		// Need to be ugly to modify nested value (copy, then assign, then set)
		// Not too bad given size of object copying 
		let activeCard = Object.assign({}, this.state.activeCard);
		activeCard[event.target.name] = event.target.value;

		this.setState({ activeCard: activeCard });
	}

	render() {
		return(
			<div className="ActiveCard" style={{float: "right", width: "50%"}}>
				Active card: { JSON.stringify(this.state.activeCard) }

				<br />

				<h2> Info: </h2> <br />

				<form onSubmit={this.handleSubmit}>
					<label> Name:
						<input name="name" type="text" value={this.state.activeCard.name} onChange={this.handleActiveCardChange} />
					</label> 
					<label> Type:
						<input name="type" type="text" value={this.state.activeCard.type} onChange={this.handleActiveCardChange} />
					</label> 

					<input type="submit" value="Submit" />
				</form>
			</div>
		);
	}
}


class CardList extends React.Component {
	typeToColor(cardType) {
		var color = "";

		switch (cardType) {
			case "monster": 
				color = "orange";
				break;
			case "spell":
				color = "green";
				break;
			case "trap":
				color = "purple";
				break;
			default:
				color = "red";
				break;
		}

		return color;
	}

	render() {
		return (
			<div className="CardList" style={{float: "left", width: "50%"}}>
				<h2>
					Cards: 
				</h2>
				{
					this.props.cards.map(card => {
						return(
							<div key={card._id} onClick={() => this.props.handleCurrCardChange(card._id)} style={{color: this.typeToColor(card.type)}}>
								{card.name}
							</div>
						);
					})
				}
			</div>
		);
	}
}

export default App;
