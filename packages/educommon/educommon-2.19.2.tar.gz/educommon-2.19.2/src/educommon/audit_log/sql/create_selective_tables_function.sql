SELECT audit.drop_functions_by_name('set_for_selective_tables_triggers');
CREATE FUNCTION audit.set_for_selective_tables_triggers(
) RETURNS void AS $body$
DECLARE
    target_table RECORD;
BEGIN
-- Устанавливаются триггеры для таблиц, которые указаны в table_for_inserting
-- и для которых еще не создан триггер.
    FOR target_table IN
        SELECT name AS table_name, schema AS table_schema
        FROM audit.table_for_inserting
        WHERE name NOT IN (
                SELECT event_object_table
                FROM information_schema.triggers
                WHERE event_object_schema = 'public' AND
                    trigger_name = 'audit_trigger' AND
                    trigger_schema = 'public'
            )
    LOOP
        EXECUTE
           'drop trigger if exists audit_trigger ' ||
           'on ' || target_table.table_schema || '.' || target_table.table_name;
        EXECUTE
            'create trigger audit_trigger after insert or update or delete ' ||
            'on '|| target_table.table_schema || '.' ||
            target_table.table_name || ' ' ||
            'for each row execute procedure audit.on_modify()';
    END LOOP;

-- Триггеры для таблиц, которые не указаны в table_for_inserting, удаляются.
    FOR target_table IN
        SELECT table_name, table_schema
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE' AND
            table_name NOT IN (SELECT name
                               FROM audit.table_for_inserting)
    LOOP
        EXECUTE
           'drop trigger if exists audit_trigger ' ||
           'on ' || target_table.table_schema || '.' || target_table.table_name;
    END LOOP;
END
$body$
LANGUAGE plpgsql;