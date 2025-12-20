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
const chatHistory = document.getElementById("chatHistory");
const sendButton = document.getElementById("sendMsg");
const chatInput = document.getElementById("chatInput");

sendButton.onclick = async () => {
    const message = chatInput.value.trim();
    if (!message) return;

    const nickname = localStorage.getItem("userNickname") || "Гість";

    // Відображаємо повідомлення користувача
    const userDiv = document.createElement("div");
    userDiv.className = "user-message";
    userDiv.innerText = `${nickname}: ${message}`;
    chatHistory.appendChild(userDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    // Читаємо обраний сервіс ШІ
    const serviceRadios = document.getElementsByName("aiService");
    let selectedService = "openai"; // дефолт
    for (const radio of serviceRadios) {
        if (radio.checked) selectedService = radio.value;
    }

    // Відправляємо запит на бекенд
    const data = {
        query: message,
        service: selectedService,
        temperature: 0.7,
        max_tokens: 150
    };

    try {
        const res = await fetch("/send_message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        const json = await res.json();

        const botDiv = document.createElement("div");
        botDiv.className = "bot-message";
        if (json.result) {
            botDiv.innerText = `PyBotAi [${selectedService.toUpperCase()}]: ${json.result}`;
        } else {
            botDiv.innerText = `PyBotAi [${selectedService.toUpperCase()}]: Помилка ШІ`;
        }
        chatHistory.appendChild(botDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    } catch (e) {
        const botDiv = document.createElement("div");
        botDiv.className = "bot-message";
        botDiv.innerText = `PyBotAi [${selectedService.toUpperCase()}]: Помилка сервера`;
        chatHistory.appendChild(botDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    chatInput.value = "";
};

// Відправка по Enter
chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendButton.click();
});
