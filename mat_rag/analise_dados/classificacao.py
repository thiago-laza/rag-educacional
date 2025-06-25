import re
import pandas as pd

# Caminho do arquivo
arquivo = "/home/laza/chat_RAG_hf/api/chat_05_MAT/documentos/contexto_pedagogico.md"

# Função de classificação com base em heurísticas simples
def classificar_resposta(interpretacao, estrategia, calculos, resposta_final):
    if not any([interpretacao, estrategia, calculos, resposta_final]):
        return 0  # Nível 0: ausente
    if resposta_final and "15" in resposta_final:
        if all([interpretacao, estrategia, calculos]):
            return 3  # Nível 3: intermediário/satisfatório
        elif any([interpretacao, estrategia, calculos]):
            return 2  # Nível 2: básico/em desenvolvimento
        else:
            return 1  # Nível 1: superficial
    elif resposta_final and any(x in resposta_final for x in ["20", "27", "45"]):
        return 1  # Nível 1: resposta errada mas tentativa
    else:
        return 0  # Nível 0: sem coerência

# Lê o conteúdo do arquivo markdown
with open(arquivo, "r", encoding="utf-8") as f:
    texto = f.read()

# Divide por estudante
blocos = re.split(r"## Estudante:\s+", texto)[1:]  # ignora cabeçalho inicial

dados = []

for bloco in blocos:
    linhas = bloco.strip().split("\n")
    nome = linhas[0].strip()
    interp = estrat = calc = resp = ""

    for linha in linhas:
        if linha.startswith("**Interpretação**:"):
            interp = linha.replace("**Interpretação**:", "").strip()
        elif linha.startswith("**Estratégia**:"):
            estrat = linha.replace("**Estratégia**:", "").strip()
        elif linha.startswith("**Cálculos**:"):
            calc = linha.replace("**Cálculos**:", "").strip()
        elif linha.startswith("**Resposta Final**:"):
            resp = linha.replace("**Resposta Final**:", "").strip()

    nivel = classificar_resposta(interp, estrat, calc, resp)

    dados.append({
        "nome": nome,
        "interpretacao": interp,
        "estrategia": estrat,
        "calculos": calc,
        "resposta_final": resp,
        "nivel_classificacao": nivel
    })

# Cria o DataFrame
df = pd.DataFrame(dados)

# Mostra as 5 primeiras linhas
print(df.head())

# Exporta para CSV
df.to_csv("respostas_classificadas.csv", index=False)
print("Arquivo 'respostas_classificadas.csv' salvo com sucesso.")
