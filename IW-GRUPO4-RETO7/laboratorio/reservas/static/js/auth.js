function getToken() { 
const params = new URLSearchParams(window.location.search); 
return params.get('token'); 
}

function urlConToken(url) { 
    const token = getToken(); 
    if (!token) return url; 
    if (url.includes('token=')) 
    return url;
    if (url.includes('?')) return url + '&token=' + token; return url + '?token=' + token; 
}

function verificarAuth() { 
const token = getToken(); 
if (!token) { window.location.href = '/login/'; } return token;
}