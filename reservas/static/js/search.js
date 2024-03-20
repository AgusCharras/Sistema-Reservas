document.addEventListener('DOMContentLoaded', function () {
    // Obtén una referencia al elemento de entrada de búsqueda y la tabla de resultados
    var searchInput = document.getElementById('search');
    var resultsTable = document.getElementById('results').getElementsByTagName('tbody')[0];

    // Agrega un evento de escucha al campo de búsqueda
    searchInput.addEventListener('input', function () {
        // Obtén el valor actual del campo de búsqueda
        var query = searchInput.value.toLowerCase(); // Convertir a minúsculas para hacer coincidencias sin distinción entre mayúsculas y minúsculas

        // Recorre las filas de la tabla y muestra u oculta según la búsqueda
        var rows = resultsTable.getElementsByTagName('tr');
        for (var i = 0; i < rows.length; i++) {
            var row = rows[i];
            var cells = row.getElementsByTagName('td');
            var matchFound = false;

            // Comprueba si alguna de las celdas contiene el valor de búsqueda
            for (var j = 0; j < cells.length; j++) {
                var cell = cells[j];
                if (cell.textContent.toLowerCase().indexOf(query) > -1) {
                    matchFound = true;
                    break; // Si se encuentra una coincidencia en esta fila, no es necesario verificar las otras celdas
                }
            }

            // Muestra u oculta la fila según si se encontró una coincidencia
            row.style.display = matchFound ? '' : 'none';
        }
    })
});
