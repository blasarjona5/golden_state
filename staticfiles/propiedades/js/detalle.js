document.addEventListener('DOMContentLoaded', function() {
    // Control de la galería interactiva de fotos
    const visor = document.getElementById('visor-principal');
    const thumbs = document.querySelectorAll('.thumb');

    if (visor && thumbs.length > 0) {
        thumbs.forEach(thumb => {
            thumb.addEventListener('click', () => {
                const src = thumb.dataset.src;
                if (!src || visor.src.endsWith(src)) return;

                // Animación de parpadeo suave
                visor.style.opacity = '0';
                setTimeout(() => {
                    visor.src = src;
                    visor.style.opacity = '1';
                }, 280);

                thumbs.forEach(t => t.classList.remove('active'));
                thumb.classList.add('active');
            });
        });
    }

    // Animación unificada de Scroll Reveal
    const reveals = document.querySelectorAll('.reveal');
    const obs = new IntersectionObserver(entries => {
        entries.forEach(e => { 
            if (e.isIntersecting) { 
                e.target.classList.add('visible'); 
                obs.unobserve(e.target); 
            } 
        });
    }, { 
        threshold: 0.07 
    });

    reveals.forEach(r => obs.observe(r));
});