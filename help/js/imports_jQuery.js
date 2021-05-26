$( "#header__navbar--jQuery" ).load( "../view/header.html" );
$( "#footer__main--jQuery" ).load( "../view/footer.html" );
$( "#footer__index--jQuery" ).load( "../view/index_footer.html" );

function myUrlFun(site){
    var actualUrl = window.location.pathname.split('/');
    console.log(actualUrl);
    console.log(site);
    console.log(actualUrl.length);
    
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