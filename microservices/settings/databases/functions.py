def update_datetime() -> str:
    return """
        CREATE OR REPLACE FUNCTION update_datetime()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.modified_at = now(); 
            RETURN NEW;
        END;
        $$ language 'plpgsql'
    """


__all__ = [
    "update_datetime",
]
