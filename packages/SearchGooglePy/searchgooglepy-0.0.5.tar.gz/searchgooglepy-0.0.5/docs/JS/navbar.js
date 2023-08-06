let home_btn = document.getElementById('home_btn');
let use_btn = document.getElementById('use_btn');
let dark_mode_btn = document.getElementById('dark_mode_btn');
let light_mode_btn = document.getElementById('light_mode_btn');

home_btn.addEventListener('click', ()=>{
    window.location = './';
});

credits_btn.addEventListener('click', ()=>{
    window.location = 'https://github.com/Boubajoker/SearchGooglePy/blob/master/ThirdPartyNotice.md';
});

dark_mode_btn.addEventListener('click', ()=>{
    this.dark_mode();
});

light_mode_btn.addEventListener('click', ()=>{
    this.light_mode();
});