DO
$do$
BEGIN
    IF pg_try_advisory_lock({lock_id}) THEN
        IF EXISTS(SELECT 1 FROM pg_proc
                  WHERE proname = 'set_for_selective_tables_triggers') THEN
            PERFORM audit.set_for_selective_tables_triggers();
        END IF;
        PERFORM pg_advisory_unlock({lock_id});
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        PERFORM pg_advisory_unlock({lock_id});
        RAISE;
END
$do$
LANGUAGE plpgsql;