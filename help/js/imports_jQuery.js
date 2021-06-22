$( "#header__navbar--jQuery" ).load( "../view/header.html", function(){
    document.getElementById('header_logo').src = '../help/img/Logo_Flowy.svg';
    document.getElementById('header_shopping_cart').src = '../help/img/shopping_cart_1.svg';
});

$( "#footer__main--jQuery" ).load( "../view/footer.html", function(){
    document.getElementById('footer_copyright_symbol').src = '../help/img/cophyright_symbol.svg';
    document.getElementById('footer_ubication_symbol').src = '../help/img/ubication_symbol.svg';
    document.getElementById('footer_at_symbol').src = '../help/img/at_sing.svg';
    document.getElementById('footer_up_arrow_symbol').src = '../help/img/up_arrow.svg';
});

$( "#footer__index--jQuery" ).load( "view/index_footer.html", function(){
    document.getElementById('header_logo').src = 'help/img/Logo_Flowy.svg';
    document.getElementById('header_shopping_cart').src = 'help/img/shopping_cart_1.svg';
});

$( "#header__navbar--index-jQuery" ).load( "view/header.html", function(){
    document.getElementById('footer_copyright_symbol').src = 'help/img/cophyright_symbol.svg';
    document.getElementById('footer_ubication_symbol').src = 'help/img/ubication_symbol.svg';
    document.getElementById('footer_at_symbol').src = 'help/img/at_sing.svg';
    document.getElementById('footer_up_arrow_symbol').src = 'help/img/up_arrow.svg';
});

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