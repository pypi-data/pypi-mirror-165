let date = new Date();
let nav = document.querySelector('nav');
let footer = document.querySelector('footer');
let copy_btn_01 = document.querySelector('#copy_btn_01');
let copy_btn_02 = document.querySelector('#copy_btn_02');
let copy_btn_03 = document.querySelector('#copy_btn_03');
let code_01 = document.getElementById('code_01').textContent;
let code_02 = document.getElementById('code_02').textContent;
let code_03 = document.getElementById('code_03').textContent;

function dark_mode() {
    footer.style.background = 'rgb(15, 15, 15)';
    nav.style.background = 'rgb(15, 15, 15)';
    document.body.style.background = 'rgb(55, 55, 55)';
};

function light_mode() {
    footer.style.background = 'rgb(255, 255, 255)';
    nav.style.background = 'rgb(255, 255, 255)';
    document.body.style.background = 'rgb(255, 255, 255)';
};

if (date.getHours() >= 17) {
    this.dark_mode();
} else {
    this.light_mode();
};

copy_btn_01.addEventListener('click', ()=>{
    navigator.clipboard.writeText(code_01);
});

copy_btn_02.addEventListener('click', ()=>{
    navigator.clipboard.writeText(code_02);
});


copy_btn_03.addEventListener('click', ()=>{
    navigator.clipboard.writeText('import searchgpy\n\n# Initialize the module.\ngoogle_search_engine = searchgpy.GoogleSearchEngine()\n# Search related results to the sentence `Hello Python !` on Google.\ngoogle_search_engine.search_text(\'Hello Python !\', log=True)');
});