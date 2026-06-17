document.addEventListener('DOMContentLoaded', function() {
    const visorPrincipal = document.getElementById('gallery-main-img');
    const miniaturas = document.querySelectorAll('.gallery-thumb');

    miniaturas.forEach(miniatura => {
        miniatura.addEventListener('click', function() {
            const nuevaSrc = this.querySelector('img').src;
            
            // Efecto de desvanecimiento premium
            visorPrincipal.style.opacity = '0.3';
            
            setTimeout(() => {
                visorPrincipal.src = nuevaSrc;
                visorPrincipal.style.opacity = '1';
            }, 150);

            // Quitamos la clase active de todas las miniaturas
            miniaturas.forEach(m => {
                m.classList.remove('active');
            });
            
            // Le ponemos la clase active a la seleccionada
            this.classList.add('active');
        });
    });
});