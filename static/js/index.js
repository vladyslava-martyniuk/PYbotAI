document.addEventListener("DOMContentLoaded", () => {
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

    // =================== Показ / сховування форм ===================
    loginBtn.onclick = () => loginBox.style.display = loginBox.style.display === "none" ? "block" : "none";
    registerBtn.onclick = () => registerBox.style.display = registerBox.style.display === "none" ? "block" : "none";

    // =================== Перевірка при завантаженні ===================
    const nickname = localStorage.getItem("userNickname");
    if (nickname) {
        greetingDiv.innerText = `Привіт, ${nickname}!`;
        loginBox.style.display = "none";
        registerBox.style.display = "none";
    }

    // =================== Реєстрація ===================
    document.getElementById("doRegister").onclick = async () => {
        const username = document.getElementById("regUsername")?.value.trim();
        const password = document.getElementById("regPassword")?.value.trim();
        const email = document.getElementById("regEmail")?.value.trim();
        const ageValue = document.getElementById("regAge")?.value;
        const age = ageValue ? parseInt(ageValue) : null;
        const resultDiv = document.getElementById("regResult");

        if (!username || !password || !email) {
            resultDiv.innerText = "Заповніть логін, пароль та email";
            resultDiv.style.color = "red";
            return;
        }

        const payload = { username, password, email };
        if (age !== null && age > 0) payload.age = age;

        try {
            const res = await fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const json = await res.json().catch(() => ({}));
            resultDiv.innerText = json.message || "Готово";
            resultDiv.style.color = res.ok ? "green" : "red";

            if (res.ok) {
                localStorage.setItem("userNickname", username);
                greetingDiv.innerText = `Привіт, ${username}!`;
                registerBox.style.display = "none";
            }
        } catch {
            resultDiv.innerText = "Помилка сервера";
            resultDiv.style.color = "red";
        }
    };

    // =================== Логін ===================
    document.getElementById("doLogin").onclick = async () => {
        const username = document.getElementById("loginUsername")?.value.trim();
        const password = document.getElementById("loginPassword")?.value.trim();
        const resultDiv = document.getElementById("loginResult");

        if (!username || !password) {
            resultDiv.innerText = "Введіть логін і пароль";
            resultDiv.style.color = "red";
            return;
        }

        try {
            const res = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            if (res.ok) {
                localStorage.setItem("userNickname", username);
                greetingDiv.innerText = `Привіт, ${username}!`;
                loginBox.style.display = "none";
                resultDiv.innerText = "Успішний вхід ✅";
                resultDiv.style.color = "green";
            } else {
                resultDiv.innerText = "Помилка логіну";
                resultDiv.style.color = "red";
            }
        } catch {
            resultDiv.innerText = "Помилка сервера";
            resultDiv.style.color = "red";
        }
    };

    // =================== Вихід ===================
    logoutBtn.onclick = async () => {
        localStorage.removeItem("userNickname");
        greetingDiv.innerText = "";
        loginBox.style.display = "block";
        registerBox.style.display = "none";
        await fetch("/logout").catch(() => {});
    };

    // =================== Чат ===================
    sendButton.onclick = async () => {
        const message = chatInput.value.trim();
        if (!message) return;

        addUserMessage(message);

        for (const service of ["openai", "gemini"]) {
            await sendToAI(service, message);
        }

        chatInput.value = "";
    };

    window.sendSingle = async function(service) {
        const input = document.getElementById(`${service}Input`);
        if (!input) return;
        const message = input.value.trim();
        if (!message) return;

        addUserMessage(`[${service.toUpperCase()}] ${message}`);
        await sendToAI(service, message);

        input.value = "";
    };

    async function sendToAI(service, message) {
        const chatDiv = document.getElementById(`${service}Chat`);
        if (!chatDiv) return;

        const botDiv = document.createElement("div");
        botDiv.className = "bot-message";
        botDiv.innerText = "⏳ Думає...";
        chatDiv.appendChild(botDiv);

        try {
            const res = await fetch("/send_message", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: message, service })
            });

            const json = await res.json();
            botDiv.innerText =
                typeof json.result === "string"
                    ? json.result
                    : JSON.stringify(json.result, null, 2);

            // ✅ Фідбеки повернуті
            addFeedback(botDiv, service);

        } catch {
            botDiv.innerText = "Помилка сервера";
            addFeedback(botDiv, service);
        }

        chatDiv.scrollTop = chatDiv.scrollHeight;
    }

    // =================== Повідомлення користувача ===================
    function addUserMessage(text) {
        const nickname = localStorage.getItem("userNickname") || "Гість";
        const div = document.createElement("div");
        div.className = "user-message";
        div.innerText = `${nickname}: ${text}`;
        chatHistoryUser.appendChild(div);
        chatHistoryUser.scrollTop = chatHistoryUser.scrollHeight;
    }

    // =================== Фідбеки ===================
    function addFeedback(botDiv, service) {
        const feedbackDiv = document.createElement("div");
        feedbackDiv.className = "feedback";
        feedbackDiv.style.marginTop = "5px";
        feedbackDiv.style.fontSize = "12px";
        feedbackDiv.style.color = "gray";

        const thumbsUp = document.createElement("button");
        thumbsUp.innerText = "👍";
        thumbsUp.style.marginRight = "5px";

        const thumbsDown = document.createElement("button");
        thumbsDown.innerText = "👎";

        thumbsUp.onclick = () => {
            thumbsUp.style.backgroundColor = "lightgreen";
            thumbsDown.style.backgroundColor = "";
        };

        thumbsDown.onclick = () => {
            thumbsDown.style.backgroundColor = "salmon";
            thumbsUp.style.backgroundColor = "";
        };

        feedbackDiv.appendChild(thumbsUp);
        feedbackDiv.appendChild(thumbsDown);
        botDiv.appendChild(feedbackDiv);
    }

    // =================== Надсилання по Enter ===================
    chatInput.addEventListener("keypress", e => {
        if (e.key === "Enter") sendButton.click();
    });
});
