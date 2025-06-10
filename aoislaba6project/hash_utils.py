def standardize_key(key):
    return key[0].upper() + key[1:].lower()

def format_entry(table, key):
    return f"{key} - {table.retrieve(key)}"