// =================== Елементи ===================
const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");
const logoutBtn = document.getElementById("logoutBtn");
const loginBox = document.getElementById("loginBox");
const registerBox = document.getElementById("registerBox");
const greetingDiv = document.getElementById("greeting");
const chatInput = document.getElementById("chatInput");
const sendButton = document.getElementById("sendMsg");
const chatHistoryUser = document.getElementById("chatHistoryUser");

// =================== Показ/сховування форм ===================
loginBtn.onclick = () => loginBox.style.display = loginBox.style.display === "none" ? "block" : "none";
registerBtn.onclick = () => registerBox.style.display = registerBox.style.display === "none" ? "block" : "none";

// =================== Перевірка при завантаженні ===================
window.addEventListener("load", () => {
    const nickname = localStorage.getItem("userNickname");
    if (nickname) {
        greetingDiv.innerText = `Привіт, ${nickname}!`;
        loginBox.style.display = "none";
        registerBox.style.display = "none";
    }
});

// =================== Реєстрація ===================
document.getElementById("doRegister").onclick = async () => {
    const username = document.getElementById("regUsername").value.trim();
    const password = document.getElementById("regPassword").value.trim();
    const email = document.getElementById("regEmail").value.trim();
    const ageValue = document.getElementById("regAge").value;
    const age = ageValue ? parseInt(ageValue) : null;

    const resultDiv = document.getElementById("regResult");

    // ❗ Вік більше НЕ обовʼязковий
    if (!username || !password || !email) {
        resultDiv.innerText = "Будь ласка, заповніть логін, пароль та email";
        resultDiv.style.color = "red";
        return;
    }

    if (age !== null && age <= 0) {
        resultDiv.innerText = "Вік має бути додатнім числом";
        resultDiv.style.color = "red";
        return;
    }

    const data = new FormData();
    data.append("username", username);
    data.append("password", password);
    data.append("email", email);

    // ➕ додаємо age ТІЛЬКИ якщо він введений
    if (age !== null) {
        data.append("age", age);
    }

    try {
        const res = await fetch("/register", { method: "POST", body: data });
        const json = await res.json();

        if (res.ok) {
            resultDiv.innerText = json.message;
            resultDiv.style.color = "green";

            setTimeout(async () => {
                try {
                    const usersRes = await fetch("/users");
                    const users = await usersRes.json();
                    const userExists = users.some(u => u.username === username);

                    if (userExists) {
                        alert(`Користувача ${username} успішно створено! ✅`);
                        registerBox.style.display = "none";
                        localStorage.setItem("userNickname", username);
                        greetingDiv.innerText = `Привіт, ${username}!`;
                    } else {
                        alert(`Користувача ${username} не знайдено ❌`);
                    }
                } catch (e) {
                    console.log("Помилка перевірки users:", e);
                }
            }, 500);

        } else {
            resultDiv.innerText = json.message || json.detail || "Помилка";
            resultDiv.style.color = "red";
        }
    } catch (e) {
        resultDiv.innerText = "Помилка сервера";
        resultDiv.style.color = "red";
    }
};


// =================== Логін ===================
document.getElementById("doLogin").onclick = async () => {
    const username = document.getElementById("loginUsername").value.trim();
    const password = document.getElementById("loginPassword").value.trim();
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

// =================== Вихід ===================
logoutBtn.addEventListener("click", async () => {
    localStorage.removeItem("userNickname");
    greetingDiv.innerText = "";
    loginBox.style.display = "block";
    registerBox.style.display = "none";
    alert("Ви вийшли з облікового запису.");

    try {
        await fetch("/logout", { method: "POST" });
    } catch(e) {
        console.log("Помилка при logout:", e);
    }
});

// =================== Чат ===================
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

async function sendSingle(service) {
    const input = document.getElementById(`${service}Input`);
    const modelSelect = document.getElementById(`${service}Model`);
    const model = modelSelect.value;
    const message = input.value.trim();
    if (!message) return;

    addUserMessage(`[${service.toUpperCase()}] ${message}`);
    await sendToAI(service, message, model);

    input.value = "";
}

async function sendToAI(service, message, model) {
    const chatDiv = document.getElementById(`${service}Chat`);
    const botDiv = document.createElement("div");
    botDiv.className = "bot-message";
    botDiv.innerText = "⏳ Думає...";
    chatDiv.appendChild(botDiv);

    try {
        const res = await fetch("/send_message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                query: message,
                service: service,
                model: model
            })
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

// =================== Фідбек ===================
function addFeedback(botDiv, service) {
    const feedbackDiv = document.createElement("div");
    feedbackDiv.style.margin = "5px";

    const thumbsUp = document.createElement("button");
    thumbsUp.innerText = "👍";
    thumbsUp.style.marginRight = "5px";
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
    if (!username) {
        alert("Щоб залишити фідбек, потрібно увійти");
        return;
    }

    try {
        await fetch("/review", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ service: service, score: type === "like" ? 5 : 1 })
        });
        botDiv.querySelectorAll("button").forEach(b => b.disabled = true);
        const msgDiv = document.createElement("div");
        msgDiv.style.fontStyle = "italic";
        msgDiv.style.color = "green";
        msgDiv.innerText = "Ваш відгук зараховано ✅";
        botDiv.appendChild(msgDiv);
    } catch (e) {
        alert("Помилка при відправці фідбеку");
    }
}

// =================== Повідомлення користувача ===================
function addUserMessage(text) {
    const nickname = localStorage.getItem("userNickname") || "Гість";
    const div = document.createElement("div");
    div.className = "user-message";
    div.innerText = `${nickname}: ${text}`;
    chatHistoryUser.appendChild(div);
}

// Відправка по Enter для спільного інпуту
chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendButton.click();
});
