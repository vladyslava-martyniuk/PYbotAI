// ===== Елементи DOM =====
const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");
const logoutBtn = document.getElementById("logoutBtn");
const loginBox = document.getElementById("loginBox");
const registerBox = document.getElementById("registerBox");
const greetingDiv = document.getElementById("greeting");

const chatInput = document.getElementById("chatInput");
const sendButton = document.getElementById("sendMsg");
const chatHistoryUser = document.getElementById("chatHistoryUser");

// ===== Відображення форм =====
loginBtn.onclick = () => {
    loginBox.style.display = loginBox.style.display === "none" ? "block" : "none";
    registerBox.style.display = "none";
};
registerBtn.onclick = () => {
    registerBox.style.display = registerBox.style.display === "none" ? "block" : "none";
    loginBox.style.display = "none";
};

// ===== Перевірка наявності увійденого користувача при завантаженні =====
window.addEventListener("load", () => {
    const nickname = localStorage.getItem("userNickname");
    if (nickname) {
        greetingDiv.innerText = `Привіт, ${nickname}!`;
        loginBox.style.display = "none";
        registerBox.style.display = "none";
    }
});

// ===== Реєстрація =====
document.getElementById("doRegister").onclick = async () => {
    const username = document.getElementById("regUsername").value;
    const password = document.getElementById("regPassword").value;
    const resultDiv = document.getElementById("regResult");

    const data = new FormData();
    data.append("username", username);
    data.append("password", password);

    try {
        const res = await fetch("/register", { method: "POST", body: data });
        const json = await res.json();
        if (res.ok) {
            resultDiv.innerText = json.message;
            resultDiv.style.color = "green";
            setTimeout(() => registerBox.style.display = "none", 1500);
        } else {
            resultDiv.innerText = json.message || json.detail || "Помилка";
            resultDiv.style.color = "red";
        }
    } catch (e) {
        resultDiv.innerText = "Помилка сервера";
        resultDiv.style.color = "red";
    }
};

// ===== Логін =====
document.getElementById("doLogin").onclick = async () => {
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;
    const resultDiv = document.getElementById("loginResult");

    const data = new FormData();
    data.append("username", username);
    data.append("password", password);

    try {
        const res = await fetch("/login", { method: "POST", body: data });
        const json = await res.json();
        if (res.ok) {
            resultDiv.innerText = json.message;
            resultDiv.style.color = "green";

            // Зберігаємо локально і показуємо привітання
            localStorage.setItem("userNickname", username);
            greetingDiv.innerText = `Привіт, ${username}!`;

            setTimeout(() => loginBox.style.display = "none", 1500);
        } else {
            resultDiv.innerText = json.detail || json.message || "Помилка";
            resultDiv.style.color = "red";
        }
    } catch (e) {
        resultDiv.innerText = "Помилка сервера";
        resultDiv.style.color = "red";
    }
};

// ===== Вихід =====
logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("userNickname");
    greetingDiv.innerText = "";
    loginBox.style.display = "block";
    registerBox.style.display = "none";
    alert("Ви вийшли з облікового запису.");
});

// ===== Чат: Спільний інпут =====
sendButton.onclick = async () => {
    const message = chatInput.value.trim();
    if (!message) return;

    addUserMessage(message);

    const services = ["openai", "groq", "gemini"];
    for (const service of services) {
        await sendToAI(service, message);
    }

    chatInput.value = "";
};

// ===== Чат: окремі ШІ =====
async function sendSingle(service) {
    const input = document.getElementById(`${service}Input`);
    const message = input.value.trim();
    if (!message) return;

    addUserMessage(`[${service.toUpperCase()}] ${message}`);
    await sendToAI(service, message);

    input.value = "";
}

// ===== Відправка на бекенд і додавання фідбеку =====
async function sendToAI(service, message) {
    const chatDiv = document.getElementById(`${service}Chat`);
    const botDiv = document.createElement("div");
    botDiv.className = "bot-message";
    botDiv.innerText = "⏳ Думає...";
    chatDiv.appendChild(botDiv);

    try {
        const res = await fetch("/send_message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: message, service: service, temperature: 0.7, max_tokens: 150 })
        });
        const json = await res.json();
        botDiv.innerText = json.result || "Помилка ШІ";

        addFeedback(botDiv, service);
    } catch {
        botDiv.innerText = "Помилка сервера";
        addFeedback(botDiv, service);
    }

    chatDiv.scrollTop = chatDiv.scrollHeight;
}

// ===== Фідбек для ШІ =====
function addFeedback(botDiv, service) {
    const feedbackDiv = document.createElement("div");
    feedbackDiv.style.marginTop = "5px";

    const thumbsUp = document.createElement("button");
    thumbsUp.innerText = "👍";
    thumbsUp.onclick = () => sendFeedback(service, botDiv, "like");

    const thumbsDown = document.createElement("button");
    thumbsDown.innerText = "👎";
    thumbsDown.onclick = () => sendFeedback(service, botDiv, "dislike");

    feedbackDiv.appendChild(thumbsUp);
    feedbackDiv.appendChild(thumbsDown);
    botDiv.appendChild(feedbackDiv);
}

async function sendFeedback(service, botDiv, type) {
    const username = localStorage.getItem("userNickname");
    if (!username) { alert("Щоб залишити фідбек, потрібно увійти"); return; }

    try {
        await fetch("/feedback", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ service: service, feedback: type })
        });
        botDiv.querySelectorAll("button").forEach(b => b.disabled = true);
    } catch (e) { alert("Помилка при відправці фідбеку"); }
}

// ===== Додаємо повідомлення користувача =====
function addUserMessage(text) {
    const nickname = localStorage.getItem("userNickname") || "Гість";
    const div = document.createElement("div");
    div.className = "user-message";
    div.innerText = `${nickname}: ${text}`;
    chatHistoryUser.appendChild(div);
}

// ===== Enter для відправки =====
chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendButton.click();
});
