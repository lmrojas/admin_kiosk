// Función para aplicar filtros
function applyFilters() {
    const selectedLocation = $('#location-filter').val();
    const selectedState = $('#state-filter').val();
    const searchText = $('#search-filter').val().toLowerCase();

    $('.kiosk-card').each(function() {
        const card = $(this);
        const locationId = card.data('location-id');
        const state = card.find('.badge').text().toLowerCase();
        const kioskName = card.find('.kiosk-name').text().toLowerCase();
        const serialNumber = card.find('.serial-number').text().toLowerCase();

        const locationMatch = selectedLocation === '' || locationId === parseInt(selectedLocation);
        const stateMatch = selectedState === '' || state === selectedState.toLowerCase();
        const searchMatch = searchText === '' || 
                          kioskName.includes(searchText) || 
                          serialNumber.includes(searchText);

        if (locationMatch && stateMatch && searchMatch) {
            card.show();
        } else {
            card.hide();
        }
    });

    // Actualizar contador de kiosks visibles
    const visibleKiosks = $('.kiosk-card:visible').length;
    const totalKiosks = $('.kiosk-card').length;
    $('#kiosk-counter').text(`Mostrando ${visibleKiosks} de ${totalKiosks} kiosks`);
}

// Inicializar filtros
$(document).ready(function() {
    // Agregar eventos de cambio a los filtros
    $('#location-filter, #state-filter').change(function() {
        applyFilters();
    });

    // Agregar evento de búsqueda con debounce
    let searchTimeout;
    $('#search-filter').on('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(applyFilters, 300);
    });

    // Aplicar filtros iniciales
    applyFilters();
});

// Función para limpiar filtros
function clearFilters() {
    $('#location-filter').val('');
    $('#state-filter').val('');
    $('#search-filter').val('');
    applyFilters();
} 