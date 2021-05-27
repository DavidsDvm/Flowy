$("#header_shopping_cart").ready(function() {
    sessionStorage.setItem("numStopLoop", 0);

    if (window.location.pathname == "/Flowy/" && sessionStorage.getItem("numStopLoop")  == 0){
        sleep(5000);
        document.getElementById('header_logo').src = 'help/img/Logo_Flowy.svg';
        document.getElementById('header_shopping_cart').src = 'help/img/shopping_cart_1.svg';
        document.getElementById('footer_copyright_symbol').src = 'help/img/cophyright_symbol.svg';
        document.getElementById('footer_ubication_symbol').src = 'help/img/ubication_symbol.svg';
        document.getElementById('footer_at_symbol').src = 'help/img/at_sing.svg';
        document.getElementById('footer_up_arrow_symbol').src = 'help/img/up_arrow.svg';
        sessionStorage.setItem("numStopLoop", 1);
    }
});