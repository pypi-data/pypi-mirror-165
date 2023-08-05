let home_btn = document.getElementById('home_btn');
let credits_btn = document.getElementById('credits_btn');
let install_btn = document.getElementById('install_btn');
let use_btn = document.getElementById('use_btn');

home_btn.addEventListener('click', ()=>{
    window.location = './';
});

credits_btn.addEventListener('click', ()=>{
    window.location = 'https://github.com/Boubajoker/SearchGooglePy/blob/master/ThirdPartyNotice.md';
});

install_btn.addEventListener('click', ()=>{
    window.location = "#install";
});

use_btn.addEventListener('click', ()=>{
    window.location = '#use'
});