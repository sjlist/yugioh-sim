import React from 'react';
import 'whatwg-fetch';

class App extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			cards: []
		};
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

	render() {
		return (
			<div className="App">
				<CardList cards={this.state.cards} />
			</div>
		);
	}
}

class CardList extends React.Component {
	render() {
		console.log(this.props.cards);
		return (
			<div className="CardList">
				<h2>
					Cards: 
				</h2>
				<ul>
					{
						this.props.cards.map(card => <li key={card._id}> { card.name } </li>)
					}
				</ul>
			</div>
		);
	}
}

export default App;
