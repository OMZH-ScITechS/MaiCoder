////ヘッダーの読み込み
document.addEventListener("DOMContentLoaded", () => {
    headerHTML = `
    <header>
        <a href="/index.html">
            <img src="/img/logo.svg" alt="MaiCoder">
        </a>
        <div>
            <a href="/editor.html">作問エディタ</a>
            <a href="/contests.html">コンテスト</a>
            <a href="/problems.html">問題集</a>
            <div class="border"></div>
            <div class="div">
                <a href="/login/signup.html">新規登録</a>
                <a href="/login/login.html" class="primary">ログイン</a>
            </div>
            <button class="logined" style="display: none; padding: 4px; border: none;" onclick="menu_toggle()">
                <img src="/img/user.svg" alt="user">
                <p></p>
            </button>
            <div class="logined_menu">
                <a href="/">プロフィール</a>
                <a href="" id="logout">ログアウト</a>
            </div>
        </div>
    </header>
`;
    document.body.insertAdjacentHTML("afterbegin", headerHTML);

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

            // Fetch and set the user's profile image
            const userImage = loggedInDiv.querySelector('img');
            userImage.src = `https://api.maicoder.f5.si/users/${payload.sub}/icon`;
        } catch (error) {
            console.error('Failed to decode JWT payload:', error);
        }
    } else {
        loggedInDiv.style.display = 'none';
        loginLinks.style.display = 'flex';
    }

    const logoutLink = document.getElementById('logout');
    logoutLink.addEventListener('click', (event) => {
        event.preventDefault();
        localStorage.removeItem('jwt_token');
        window.location.href = '/';
    });
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