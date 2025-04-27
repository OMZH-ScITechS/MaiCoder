// Retrieve the JWT token from localStorage
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