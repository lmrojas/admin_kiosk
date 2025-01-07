-- Agregar campos de ubicación real a la tabla kiosk
ALTER TABLE kiosk 
ADD COLUMN IF NOT EXISTS current_latitude FLOAT,
ADD COLUMN IF NOT EXISTS current_longitude FLOAT,
ADD COLUMN IF NOT EXISTS location_mismatch BOOLEAN DEFAULT FALSE;

-- Modificar campos de ubicación en la tabla location
ALTER TABLE location 
ADD COLUMN IF NOT EXISTS description TEXT,
ALTER COLUMN address TYPE VARCHAR(255),
ALTER COLUMN address SET NOT NULL,
ALTER COLUMN latitude SET NOT NULL,
ALTER COLUMN longitude SET NOT NULL; 