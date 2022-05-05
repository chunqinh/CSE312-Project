// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/homepage_voting/websocket');

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