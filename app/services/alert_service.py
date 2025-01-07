"""Servicio para manejar las alertas del sistema"""

class AlertService:
    # Umbrales de alertas
    CPU_WARNING = 80
    CPU_CRITICAL = 90
    RAM_WARNING = 85
    RAM_CRITICAL = 95
    DISK_WARNING = 85
    DISK_CRITICAL = 95
    TEMP_WARNING = 35
    TEMP_CRITICAL = 40
    LATENCY_WARNING = 100
    LATENCY_CRITICAL = 150
    
    @staticmethod
    def calculate_alerts(sensors_data):
        """Calcula todas las alertas basadas en los datos de sensores"""
        if not sensors_data:
            return []
            
        alerts = []
        alerts.extend(AlertService._check_cpu(sensors_data))
        alerts.extend(AlertService._check_ram(sensors_data))
        alerts.extend(AlertService._check_disk(sensors_data))
        alerts.extend(AlertService._check_temperature(sensors_data))
        alerts.extend(AlertService._check_network(sensors_data))
        alerts.extend(AlertService._check_ups(sensors_data))
        return alerts
    
    @staticmethod
    def _check_cpu(sensors_data):
        """Verifica alertas de CPU"""
        alerts = []
        cpu = float(sensors_data.get('cpu_usage', 0))
        
        if cpu > AlertService.CPU_CRITICAL:
            alerts.append({
                'type': 'danger',
                'message': f'CPU crítico: {cpu:.1f}%'
            })
        elif cpu > AlertService.CPU_WARNING:
            alerts.append({
                'type': 'warning',
                'message': f'CPU alto: {cpu:.1f}%'
            })
        return alerts
    
    @staticmethod
    def _check_ram(sensors_data):
        """Verifica alertas de RAM"""
        alerts = []
        ram = float(sensors_data.get('ram_usage', 0))
        
        if ram > AlertService.RAM_CRITICAL:
            alerts.append({
                'type': 'danger',
                'message': f'RAM crítica: {ram:.1f}%'
            })
        elif ram > AlertService.RAM_WARNING:
            alerts.append({
                'type': 'warning',
                'message': f'RAM alta: {ram:.1f}%'
            })
        return alerts
    
    @staticmethod
    def _check_disk(sensors_data):
        """Verifica alertas de disco"""
        alerts = []
        disk = float(sensors_data.get('disk_usage', 0))
        
        if disk > AlertService.DISK_CRITICAL:
            alerts.append({
                'type': 'danger',
                'message': f'Disco crítico: {disk:.1f}%'
            })
        elif disk > AlertService.DISK_WARNING:
            alerts.append({
                'type': 'warning',
                'message': f'Disco alto: {disk:.1f}%'
            })
        return alerts
    
    @staticmethod
    def _check_temperature(sensors_data):
        """Verifica alertas de temperatura"""
        alerts = []
        temp = float(sensors_data.get('temperature', 0))
        
        if temp > AlertService.TEMP_CRITICAL:
            alerts.append({
                'type': 'danger',
                'message': f'Temperatura crítica: {temp:.1f}°C'
            })
        elif temp > AlertService.TEMP_WARNING:
            alerts.append({
                'type': 'warning',
                'message': f'Temperatura alta: {temp:.1f}°C'
            })
        return alerts
    
    @staticmethod
    def _check_network(sensors_data):
        """Verifica alertas de red"""
        alerts = []
        network = sensors_data.get('network', {})
        latency = float(network.get('latency', 0))
        
        if latency > AlertService.LATENCY_CRITICAL:
            alerts.append({
                'type': 'danger',
                'message': f'Latencia crítica: {latency:.0f}ms'
            })
        elif latency > AlertService.LATENCY_WARNING:
            alerts.append({
                'type': 'warning',
                'message': f'Latencia alta: {latency:.0f}ms'
            })
        return alerts
    
    @staticmethod
    def _check_ups(sensors_data):
        """Verifica alertas de UPS"""
        alerts = []
        ups = sensors_data.get('ups', {})
        
        if ups.get('status') == 'battery':
            battery = float(ups.get('battery_level', 0))
            runtime = int(ups.get('estimated_runtime', 0))
            
            if battery < 20:
                alerts.append({
                    'type': 'danger',
                    'message': f'Batería crítica: {battery:.1f}% ({runtime}min restantes)'
                })
            elif battery < 50:
                alerts.append({
                    'type': 'warning',
                    'message': f'En batería: {battery:.1f}% ({runtime}min restantes)'
                })
        return alerts 