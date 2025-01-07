-- Desactivar restricciones de clave foránea temporalmente
SET session_replication_role = 'replica';

-- Limpiar tablas
TRUNCATE TABLE kiosk_log CASCADE;
TRUNCATE TABLE kiosk CASCADE;
TRUNCATE TABLE location CASCADE;
TRUNCATE TABLE states CASCADE;
TRUNCATE TABLE settings CASCADE;

-- Reactivar restricciones de clave foránea
SET session_replication_role = 'origin'; 