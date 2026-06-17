function setView(mode) {
    const grid = document.getElementById('view-grid');
    const list = document.getElementById('view-list');
    const btnGrid = document.getElementById('btn-grid');
    const btnList = document.getElementById('btn-list');

    if (grid && list && btnGrid && btnList) {
        if (mode === 'grid') {
            grid.classList.remove('hidden');
            list.classList.add('hidden');
            btnGrid.classList.add('active');
            btnList.classList.remove('active');
        } else {
            grid.classList.add('hidden');
            list.classList.remove('hidden');
            btnList.classList.add('active');
            btnGrid.classList.remove('active');
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
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