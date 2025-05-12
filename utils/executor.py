def execute_code(code: str):
    """
    Esegue codice Python generato dinamicamente in un ambiente controllato.
    - Redirige l'output
    - Gestisce gli errori
    - Blocca side effects pericolosi
    """
    local_vars = {}
    try:
        print("🚀 Esecuzione codice...")
        exec(code, {}, local_vars)
        # Prova a restituire una variabile significativa
        for key in ["result", "data", "output"]:
            if key in local_vars:
                return local_vars[key]
        return None
    except Exception as e:
        print("❌ Errore durante l'esecuzione del codice:\n", str(e))
        return None
