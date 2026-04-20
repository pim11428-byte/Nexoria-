const tg = window.Telegram.WebApp;
tg.expand();

const user = tg.initDataUnsafe.user;

document.getElementById("status").innerText =
    `Привет, ${user.first_name}!`;

document.getElementById("btn-osint").onclick = () => {
    tg.openTelegramLink("https://t.me/YOUR_BOT?start=osint");
};

document.getElementById("btn-sub").onclick = () => {
    tg.openTelegramLink("https://t.me/YOUR_BOT?start=subscription");
};
