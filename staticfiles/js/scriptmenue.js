
var menue = document.querySelector('#menue-mob');


affiche = function(event){
    menu = document.querySelector("#menue-web");
    menu.classList.toggle('cache-menue');
    menu.classList.toggle('affiche-menue');
}


menue.addEventListener('click' , affiche);










