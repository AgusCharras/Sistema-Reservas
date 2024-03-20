// Recupera la preferencia del modo nocturno desde el almacenamiento local
const modoNocturnoGuardado = localStorage.getItem('modoNocturno');

// Obtiene los elementos relevantes
const darkMode = document.querySelector('.dark-mode');
const resultsTable = document.getElementById('results');

console.log("1");

// Función para activar el modo nocturno
function activarModoNocturno() {
    if (darkMode) {
        document.body.classList.add('dark-mode-variables');
        const span1 = darkMode.querySelector('span:nth-child(1)');
        const span2 = darkMode.querySelector('span:nth-child(2)');
        if (span1 && span2) {
            span1.classList.add('active');
            span2.classList.add('active');
        }
        // Guarda la preferencia en el almacenamiento local
        localStorage.setItem('modoNocturno', 'activado');
    }
}

// Función para desactivar el modo nocturno
function desactivarModoNocturno() {
    if (darkMode) {
        document.body.classList.remove('dark-mode-variables');
        const span1 = darkMode.querySelector('span:nth-child(1)');
        const span2 = darkMode.querySelector('span:nth-child(2)');
        if (span1 && span2) {
            span1.classList.remove('active');
            span2.classList.remove('active');
        }
        // Guarda la preferencia en el almacenamiento local
        localStorage.setItem('modoNocturno', 'desactivado');
        console.log("3");
    }
}

// Agrega el evento click al botón o elemento darkMode
darkMode.addEventListener('click', () => {
    const modoNocturnoActivo = document.body.classList.contains('dark-mode-variables');
    if (modoNocturnoActivo) {
        desactivarModoNocturno();
    } else {
        activarModoNocturno();
    }
    console.log("4");
});

// Aplica el modo nocturno al cargar la página si la preferencia está guardada
if (modoNocturnoGuardado === 'activado') {
    activarModoNocturno();
    console.log("5");
}
