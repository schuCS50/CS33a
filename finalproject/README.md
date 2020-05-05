# Final Project, CS33a
### Spencer Chu, Git: schuCS50

## Project: Games Online
This project's goal was to enable users to play games online. Proposal specifics below:
* **Good Outcome**: A good outcome will be allowing users to log in and play one game asynchronously.
* **Better Outcome**: A better outcome will allow users to play 2-3 different games and allow them to be played live.
* **Best Outcome**: The best outcome would allow users to play 4+ games and allow users to implement their own rules for games.

## Outcome Summary
In this project I was able to implement one game (Tic Tac Toe) that can be played synchronously.
### Requirements
* Utilizes Django
* App is Mobile Responsive
* This is the README
* requirements.txt file included
### Thoughts on Outcome
Overall I am very pleased with the outcome of the project. I would have liked to be able to implement more than one game (and as the appname suggests, a card game), but learning how WebSockets and Django Channels work together took a bit longer than I anticipated. Despite that, I would not change the decision to go that route because I learned a lot about how those two components work. 
### Functionality
* The user can register, log in, and log out
* On the homepage, the user can see all games that have been created
* On a user page (their own or another user's) you can see that user's games
* A user can create a new game with any other user
* Once in the game, the users can synchronously play the game together
* Once a winner has been established, the game and page are updated
### Chat WebSocket Example (Directly from [Django Channels Tutorial](https://channels.readthedocs.io/en/latest/tutorial/index.html))
As part of this project I had to learn how to use websockets to enable the syncrhonous nature of the application. The WebSocket framework along with Django Channels channel_layers allowed me to push updates between the users (or spectators) who were viewing a given game. As part of that, I went through a tutorial that showed how to use channel_layers by implementing a chatroom server. I have kept that example in the application to demonstrate the learning process from that tutorial, but I do not take credit for the design of that piece of the application.
#### Files from Tutorial
* chat.html
* room.html
* ChatConsumer in consumers.py
* chat and room views in views.py
* url paths for chat and room in urls.py

## Primary Files and Details
### Python
* **cards/admin.py:** Enable DB management from Admin panel
* **cards/consumers.py:** WebSocket Consumers (primarily TicTacToeConsumer)
* **cards/models.py:** Django database setup (User and TicTacToe game objects)
* **cards/routing.py:** Routing logic for WebSocket request
* **cards/urls.py:** URL routing logic for HTTP requests
* **cards/views.py:** All view functions to handle HTTP requests
* **games/routing.py:** Point settings at cards/routing.py
* **games/settings.py:** Add settings for Django Channels & ASGI settings
* **games/urls.py:** Point url management at cards/urls.py
### Javascript
* **tictactoe.js:** JS to handle gameplay (both in terms of HTTP and WebSocket connections) 
### HTML
* **chat.html:** Example file from Django Channels tutorial
* **index.html:** Page used to render both home page and user pages
* **layout.html:** Extended template (repurposed from previous project)
* **login.html:** Login page (repurposed from previous project)
* **newgame.html:** Page with form for new game
* **register.html:** Register page (repurposed from previous project)
* **room.html:** Example file from Django Channels tutorial
* **tictactoe.html:** Shell page for gameplay
### CSS
* **styles.css:** Minor CSS style additions to bootstrap primary

Note: App Requires [Django Channels](https://channels.readthedocs.io/en/latest/installation.html)