// =================== Логін/Реєстрація ===================
const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");
const loginBox = document.getElementById("loginBox");
const registerBox = document.getElementById("registerBox");

loginBtn.onclick = () => loginBox.style.display = loginBox.style.display === "none" ? "block" : "none";
registerBtn.onclick = () => registerBox.style.display = registerBox.style.display === "none" ? "block" : "none";

// Реєстрація
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

// Логін
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
            localStorage.setItem("userNickname", username);
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

// =================== Чат ===================
const chatInput = document.getElementById("chatInput");
const sendButton = document.getElementById("sendMsg");
const chatHistoryUser = document.getElementById("chatHistoryUser");

// Надсилання повідомлення
sendButton.onclick = async () => {
    const message = chatInput.value.trim();
    if (!message) return;

    const nickname = localStorage.getItem("userNickname") || "Гість";

    // Відображаємо повідомлення користувача
    const userDiv = document.createElement("div");
    userDiv.className = "user-message";
    userDiv.innerText = `${nickname}: ${message}`;
    chatHistoryUser.appendChild(userDiv);

    // Список сервісів
    const services = ["openai", "groq", "gemini"];

    for (const service of services) {
        const chatDiv = document.getElementById(`${service}Chat`);
        const botDiv = document.createElement("div");
        botDiv.className = "bot-message";
        botDiv.innerText = `⏳ ${service.toUpperCase()} думає...`;
        chatDiv.appendChild(botDiv);
        chatDiv.scrollTop = chatDiv.scrollHeight;

        // Відправляємо на бекенд
        const data = { query: message, service: service, temperature: 0.7, max_tokens: 150 };
        try {
            const res = await fetch("/send_message", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            const json = await res.json();
            botDiv.innerText = json.result ? `PyBotAi: ${json.result}` : "Помилка ШІ";
        } catch (e) {
            botDiv.innerText = "Помилка сервера";
        }

        chatDiv.scrollTop = chatDiv.scrollHeight;
    }

    chatInput.value = "";
};

// Відправка по Enter
chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendButton.click();
});
