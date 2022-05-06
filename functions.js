// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

function sendVote(vote) {
    socket.send(JSON.stringify({'vote': vote}));
}

function addVote(vote){
    if(vote === "add-vote1"){

    }
    else if(vote === "add-vote2"){

    }
    else if(vote === "add-vote3"){

    }
    else if(vote === "add-vote4"){

    }
    else if(vote === "add-vote5"){

    }
    else{
        console.log("Invalid Vote");
    }
}

socket.onmessage = function (ws_message) {
    const vote = JSON.parse(ws_message.data);
    const voteType = vote.vote;
    addVote(voteType);
}

function get_online_users() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const users = JSON.parse(this.response);
            for (const user of users) {
                addUser(user);
            }
        }
    };
    request.open("GET", "/online_users");
    request.send();
}

function addUser(username) {
    let user = document.getElementById('user');
    // user.style.color = username['color']
    if (username['sender']== username['receiver']){
        user.innerHTML += "<li class='list-item' > <span style ='color:" + username['color']+ "'> " + username['receiver'] +"<span/> </li>";
    }else{
        user.innerHTML += "<a href='/chat="+username['sender']+ "&"+username['receiver']+ "' class='list-item' > <span style ='color:" + username['color']+ "'> " + username['receiver'] +"<span/> </a>";
    }
}

function get_chat_history() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const messages = JSON.parse(this.response);
            for (const message of messages) {
                addMessage(message);
            }
        }
    };
    request.open("GET", "/chat-history");
    request.send();
}

function addMessage(chatMessage) {
    let chat = document.getElementById('chat');
    chat.innerHTML += "<b>" + chatMessage['username'] + "</b>: " + chatMessage["comment"] + "<br/>";
}