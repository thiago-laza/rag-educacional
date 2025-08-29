import pandas as pd
import random
import os
import time

# --- 1. Dados de Referência e Caminhos ---
PERGUNTAS_DIR = "testes"
METRICAS_DIR = "metricas"
RESPOSTAS_SIMULADAS_DIR = "respostas_simuladas"
DATASETS_CLASSIFICADOS_DIR = "datasets_classificados"

# --- Dados do Gabarito e da Métrica (embutidos para evitar erros de arquivo) ---
DADOS_TESTE1 = {
    'questao_id': [f"Q{i}" for i in range(1, 21)],
    'pergunta': [
        "A biblioteca da escola recebeu novas doações de livros. Na segunda-feira, chegaram 273 livros. Na terça-feira, chegaram 319 livros. No total, quantos livros a biblioteca recebeu nestes dois dias?",
        "Em uma campanha de arrecadação de alimentos, o primeiro bairro doou 875 kg de alimentos e o segundo bairro doou 1.120 kg. Quantos quilos de alimentos foram arrecadados pelos dois bairros juntos?",
        "Um fazendeiro plantou 5.300 pés de milho em uma safra e 6.150 pés de milho na safra seguinte. Quantos pés de milho ele plantou no total nas duas safras?",
        "No zoológico, nasceram 43 filhotes de pássaros, 15 filhotes de macacos e 28 filhotes de leões. Quantos filhotes nasceram no total no zoológico?",
        "Para organizar um evento, foram vendidos 2.345 ingressos online e 1.987 ingressos na bilheteria. Qual foi o número total de ingressos vendidos para o evento?",
        "Um atleta correu 7.500 metros em um dia e 6.800 metros no dia seguinte. Qual foi a distância total percorrida pelo atleta nesses dois dias?",
        "Uma empresa produziu 15.670 peças de um produto em janeiro e 18.905 peças em fevereiro. Qual foi a produção total da empresa nesses dois meses?",
        "Em uma coleta de lixo reciclável, foram recolhidos 2.100 kg de papel, 1.550 kg de plástico e 890 kg de vidro. Quantos quilos de material reciclável foram recolhidos no total?",
        "Uma loja de eletrônicos vendeu 54 celulares na primeira semana, 78 na segunda semana e 92 na terceira semana. Quantos celulares a loja vendeu no total nessas três semanas?",
        "Numa classe há 15 meninos e 13 meninas. Quantas crianças ao todo nessa classe?",
        "Uma escola funciona em dois turnos. No turno matutino há 1.407 alunos e no turno vespertino há 1.825 alunos. Quantos alunos estudam nessa escola?",
        "De acordo com o censo realizado em 1991, o estado da Paraíba tem 1.546.042 homens e 1.654.578 mulheres. Qual é a população da Paraíba segundo esse censo?",
        "Em uma fruteira, há 7 laranjas, 5 maçãs e 3 bananas. Quantas frutas há no total na fruteira?",
        "No aquário de Ana, havia 18 peixes. Ela foi à loja e comprou mais 7 peixes. Com quantos peixes Ana ficou?",
        "Um ônibus partiu com 35 passageiros. Na primeira parada, subiram mais 12 pessoas. Quantos passageiros o ônibus tem agora?",
        "Marta tinha R$ 45,00. Seu pai lhe deu mais R$ 20,00. Quanto dinheiro Marta tem?",
        "Uma biblioteca tinha 320 livros infantis. Eles adquiriram mais 85 livros novos. Quantos livros infantis a biblioteca possui agora?",
        "Em um estacionamento, há 15 carros brancos, 10 carros pretos e 5 carros vermelhos. Quantos carros há no total?",
        "Uma equipe de basquete marcou 28 pontos no primeiro quarto e 35 pontos no segundo quarto. Quantos pontos a equipe marcou juntos nesses dois quartos?",
        "Em uma fazenda, há 120 galinhas e 85 patos. Quantas aves há ao todo na fazenda?"
    ],
    'resposta_esperada': [
        "Para saber o total, eu somei os livros dos dois dias: 273+319=592. A biblioteca recebeu um total de 592 livros.",
        "Para encontrar o total arrecadado, somei as doações dos dois bairros: 875 kg+1.120 kg=1.995 kg. Foram arrecadados 1.995 kg de alimentos.",
        "Para saber o total de pés de milho plantados, somei os pés de milho de cada safra: 5.300+6.150=11.450. Ele plantou 11.450 pés de milho no total nas duas safras.",
        "Para calcular o total de filhotes nascidos, somei o número de filhotes de cada espécie: 43+15+28=86. Nasceram 86 filhotes no total no zoológico.",
        "Para obter o número total de ingressos, somei os ingressos vendidos online e na bilheteria: 2.345+1.987=4.332. O número total de ingressos vendidos foi 4.332.",
        "Para encontrar a distância total percorrida, somei a distância de cada dia: 7.500 metros+6.800 metros=14.300 metros. O atleta percorreu 14.300 metros no total.",
        "Para calcular a produção total, somei as peças produzidas em janeiro e fevereiro: 15.670+18.905=34.575. A produção total da empresa nesses dois meses foi de 34.575 peças.",
        "Para saber o total de material reciclável recolhido, somei as quantidades de cada material: 2.100 kg+1.550 kg+890 kg=4.540 kg. Foram recolhidos 4.540 kg de material reciclável no total.",
        "Para encontrar o total de celulares vendidos, somei as vendas de cada semana: 54+78+92=224. A loja vendeu 224 celulares no total nessas três semanas.",
        "Para saber o total de crianças, somei o número de meninos e meninas: 15+13=28. Há 28 crianças ao todo nessa classe.",
        "Para calcular o total de alunos que estudam na escola, somei os alunos do turno matutino e vespertino: 1.407+1.825=3.232. Estudam 3.232 alunos nessa escola.",
        "Para determinar a população total da Paraíba, somei o número de homens e mulheres: 1.546.042+1.654.578=3.200.620. A população da Paraíba, segundo esse censo, é de 3.200.620 habitantes.",
        "Para saber o total de frutas, somei a quantidade de cada tipo de fruta: 7+5+3=15. Há 15 frutas no total na fruteira.",
        "Para saber com quantos peixes Ana ficou, somei os peixes que ela já tinha com os que comprou: 18+7=25. Ana ficou com 25 peixes.",
        "Para calcular o total de passageiros, somei os passageiros iniciais com os que subiram na parada: 35+12=47. O ônibus tem 47 passageiros agora.",
        "Para saber quanto dinheiro Marta tem, somei o valor que ela já possuía com o que seu pai lhe deu: R$ 45,00+R$20,00=R$65,00. Marta tem R$ 65,00.",
        "Para saber o total de livros infantis, somei os livros que a biblioteca já tinha com os que foram adquiridos: 320+85=405. A biblioteca possui 405 livros infantis agora.",
        "Em um estacionamento, há 15 carros brancos, 10 carros pretos e 5 carros vermelhos. Quantos carros há no total?",
        "Uma equipe de basquete marcou 28 pontos no primeiro quarto e 35 pontos no segundo quarto. Quantos pontos a equipe marcou juntos nesses dois quartos?",
        "Em uma fazenda, há 120 galinhas e 85 patos. Quantas aves há ao todo na fazenda?"
    ],
    'resposta_numerica_esperada': [
        "592", "1995", "11450", "86", "4332", "14300", "34575", "4540", "224", "28",
        "3232", "3200620", "15", "25", "47", "65", "405", "30", "63", "205"
    ]
}

TEXTO_METRICA = """
# Métrica de Acertos e Erros

Esta métrica avalia o desempenho do estudante na resolução de problemas de matemática.

### Tipos de Classificação da Resposta:

* **Correto**: A resposta está completamente certa. O estudante demonstrou total compreensão do problema, escolheu a(s) operação(ões) correta(s) e executou os cálculos com exatidão. Não há erros.
* **Parcialmente Correto**: A resposta está parcialmente certa. O estudante entendeu a lógica principal do problema, mas cometeu erros numéricos ou de cálculo. A compreensão do problema é correta, mas a precisão aritmética falhou.
* **Incorreto**: A resposta está errada. O estudante falhou na interpretação do problema, escolheu uma operação inadequada ou não apresentou nenhuma resposta.
"""

# --- 2. Funções de Geração e Análise ---

def gerar_arquivos_iniciais():
    """Gera o arquivo de métrica e o gabarito."""
    os.makedirs(METRICAS_DIR, exist_ok=True)
    os.makedirs(PERGUNTAS_DIR, exist_ok=True)
    
    # Gera o arquivo de métrica
    with open(os.path.join(METRICAS_DIR, "acertos_e_erros.md"), "w") as f:
        f.write(TEXTO_METRICA)
    print("Arquivo de métrica 'acertos_e_erros.md' gerado com sucesso.")
    
    # Gera o arquivo de gabarito (teste1.csv)
    df_gabarito = pd.DataFrame(DADOS_TESTE1)
    df_gabarito.to_csv(os.path.join(PERGUNTAS_DIR, "teste1.csv"), index=False)
    print("Arquivo de gabarito 'teste1.csv' gerado com sucesso.")
    
    return df_gabarito

def gerar_respostas_simuladas(df_gabarito):
    """Gera as respostas simuladas dos estudantes, separadas por ano."""
    os.makedirs(RESPOSTAS_SIMULADAS_DIR, exist_ok=True)
    
    # Erros de cálculo e conceituais simplificados
    erros_calculo = ["Eu somei, mas o resultado deu 123.", "O cálculo que fiz foi 456 + 1000 = 1450."]
    erros_conceituais = ["Não entendi a pergunta, achei que era para subtrair.", "Achei que era um problema de divisão."]
    
    anos = [6, 7, 8, 9]
    for ano in anos:
        respostas = []
        for i in range(50): # 50 estudantes por ano
            for j in range(len(df_gabarito)):
                questao_id = df_gabarito.iloc[j]['questao_id']
                
                # Lógica de simulação de resposta
                tipo_resposta = random.choices(
                    ['correta', 'erro_calculo', 'erro_conceitual', 'sem_resposta'],
                    weights=[0.6, 0.2, 0.15, 0.05]
                )[0]
                
                if tipo_resposta == 'correta':
                    resposta_aluno = df_gabarito.iloc[j]['resposta_esperada']
                elif tipo_resposta == 'erro_calculo':
                    resposta_aluno = random.choice(erros_calculo)
                elif tipo_resposta == 'erro_conceitual':
                    resposta_aluno = random.choice(erros_conceituais)
                else:
                    resposta_aluno = "Não respondeu."
                
                respostas.append({
                    'aluno_id': f"ALUNO_{ano}_{i+1}",
                    'nome_aluno': f"Estudante {i+1}",
                    'questao_id': questao_id,
                    'resposta_aluno': resposta_aluno
                })
        
        df_respostas = pd.DataFrame(respostas)
        df_respostas.to_csv(os.path.join(RESPOSTAS_SIMULADAS_DIR, f"respostas_simuladas_{ano}_ano.csv"), index=False)
        print(f"Respostas simuladas para o {ano}º ano geradas com sucesso.")

def analisar_e_classificar_respostas(df_gabarito):
    """Analisa as respostas simuladas e gera os datasets classificados."""
    os.makedirs(DATASETS_CLASSIFICADOS_DIR, exist_ok=True)
    
    anos = [6, 7, 8, 9]
    gabarito_map = df_gabarito.set_index('questao_id')['resposta_numerica_esperada'].to_dict()
    
    for ano in anos:
        respostas_path = os.path.join(RESPOSTAS_SIMULADAS_DIR, f"respostas_simuladas_{ano}_ano.csv")
        df_respostas = pd.read_csv(respostas_path)
        
        classificacoes = []
        for index, row in df_respostas.iterrows():
            resposta_aluno = str(row['resposta_aluno'])
            questao_id = row['questao_id']
            resposta_esperada = gabarito_map.get(questao_id)
            
            classificacao = "Incorreto"
            if "Não respondeu" in resposta_aluno:
                classificacao = "Incorreto"
            elif resposta_esperada and resposta_esperada in resposta_aluno:
                classificacao = "Correto"
            elif any(s in resposta_aluno for s in ["somei", "subtrai", "dividi", "multipliquei"]):
                classificacao = "Parcialmente Correto"
            
            classificacoes.append(classificacao)
        
        df_respostas['classificacao'] = classificacoes
        df_respostas.to_csv(os.path.join(DATASETS_CLASSIFICADOS_DIR, f"dataset_classificado_{ano}_ano.csv"), index=False)
        print(f"Dataset classificado do {ano}º ano gerado com sucesso.")

# --- 3. Execução Principal ---
if __name__ == "__main__":
    print("Iniciando a geração de dados...")
    df_gabarito = gerar_arquivos_iniciais()
    print("\nGerando respostas de estudantes...")
    gerar_respostas_simuladas(df_gabarito)
    print("\nIniciando a análise e classificação dos dados...")
    analisar_e_classificar_respostas(df_gabarito)
    print("\nProcesso concluído com sucesso. Os datasets classificados estão na pasta 'datasets_classificados'.")