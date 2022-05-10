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
            let user = document.getElementById('user');
            user.innerHTML='';
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
    
    // message=''
    if (username['sender']== username['receiver']){
        user.innerHTML += "<li class='list-item' > <span style ='color:" + username['color']+ "'> " + username['receiver'] +"</span> </li>";
    }else{
        // user.innerHTML += "<li class='list-item' onclick='popup()' > <span style ='color:" + username['color']+ "'> " + username['receiver'] +"<span/> </li>";
        // user.innerHTML += "<li class='list-item' onclick='popup(\''+ username['sender'] + '\')' > <span style ='color:" + username['color']+ "'> " + username['receiver'] +"<span/> </li>";
        user.innerHTML += "<li class='list-item' onclick='onclick_popup(`"+ escapeHtml(username['sender']) +"`,`"+ escapeHtml(username['receiver'])+ "`,`"+username['chat_history']+"`)' > <span style ='color:" + username['color']+ "'> " + username['receiver'] +"</span> </li>";
    }
}


function addMessage(chatMessage) {
    let chat = document.getElementById('chat_history');
    console.log(chatMessage);
    // chat.innerHTML += "<b>" + chatMessage['sender'] + "</b>: " + chatMessage["message"] + "</br>";
    // + "<br/>"
    chat.innerHTML += "<p><b>"+chatMessage['sender'] +"</b>: "  + chatMessage["message"] + "</p></br>";
}

function sendMessage() {
    const chatBox = document.getElementById("send_message");
    const message = chatBox.value;
    const sender = document.getElementById("sender").textContent;
    const receiver = document.getElementById("receiver").textContent;
    chatBox.value = "";
    // const send_message = document.getElementById("show_send_message");
    const send_message = document.getElementById('chat_history');
    send_message.innerHTML += "<p><b>"+sender +"</b>: "  + message + "</p></br>";
    // "<b>" + sender + "</b>: " + message + "<br/>";
    // send_message.textContent += sender +": "+message;
    chatBox.focus();
    if (message !== "") {
        // setInterval(request,1000)
        const request = new XMLHttpRequest();
        
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                console.log(this.response)
                // const messages = JSON.parse(this.response);
                // for (const message of messages) {
                //     addMessage(message);
                // }
            }
        };
        request.open("POST", "/direct-message");
        let data = {'sender':sender,'receiver':receiver,'message':message};
        request.send(JSON.stringify(data));
        
    }
}

function fetchMessage(){
    
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const messages = JSON.parse(this.response);
            console.log(messages)
            if (messages['chat_history'] !=''){
                sent_popup(messages['sender'],messages['receiver'],messages['chat_history']);
            }
            // for (const message of messages) {
            //     addMessage(message);
            // }
        }
    };
    request.open("GET", "/get-message");
    request.send();
}



function onclick_popup(sender, receiver, messages){
    console.log(sender)
    console.log(receiver)
    console.log(messages)
    let popup_sender = document.getElementById('sender');
    popup_sender.innerHTML =sender;
    // popup_sender.innerHTML =receiver;
    let popup_receiver = document.getElementById('receiver');
    popup_receiver.innerHTML =receiver;
    // popup_receiver.innerHTML =sender;
    let rece_message = document.getElementById('chat_history')
    rece_message.textContent = '';
    
    const mess =JSON.parse(messages)
    // console.log(mess)
    for (const message of mess) {
        addMessage(message);
    }
    
    // rece_message.innerHTML = message
    // sender, receiver, message
    modal.style.display = "block";
}

function sent_popup(sender, receiver, messages){
    console.log(sender)
    console.log(receiver)
    console.log(messages)
    let popup_sender = document.getElementById('sender');
    // popup_sender.innerHTML =sender;
    popup_sender.innerHTML =receiver;
    let popup_receiver = document.getElementById('receiver');
    // popup_receiver.innerHTML =receiver;
    popup_receiver.innerHTML =sender;
    let rece_message = document.getElementById('chat_history')
    rece_message.textContent = '';
    
    const mess =JSON.parse(messages)
    // console.log(mess)
    for (const message of mess) {
        addMessage(message);
    }
    
    // rece_message.innerHTML = message
    // sender, receiver, message
    modal.style.display = "block";
}

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

function welcome() {

    fetchMessage();
    setInterval(fetchMessage,1000);
    get_online_users();
    setInterval(get_online_users,1000);


}