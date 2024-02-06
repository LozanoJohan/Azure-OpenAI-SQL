def query_getter(key_words, limit):
    if "FacturasVenta" in key_words and "Cliente" in key_words:
        query = f"""SELECT TOP {limit} * FROM FACTURASVENTA INNER JOIN CLIENTES ON FACTURASVENTA.CODCLIENTE = CLIENTES.CODCLIENTE"""
    elif "FacturasVenta" in key_words:
        query = f"""SELECT TOP {limit} * FROM FACTURASVENTA"""
    elif "Cliente" in key_words:
        query = f"""SELECT TOP {limit} * FROM CLIENTES"""
    else: query=None

    return query
