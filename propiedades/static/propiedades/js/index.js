document.addEventListener('DOMContentLoaded', function() {
    
    // 1️⃣ LÓGICA DE ANIMACIÓN SUAVE (SCROLL REVEAL)
    const reveals = document.querySelectorAll('.reveal');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(e => { 
            if (e.isIntersecting) { 
                e.target.classList.add('visible'); 
                observer.unobserve(e.target); 
            } 
        });
    }, { threshold: 0.1 });
    reveals.forEach(r => observer.observe(r));


    // 2️⃣ LÓGICA DEL MENÚ LATERAL DE COSTADO (Forzado Nativo por JS)
    const menuBtn = document.getElementById('menu-btn');
    const menuDropdown = document.getElementById('menu-dropdown');
    
    if (menuBtn && menuDropdown) {
        console.log("Menú de costado listo.");
        
        const spans = menuBtn.querySelectorAll('span');
        const mobileLinks = menuDropdown.querySelectorAll('a');

        // Configuramos el estado inicial de costado (oculto a la derecha)
        menuDropdown.style.setProperty('display', 'flex', 'important');
        menuDropdown.style.setProperty('transform', 'translateX(100%)', 'important');
        menuDropdown.style.setProperty('transition', 'transform 0.4s ease-in-out', 'important');

        let isOpen = false;

        function toggleMenu(e) {
            if (e) e.preventDefault(); 
            
            if (!isOpen) {
                // 🔓 AL ABRIR: Desplazamos el menú hacia adentro de la pantalla
                menuDropdown.style.setProperty('transform', 'translateX(0%)', 'important');
                isOpen = true;
                console.log("Menú lateral abierto.");
            } else {
                // 🔒 AL CERRAR: Lo mandamos de vuelta hacia la derecha (afuera)
                menuDropdown.style.setProperty('transform', 'translateX(100%)', 'important');
                isOpen = false;
                console.log("Menú lateral cerrado.");
            }

            // Animación interactiva de las liñitas para formar la X de cierre
            spans[0].classList.toggle('rotate-45');
            spans[0].classList.toggle('translate-x-[2px]');
            spans[0].classList.toggle('translate-y-[4.5px]'); 
            
            spans[1].classList.toggle('opacity-0');
            
            spans[2].classList.toggle('-rotate-45');
            spans[2].classList.toggle('translate-x-[2px]');
            spans[2].classList.toggle('-translate-y-[4.5px]');
        }

        // Eventos táctiles y clicks en paralelo
        menuBtn.addEventListener('click', toggleMenu);
        menuBtn.addEventListener('touchstart', toggleMenu, { passive: false });
        
        // Si el cliente hace click en un link interno (#servicios), el menú se esconde
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                menuDropdown.style.setProperty('transform', 'translateX(100%)', 'important');
                isOpen = false;
                
                // Reseteamos el botón para que vuelva a ser hamburguesa
                spans[0].classList.remove('rotate-45', 'translate-x-[2px]', 'translate-y-[4.5px]');
                spans[1].classList.remove('opacity-0');
                spans[2].classList.remove('-rotate-45', 'translate-x-[2px]', '-translate-y-[4.5px]');
            });
        });
    }
});