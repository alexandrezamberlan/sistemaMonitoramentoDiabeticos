import hashlib
import random
import secrets

def gerar_hash():
    return hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()

def gerar_chave_codigo_matricula(texto):
    # Gera um valor aleatório seguro
    aleatorio = secrets.token_hex(8)  # 16 caracteres hex (8 bytes)
    
    # Concatena o nome com o valor aleatório
    base = texto + aleatorio
    
    # Cria um hash SHA-256 da base
    hash_resultado = hashlib.sha256(base.encode()).hexdigest()
    
    # Retorna os primeiros 16 caracteres do hash
    return hash_resultado[:16]