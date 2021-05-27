$( "#header__navbar--jQuery" ).load( "../view/header.html" );
$( "#footer__main--jQuery" ).load( "../view/footer.html" );
$( "#footer__index--jQuery" ).load( "view/index_footer.html" );
$( "#header__navbar--index-jQuery" ).load( "view/header.html" );

// Si entra a index.html se le llevara a flowy normal
if (window.location.pathname == "/Flowy/index.html"){
    window.location.href = "../Flowy";
}

function myUrlFun(site){
    var actualUrl = window.location.pathname.split('/');
    console.log(actualUrl);
    console.log(site);
    console.log(actualUrl.length);
    
    // Estos condicionales tienen como objetivo redireccionar correctamente en el Headers(navbar)
    if (window.location.pathname == "/Flowy/"){
        // Si la pagina esta hosteada en GitHub
        if (site == 'index'){
            if (actualUrl.length == 3){
                window.location.href = site + ".html";
            } else if (actualUrl.length >= 4) {
                window.location.href = "../" + site + ".html";
            } 
        } else {
            if (actualUrl.length >= 4){
                window.location.href = site + ".html";
            } else if (actualUrl.length == 3) {
                window.location.href = "view/" + site + ".html";
            }
        }
    } else {
        // Si la pagina esta hosteada en forma local
        if (site == 'index') {
            if (actualUrl.length == 2){
                window.location.href = site + ".html";
            } else if (actualUrl.length >= 3) {
                window.location.href = "../" + site + ".html";
            }
        } else{
            if (actualUrl.length >= 3){
                window.location.href = site + ".html";
            } else if (actualUrl.length == 2) {
                window.location.href = "view/" + site + ".html";
            }
        }
    }

}