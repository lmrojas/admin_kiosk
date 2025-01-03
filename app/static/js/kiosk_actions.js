// Funciones para manejo de acciones de kiosks
const KioskActions = {
    socket: null,
    
    // Inicializar WebSocket
    init: function() {
        this.socket = io('/kiosk');
        this.setupSocketListeners();
        this.setupEventListeners();
    },
    
    // Configurar listeners de WebSocket
    setupSocketListeners: function() {
        this.socket.on('connect', () => {
            console.log('WebSocket conectado');
        });
        
        this.socket.on('disconnect', () => {
            console.log('WebSocket desconectado');
        });
        
        this.socket.on('kiosk_update', data => {
            this.updateKioskCard(data);
        });
        
        this.socket.on('kiosk_action_update', data => {
            this.updateActionState(data.kiosk_id, data.state);
        });
    },
    
    // Configurar listeners de eventos
    setupEventListeners: function() {
        $(document).on('click', '.action-btn', event => {
            const btn = $(event.currentTarget);
            const card = btn.closest('[data-kiosk-id]');
            const kioskId = card.data('kioskId');
            const actionId = btn.data('actionId');
            const actionName = btn.data('actionName');
            const requiresConfirmation = btn.data('requiresConfirmation');
            
            this.executeAction(kioskId, actionId, actionName, requiresConfirmation);
        });
    },
    
    // Ejecutar una acción en un kiosk
    executeAction: function(kioskId, actionId, actionName, requiresConfirmation) {
        if (requiresConfirmation && !confirm(`¿Está seguro que desea ejecutar la acción "${actionName}"?`)) {
            return;
        }
        
        return $.ajax({
            url: `/kiosk/api/execute/${kioskId}/${actionId}`,
            method: 'POST',
            contentType: 'application/json'
        }).then(response => {
            this.showNotification('success', 'Acción ejecutada exitosamente');
            return response;
        }).catch(xhr => {
            const message = xhr.responseJSON?.message || 'Error al ejecutar la acción';
            this.showNotification('danger', message);
            throw xhr;
        });
    },

    // Asignar ubicación a un kiosk
    assignLocation: function(kioskId, locationId, notes) {
        return $.ajax({
            url: '/location/api/assign-kiosk',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                kiosk_id: kioskId,
                location_id: locationId,
                notes: notes || ''
            })
        }).then(response => {
            this.showNotification('success', 'Ubicación asignada exitosamente');
            return response;
        }).catch(xhr => {
            const message = xhr.responseJSON?.message || 'Error al asignar la ubicación';
            this.showNotification('danger', message);
            throw xhr;
        });
    },

    // Actualizar tarjeta de kiosk con nuevos datos
    updateKioskCard: function(data) {
        const card = $(`[data-kiosk-id="${data.id}"]`);
        if (!card.length) return;
        
        // Actualizar estado
        card.find('.status-badge')
            .removeClass('bg-success bg-danger')
            .addClass(`bg-${data.status === 'online' ? 'success' : 'danger'}`)
            .text(data.status.charAt(0).toUpperCase() + data.status.slice(1));
        
        if (!data.sensors_data) return;
        
        // Actualizar métricas de sistema
        this.updateProgressBar(card.find('.cpu-bar'), data.sensors_data.cpu_usage);
        this.updateProgressBar(card.find('.ram-bar'), data.sensors_data.ram_usage);
        this.updateProgressBar(card.find('.disk-bar'), data.sensors_data.disk_usage);
        
        // Actualizar métricas de ambiente
        card.find('.temp-value')
            .removeClass('text-danger text-warning')
            .addClass(data.sensors_data.temperature > 40 ? 'text-danger' : 
                     data.sensors_data.temperature > 35 ? 'text-warning' : '')
            .text(`${data.sensors_data.temperature}°C`);
        
        card.find('.humidity-value').text(`${data.sensors_data.humidity}%`);
        
        // Actualizar red
        card.find('.latency-value').text(`${data.sensors_data.network.latency}ms`);
        card.find('.speed-value').text(`↓${data.sensors_data.network.download_speed}Mbps`);
        card.find('.signal-value')
            .removeClass('text-warning')
            .addClass(data.sensors_data.network.signal_strength < 30 ? 'text-warning' : '')
            .text(`${data.sensors_data.network.signal_strength}%`);
        
        // Actualizar UPS si existe
        if (data.sensors_data.ups) {
            const upsSection = card.find('.ups-section');
            if (!upsSection.length) {
                // TODO: Crear sección UPS si no existe
            } else {
                upsSection.find('.battery-value')
                    .removeClass('text-danger')
                    .addClass(data.sensors_data.ups.battery_level < 10 ? 'text-danger' : '')
                    .text(`${data.sensors_data.ups.battery_level}%`);
                upsSection.find('.runtime-value').text(`${data.sensors_data.ups.estimated_runtime}min`);
            }
        }
        
        // Actualizar alertas
        const alertsSection = card.find('.alerts-section').empty();
        data.sensors_data.errors?.forEach(error => {
            alertsSection.append(`
                <div class="alert alert-danger py-1 px-2 mb-1">${error}</div>
            `);
        });
        data.sensors_data.warnings?.forEach(warning => {
            alertsSection.append(`
                <div class="alert alert-warning py-1 px-2 mb-1">${warning}</div>
            `);
        });
    },
    
    // Actualizar estado de acción
    updateActionState: function(kioskId, state) {
        const card = $(`[data-kiosk-id="${kioskId}"]`);
        if (!card.length) return;
        
        card.find('.action-state').text(state);
    },
    
    // Actualizar barra de progreso
    updateProgressBar: function(bar, value) {
        if (!bar.length) return;
        
        const oldValue = bar.data('value');
        bar.data('value', value)
           .css('width', `${value}%`)
           .text(`${bar.text().split(':')[0]}: ${value}%`)
           .removeClass('bg-success bg-warning bg-danger')
           .addClass(this.getProgressBarClass(value, bar.hasClass('ram-bar')));
        
        if (oldValue !== value) {
            bar.addClass('progress-bar-animated').addClass('progress-bar-striped');
            setTimeout(() => {
                bar.removeClass('progress-bar-animated').removeClass('progress-bar-striped');
            }, 1000);
        }
    },
    
    // Obtener clase para barra de progreso
    getProgressBarClass: function(value, isRam) {
        if (isRam) {
            return value > 95 ? 'bg-danger' : value > 85 ? 'bg-warning' : 'bg-success';
        }
        return value > 90 ? 'bg-danger' : value > 80 ? 'bg-warning' : 'bg-success';
    },

    // Mostrar notificación
    showNotification: function(type, message) {
        const alert = $(`
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
        $('.container-fluid').prepend(alert);
        
        // Auto-ocultar después de 5 segundos
        setTimeout(() => alert.alert('close'), 5000);
    }
};

// Inicializar cuando el documento esté listo
$(document).ready(() => {
    KioskActions.init();
}); 