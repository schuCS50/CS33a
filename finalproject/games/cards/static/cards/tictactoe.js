document.addEventListener('DOMContentLoaded', function() {
    load_game();

    //Get required information from page
    const gameId = document.querySelector('#game-id').innerHTML;
    const isPlayer = document.querySelector('#is-player').innerHTML;
    const user = document.querySelector('#username').innerHTML;
    const token = Cookies.get('csrftoken');
    
    //Open WebSocket
    const gameSocket = new WebSocket(
        'ws://'
        + window.location.host
        +'/ws/tictactoe/'
        + gameId
        + '/'
    );

    //Get all remaining buttons
    const btns = document.getElementsByClassName('space-btn');

    //If the user is not a player in the game disable the buttons
    if (isPlayer != "True") {
        for (var i = 0; i < btns.length; i++) {
            btns[i].disabled = true;
        }
    }

    //Add EventListeners to buttons to put the move and send to WebSocket
    for (var i = 0; i < btns.length; i++) {
        const id = btns[i].id
        btns[i].addEventListener('click', function() {
            
            //PUT the move to the DB
            fetch(`/game/tictactoe/game/${gameId}`, {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': token
                },
                body: JSON.stringify({
                    location: id,
                    user: user
                })
            })
            .then(response => {
                //Send the move to the channel after DB action completes
                gameSocket.send(JSON.stringify({
                    'location': id,
                    'user': user
                }));
                console.log(response);
            });
        });
    }

    //If Websocket closes alert user
    gameSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
        alert("Game disconnected, please reload page");
    };

    //When we receive a websocket message, update page to reflect
    gameSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const btn = document.querySelector(`#${data['location']}`);
        const parent = btn.parentElement;
        btn.remove();
        parent.innerHTML = data['user'];
        won = check_win(data['user']);

        //If the move is a winning move, update
        if (won) {
            won_clear(data['user']);
            
            //Update DB
            fetch(`/game/tictactoe/game/${gameId}`, {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': token
                },
                body: JSON.stringify({
                    won: true,
                    user: data['user']
                })
            })
            .then(response => {
                console.log(response);
            });
        }
    }


});

//Function to clear all remaining buttons if winning move
function won_clear(user) {
    const table = document.querySelector('table');
    const div = table.parentElement;
    const btns = document.getElementsByClassName('space-btn');
    const len = btns.length;
    for (var i = 0; i < len; i++) {
        const element = btns[0].parentElement;
        btns[0].remove();
        element.innerHTML = '-';
    }
    const h1 = document.createElement('h1');
    h1.innerHTML = `${user} wins`;
    div.append(h1);
}

//Function to check if the move is a winning move
function check_win(user) {
    //Get all spaces
    const tds = document.getElementsByClassName('space');
    var win = [];

    //Add all of the current user's spaces to the array
    for (var i = 0; i < tds.length; i++) {
        const id = tds[i].id;
        if (user === tds[i].innerHTML) {
            win.push(parseInt(id));
        }
    }

    //Winning combinations
    const winners = [
        [1,2,3],
        [4,5,6],
        [7,8,9],
        [1,4,7],
        [2,5,8],
        [3,6,9],
        [1,5,9],
        [3,5,7]
    ];

    //check if a winning option
    for (var i = 0; i < winners.length; i++) {
        const won = winners[i].every(val => win.includes(val));
        if (won) {
            return won;
        }
    }
}

//Load the game on pageload
function load_game() {
    const gameTable = document.querySelector('#game');
    const gameId = document.querySelector('#game-id').innerHTML;
    //Generate table
    for (var i = 0; i < 3; i++) {
        const row = document.createElement('tr');
        gameTable.append(row);
        for (var j = 0; j < 3; j++) {
            const td = document.createElement('td');
            const btn = document.createElement('button');

            td.className = 'space';
            td.id = `${(3 * i) + j + 1}`;
            btn.className = 'space-btn btn btn-sm btn-outline-primary';
            btn.id = `btn-${(3 * i) + j + 1}`;
            btn.innerHTML = '_';

            td.append(btn);
            row.append(td);
        }
    }

    //Get game state from DB
    fetch(`/game/tictactoe/game/${gameId}`)
    .then(response => {
        console.log(response);
        return response.json();
    })
    .then(game => {
        cells = game['cells'];
        for (var i = 0; i < cells.length; i++) {
            if (cells[i]) {
                const btn = document.querySelector(`#btn-${i+1}`);
                const parent = btn.parentElement;
                btn.remove();
                parent.innerHTML = cells[i];
            }
        }
        if (game['winner']) {
            won_clear(game['winner']);
        }
    });
}