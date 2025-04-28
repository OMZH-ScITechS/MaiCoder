////ヘッダーの読み込み
document.addEventListener("DOMContentLoaded", () => {
    headerHTML = `
    <header>
        <a href="/web/html/index.html">
            <img src="/web/html/img/logo.svg" alt="MaiCoder">
        </a>
        <div>
            <a href="/web/html/editor.html">作問エディタ</a>
            <a href="/web/html/contests.html">コンテスト</a>
            <a href="/web/html/problems.html">問題集</a>
            <div class="border"></div>
            <div class="div">
                <a href="/web/html/login/signup.html">新規登録</a>
                <a href="/web/html/login/login.html" class="primary">ログイン</a>
            </div>
            <button class="logined" style="display: none; padding: 4px; border: none;" onclick="menu_toggle()">
                <img src="/web/html/img/user.svg" alt="user">
                <p></p>
            </button>
            <div class="logined_menu">
                <a href="/web/html/">プロフィール</a>
                <a href="">ログアウト</a>
            </div>
        </div>
    </header>
`;
    if (location.toString().includes("127.0.0.1")) { //開発環境
        document.body.insertAdjacentHTML("afterbegin", headerHTML);
    } else {
        document.body.insertAdjacentHTML("afterbegin", headerHTML.replace("/web/html",""));
    }

    // Retrieve the JWT token from localStorage
    const token = localStorage.getItem('jwt_token');
    // Update the header to reflect the user's login status
    const header = document.querySelector('header');
    const loggedInDiv = header.querySelector('.logined');
    const loginLinks = header.querySelector('.div');

    if (token) {
        try {
            const payloadBase64 = token.split('.')[1];
            const payloadJson = atob(payloadBase64);
            const payload = JSON.parse(payloadJson);

            loggedInDiv.style.display = 'flex';
            loggedInDiv.querySelector('p').textContent = payload.sub || 'User';
            loginLinks.style.display = 'none';
        } catch (error) {
            console.error('Failed to decode JWT payload:', error);
        }
    } else {
        loggedInDiv.style.display = 'none';
        loginLinks.style.display = 'flex';
    }
});

function menu_toggle() {
    const menu = document.querySelector('.logined_menu');
    menu.style.display = menu.style.display === 'none' || menu.style.display === '' ? 'flex' : 'none';

    if (menu.style.display === 'flex') {
        document.addEventListener('click', closeMenuOnClickOutside);
    }
}

function closeMenuOnClickOutside(event) {
    const menu = document.querySelector('.logined_menu');
    const button = document.querySelector('.logined');
    if (!menu.contains(event.target) && !button.contains(event.target)) {
        menu.style.display = 'none';
        document.removeEventListener('click', closeMenuOnClickOutside);
    }
}