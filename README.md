# CHESS TOURNAMENT MANAGER #

1.  [Description](#description)
2.  [Use](#use)
    1.  [setup](#setup)
    2.  [player management](#player-management)
    3.  [tournament management](#tournament-management)
    4.  [data visualisation](#data-visualisation)
    5.  [flake8 report](#flake8)

## 1. Description <a name="description"></a> ##

This script has been realized as part of a project of the course
'Application developer - Python' of OpenClassrooms.


The program is a chess tournament manager that allows :
- The creation and management of tournaments with registration in a database.
- Matchmaking is based on the Swiss system.
- Visualization of the list of players and tournaments.

The script is used via a terminal interface. The database is a document oriented database created with TinyDB.

## 2. Use <a name="use"></a> ##

#### SETUP : <a name="setup"></a> ####

First, start by cloning the repository:

```
git clone git@github.com:mariefj/chessTournament.git
```

- Access the project folder
```
cd chessTournament
```

- Create a virtual environment
```
python -m venv env
```

- Enable the virtual environment
```
source env/bin/activate
```

- Install the python dependencies on the virtual environment
```
pip install -r requirements.txt
```

- Start
```
python chess-tournament.py
```

#### PLAYER MANAGEMENT : <a name="player-management"></a> ####

In the principal menu choose option 2 "Gérer les joueurs", 
then you can create a new player or see the list of players sorted alphabetically or by rank.

If you want to update a player's rank : choose option 2 or 3, then 1 "oui" to rank's update question 
and choose the id of the player.

#### TOURNAMENT MANAGEMENT : <a name="tournament-management"></a> ####

To launch a tournament, in the principal menu choose 1 "Lancer un tournoi", 
then you have the choice to create a new tournament or launch an existent tournament.

Once a new tournament was created, you have to add 8 players to begin first round.

At each round the program shows the games to play, then you choose to begin and end the round, 
and report players's scores.

At the end of the tournament, you'll be able to update players'rank.

#### DATA VISUALISATION : <a name="data-visualisation"></a> ####

In the principal menu choose option 3 "Accéder aux données", 
then you can see the list of all players sorted but also with option 3 "Liste des tournois" 
access to all tournament's info, which includes the players, the rounds and the games of a specific tournament.

#### FLAKE-8 REPORT : <a name="flake8"></a> ####

To generate flake-8 reports, the command is :

```
flake8 --format=html --htmldir=flake8_rapport --exclude env/
```

The reports will be generated in the folder : flake-report
