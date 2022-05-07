// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');
// Get the modal
var modal = document.getElementById("myModal");
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// var send_message =''
// var received_message=''
// var sender =''
// var receiver =''

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
    // received_message=''
    // send_message=''
    // sender =username['sender']
    // receiver = username['receiver']
    // user.style.color = username['color']
    message=''
    if (username['sender']== username['receiver']){
        user.innerHTML += "<li class='list-item' > <span style ='color:" + username['color']+ "'> " + username['receiver'] +"</span> </li>";
    }else{
        // user.innerHTML += "<li class='list-item' onclick='popup()' > <span style ='color:" + username['color']+ "'> " + username['receiver'] +"<span/> </li>";
        // user.innerHTML += "<li class='list-item' onclick='popup(\''+ username['sender'] + '\')' > <span style ='color:" + username['color']+ "'> " + username['receiver'] +"<span/> </li>";
        user.innerHTML += "<li class='list-item' onclick='popup(`"+ escapeHtml(username['sender']) +"`,`"+ escapeHtml(username['receiver'])+ "`,`"+escapeHtml(message)+"`)' > <span style ='color:" + username['color']+ "'> " + username['receiver'] +"</span> </li>";
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



function popup(sender, receiver, message){
    let popup_sender = document.getElementById('sender')
    popup_sender.innerHTML =sender
    let popup_receiver = document.getElementById('receiver')
    popup_receiver.innerHTML =receiver
    let rece_message = document.getElementById('received_message')
    rece_message.innerHTML = message
    // sender, receiver, message
    modal.style.display = "block";
}

// // When the user clicks the button, open the modal 
// btn.onclick = function() {
//     modal.style.display = "block";
// }

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    console.log("X")
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function escapeHtml(unsafe){
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }


 function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }

  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }