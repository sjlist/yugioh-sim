# Readme for Database

I'm using a MongoDB set-up. A good reference to get started and find commands is: https://www.tutorialspoint.com/mongodb.

## Set-Up

1. Install mongo
2. Install Node and npm

## Using API

### Set up API

1. cd into cardapi
2. run `npm install`

### Using API

To start, I'm just making a simple webpage entry form with the given fields. Later, I want this to let you browse all the cards and make edits to them. Additionally, this could be one way to construct the decks. 

After the api is installed (as specified above) you should be able to run it with the command `npm start`, then naviage to: localhost:8888/ in your webbrowser of choice. 


## Using DB

I am providing/building an API for card entry and editing, so hopefully you wont need to do too much in the database yourself. To run the database, first run `mongod --dbpath ~/Documents/Projects/yugioh-sim/db`, this points the mongoDB instance at the db directory, where we'll store our relavant data. After this, in a new terminal, run `mongo` (it may be worth using the `--smallfiles` flag since some of the journals produced could be over 100MB and thus make git mad, see links at bottom for more info.) to start the database shell. To sue the cards database, enter `use cards`. From here you can use any command you want, like add, edit, or delete cards. Each card is stored as a document in the Cards database.

### Common Commands

`db.cards.insert({
  "name": "The Agent of Creation - Venus",
  "type": "monster",
  "effects": [
    {
      "location": "m_zone",
      "activation": {
        "deck": {
          "Mystical Shine Ball": 1
        },
        "lifepoints": 500
      },
      "cost": [
        ["lifepoints", -500]
      ],
      "actions": [
        ["special_summon", "Mystical Shine Ball", "OPTION0", "OPTION1"]
      ]
    }
  ]
});`

`db.cards.find()`

`db.cards.find({type: "monster"}).pretty()`

There are also update and delete commands. 

### Comments

I haven't looked into how to properly backup data with git. I don't know if we need all of the files in db or just a few. For now it's probably fine, but one we start to get many more cards, it may be an issue to look at. 

The journal directory records things as they get written to the disk. I'm going to try not tracking it, but if we need it, we can use the `smallfiles` flag `mongo --smallfiles` to change the journal file size from about 100MB (which could make git mad) to about 32MB. 
https://stackoverflow.com/questions/19533019/is-it-safe-to-delete-the-journal-file-of-mongodb
https://docs.mongodb.com/manual/core/journaling/