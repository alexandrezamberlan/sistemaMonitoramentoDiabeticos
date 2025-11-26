from conecta_llm import Conecta

model = Conecta.conectar_api()
if model and not isinstance(model, str):
    Conecta.testar_conexao(model)