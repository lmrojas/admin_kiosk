// Inicializar Socket.IO
const socket = io();

// Función para formatear fechas
function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleString();
}

// Función para actualizar los datos de un kiosk
function updateKioskData(data) {
    const kioskCard = $(`#kiosk-${data.id}`);
    if (kioskCard.length) {
        // Actualizar estado
        kioskCard.find('.badge')
            .removeClass()
            .addClass(`badge bg-${data.state.color_class}`)
            .text(data.state.name);
        
        // Actualizar última conexión
        kioskCard.find('.last-connection')
            .text(formatDate(data.last_connection));
        
        // Actualizar datos de sensores si existen
        if (data.sensors_data) {
            let sensorsHtml = '';
            
            if (data.sensors_data.temperature !== undefined) {
                sensorsHtml += `
                    <div class="col-6">
                        <div class="p-2 border rounded">
                            <i class="fas fa-thermometer-half me-1"></i>${data.sensors_data.temperature}°C
                        </div>
                    </div>`;
            }
            
            if (data.sensors_data.cpu_usage !== undefined) {
                sensorsHtml += `
                    <div class="col-6">
                        <div class="p-2 border rounded">
                            <i class="fas fa-microchip me-1"></i>${data.sensors_data.cpu_usage}%
                        </div>
                    </div>`;
            }
            
            if (data.sensors_data.memory_usage !== undefined) {
                sensorsHtml += `
                    <div class="col-6">
                        <div class="p-2 border rounded">
                            <i class="fas fa-memory me-1"></i>${data.sensors_data.memory_usage}%
                        </div>
                    </div>`;
            }
            
            kioskCard.find('.sensors-data .row').html(sensorsHtml);
        }
    }
}

// Función para mostrar notificaciones
function showNotification(message, type = 'success') {
    const alert = $(`
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);
    
    $('.container-fluid').prepend(alert);
    
    // Remover la alerta después de 3 segundos
    setTimeout(() => {
        alert.alert('close');
    }, 3000);
}

// Escuchar actualizaciones de kiosks
socket.on('kiosk_update', (data) => {
    updateKioskData(data);
});

// Escuchar errores de WebSocket
socket.on('error', (error) => {
    showNotification(error.message, 'danger');
});

// Escuchar reconexiones
socket.on('reconnect', () => {
    showNotification('Conexión restablecida', 'success');
});

// Escuchar desconexiones
socket.on('disconnect', () => {
    showNotification('Conexión perdida. Intentando reconectar...', 'warning');
}); 