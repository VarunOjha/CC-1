const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const BOT_IMG = "https://image.flaticon.com/icons/svg/327/327779.svg";
const PERSON_IMG = "https://image.flaticon.com/icons/svg/145/145867.svg";
const BOT_NAME = "BOT";
const PERSON_NAME = "You";

msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";
  console.log(msgText)
  getBotResponse(msgText);
});

function appendMessage(name, img, side, text) {
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

function getBotResponse(message) {
  const delay = message.split(" ").length * 100;

  fetch('https://xu5gmm9tyg.execute-api.us-east-1.amazonaws.com/dev/chatbot', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({BotRequest:[{Message:message}]})
  })
  .then((res)=>{
    res.json().then((responseObject)=>{
      setTimeout(() => {
        if(responseObject.body){
          appendMessage(BOT_NAME, BOT_IMG, "left", responseObject.body);
        } else {
          appendMessage(BOT_NAME, BOT_IMG, "left", "I don't understand that!");
        }
      }, delay);
    }).catch(()=>{
      setTimeout(() => {
        appendMessage(BOT_NAME, BOT_IMG, "left", "I don't understand that!");
      }, delay);
    })
  })
  .catch((a)=>{
    setTimeout(() => {
      appendMessage(BOT_NAME, BOT_IMG, "left", "I don't understand that!");
    }, delay);
  })

}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}
