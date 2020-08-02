

	tab = document.querySelectorAll('.element-tof')
	var activ_tof = function(){ 
			if(this.classList.contains('active')){
				var a = 0 
			}else{

			deja_activ = document.querySelector('.active')
			deja_activ.classList.remove('active')
			deja_activ.classList.add('tof')
			id = this.getAttribute('href')
			activons = document.querySelector(id)
			activons.classList.remove('tof')
			activons.classList.add('active')
			
		}

		}

	for (i=0 ; i<tab.length ; i++) {

			tab[i].addEventListener('mouseover' , activ_tof)
		

		
	}
/*
	element_active = document.querySelector('.active');

	element_active.addEventListener('mouseover' , function(event){
		x = event.clientX;
		y = event.clientY;
		haute = this.offsetHeight 
		large= this.offsetWidth
		console.log("Hauteur   !"+ haute+ "     Largeur     !"+large+"      abcisse  :"+x+"   ordonner   :"+y); 
	})


*/