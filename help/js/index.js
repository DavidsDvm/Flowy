function loadImagesHeader(){
    if (window.location.pathname == "/Flowy/"){
        document.getElementById('header_logo').src = 'help/img/Logo_Flowy.svg';
        document.getElementById('header_shopping_cart').src = 'help/img/shopping_cart_1.svg';
    }
}

function loadImagesFooter(){
    if (window.location.pathname == "/Flowy/"){
        document.getElementById('footer_copyright_symbol').src = 'help/img/cophyright_symbol.svg';
        document.getElementById('footer_ubication_symbol').src = 'help/img/ubication_symbol.svg';
        document.getElementById('footer_at_symbol').src = 'help/img/at_sing.svg';
        document.getElementById('footer_up_arrow_symbol').src = 'help/img/up_arrow.svg';
    }
}