let base_url = `${document.location.origin}${document.location.pathname}`;
let links_paths = {
    'paths' : {
        'index' : './index.html',
        'credits' : 'https://github.com/Boubajoker/SearchGooglePy/blob/ThirdPartyNotices.md',
        'install' : '#install',
        'use' : '#use',
        'table_of_content' : '#table_of_content'
    }
};

if (document.URL == base_url + `?Link=Home`) {
    window.location = links_paths.paths.index;
};

if (document.URL == base_url + `?Link=Credits`) {
    window.location = links_paths.paths.credits;
};

if (document.URL == base_url + `?Link=Install`) {
    window.location = links_paths.paths.install;
};

if (document.URL == base_url + `?Link=Use`) {
    window.location = links_paths.paths.use;
};

if (document.URL == base_url + `?Link=Table_Of_Content`) {
    window.location = links_paths.paths.table_of_content;
};