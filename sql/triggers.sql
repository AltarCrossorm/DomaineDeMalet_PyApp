-- ==================================================
-- Filename : triggers.sql
-- Author : CRESP Enguerran
-- Motor : SQLite
-- Rôle : setup all triggers for Tables
-- Last Update : 06/07/2025
-- ==================================================

CREATE TRIGGER trigger_META_Ingredients_units
BEFORE INSERT ON META_Ingredients
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.primary_unit = NEW.secondary_unit THEN
            RAISE(ABORT, 'primary_unit and secondary_unit must be different')
    END;
END;