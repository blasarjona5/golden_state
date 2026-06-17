/**
 * 🎰 Golden State Luxury - Contact Interactions (Ultra-Optimized)
 */
document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Control de Estado en los Inputs (Validación visual si tienen texto)
    const luxuryInputs = document.querySelectorAll('.input-luxury');

    luxuryInputs.forEach(input => {
        // Ejecutar al perder el foco (blur)
        input.addEventListener('blur', () => {
            if (input.value.trim() !== "") {
                // Si tiene texto, le sumamos una clase indicadora
                input.classList.add('has-text');
            } else {
                // Si está vacío, se la quitamos
                input.classList.remove('has-text');
            }
        });

        // Opcional: Verificar si Django ya recargó el formulario con datos (ej. un error)
        if (input.value.trim() !== "") {
            input.classList.add('has-text');
        }
    });

    // 2. Lógica de los botones de Motivo de Consulta (Sincronizado con Django)
    const motivoButtons = document.querySelectorAll('.motivo-btn-gs');
    const hiddenInput = document.getElementById('id_motivo_consulta');

    motivoButtons.forEach(button => {
        button.addEventListener('click', function() {
            motivoButtons.forEach(btn => {
                btn.classList.remove('bg-[#c9a84c]', 'text-[#0a0a0b]', 'border-[#c9a84c]');
                btn.classList.add('border-white/10', 'text-neutral-400');
            });
            this.classList.remove('border-white/10', 'text-neutral-400');
            this.classList.add('bg-[#c9a84c]', 'text-[#0a0a0b]', 'border-[#c9a84c]');
            
            if (hiddenInput) {
                hiddenInput.value = this.getAttribute('data-value');
            }
        });
    });

    // 3. Lógica del Acordeón Minimalista (FAQs)
    const faqHeaders = document.querySelectorAll('.faq-header');
    faqHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const body = this.nextElementSibling;
            const icon = this.querySelector('.faq-icon');
            
            body.classList.toggle('hidden');
            if (icon) icon.classList.toggle('rotate-180');
        });
    });
});