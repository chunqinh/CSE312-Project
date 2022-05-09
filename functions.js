// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/homepage_voting/websocket');

function sendVote(vote) {
    socket.send(JSON.stringify({'vote': vote}));
}

function addVote(vote, voteName, voteCount){
    const voteRequest = new XMLHttpRequest();
    voteRequest.open("POST", "/add-vote")
    voteRequest.send(vote + "," + voteName + "," + voteCount)
    if(vote === "add-vote1"){
        const votes = document.getElementById("vote1")
        votes.innerHTML =
            `<label id="vote1" className="homepagewvoting-creator-text08">` + voteName + ": " + voteCount + "</label>"
    }
    else if(vote === "add-vote2"){
        const votes = document.getElementById("vote2")
        votes.innerHTML =
            `<label id="vote2" className="homepagewvoting-creator-text07">` + voteName + ": " + voteCount + "</label>"
    }
    else if(vote === "add-vote3"){
        const votes = document.getElementById("vote3")
        votes.innerHTML =
            `<label id="vote3" className="homepagewvoting-creator-text05">` + voteName + ": " + voteCount + "</label>"
    }
    else if(vote === "add-vote4"){
        const votes = document.getElementById("vote4")
        votes.innerHTML =
            `<label id="vote4" className="homepagewvoting-creator-text06">` + voteName + ": " + voteCount + "</label>"
    }
    else if(vote === "add-vote5"){
        const votes = document.getElementById("vote5")
        votes.innerHTML =
            `<label id="vote5" className="homepagewvoting-creator-text04">` + voteName + ": " + voteCount + "</label>"
    }
    else{
        console.log("Invalid Vote")
    }
}

socket.onmessage = function (ws_message) {
    const vote = JSON.parse(ws_message.data);
    const voteType = vote.vote;
    const voteName = vote.voteName;
    const voteCount = vote.voteCount;
    addVote(voteType, voteName, voteCount);
}