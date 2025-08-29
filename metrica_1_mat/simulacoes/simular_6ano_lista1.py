import random
import os
import time
import pandas as pd

# --- Dados de Referência para a Simulação ---
NOMES_ESTUDANTES = [
    "Ana Clara Santos", "Lucas Almeida Oliveira", "Beatriz Costa Pereira", "Guilherme Souza Lima",
    "Isabela Rocha Santos", "Pedro Henrique Costa", "Mariana Oliveira Dias", "Felipe Silva Martins",
    "Lívia Fernandes Souza", "Rafael Gomes Costa", "Larissa Ribeiro Alves", "Gustavo Barbosa Ferreira",
    "Sofia Castro Mendes", "Matheus Pires Gomes", "Laura Dias Barbosa", "Leonardo Carvalho Lima",
    "Camila Alves Pereira", "Bruno Rocha Souza", "Gabriela Fernandes Silva", "Daniel Martins Oliveira",
    "Valentina Lima Dias", "Thiago Ribeiro Castro", "Manuela Gomes Almeida", "Vitor Lima Souza",
    "Luiza Oliveira Costa", "Arthur Pereira Mendes", "Helena Alves Barbosa", "Enzo Ribeiro Santos",
    "Maria Eduarda Silva", "João Pedro Lima", "Alice Fernandes Gomes", "Bernardo Souza Costa",
    "Julia Oliveira Almeida", "Nicolas Ribeiro Dias", "Giovanna Lima Pereira", "Eduardo Martins Alves",
    "Clara Mendes Barbosa", "Diego Gomes Souza", "Cecília Rocha Lima", "Miguel Carvalho Santos",
    "Yasmin Alves Dias", "Antônio Castro Pereira", "Letícia Martins Lima", "Heitor Gomes Souza",
    "Heloísa Ribeiro Barbosa", "Davi Alves Castro", "Júlia Pires Dias", "Lorenzo Silva Oliveira",
    "Carolina Rocha Mendes", "Benício Alves Santos"
]

LISTA_PROBLEMAS = {
    'lista1': {
        'Q1': {'enunciado': "A biblioteca da escola recebeu novas doações de livros. Na segunda-feira, chegaram 273 livros. Na terça-feira, chegaram 319 livros. No total, quantos livros a biblioteca recebeu nestes dois dias?", 'resposta_esperada': "592"},
        'Q2': {'enunciado': "Um avião tem capacidade para 295 passageiros e, em um voo, está transportando 209 passageiros. Quantas poltronas desse avião não estão ocupadas?", 'resposta_esperada': "86"},
        'Q3': {'enunciado': "Uma fábrica de brinquedos produz 138 carrinhos por dia. Se a fábrica trabalha durante 25 dias em um mês, quantos carrinhos ela produzirá nesse período?", 'resposta_esperada': "3450"},
        'Q4': {'enunciado': "Uma turma de 27 alunos decidiu organizar uma vaquinha para comprar um presente de formatura que custa R$ 945,00. Se todos os alunos contribuírem com a mesma quantia, quanto cada aluno deverá pagar?", 'resposta_esperada': "35"},
        'Q5': {'enunciado': "Em uma campanha de arrecadação de alimentos, o primeiro bairro doou 875 kg de alimentos e o segundo bairro doou 1.120 kg. Quantos quilos de alimentos foram arrecadados pelos dois bairros juntos?", 'resposta_esperada': "1995"},
        'Q6': {'enunciado': "João tinha R$ 1.500,00 na poupança e gastou R$ 385,00 em um presente. Quanto dinheiro sobrou na poupança de João?", 'resposta_esperada': "1115"},
        'Q7': {'enunciado': "Com 12 prestações mensais iguais de R$ 325,00, é possível comprar uma moto. Quanto será pago por essa moto?", 'resposta_esperada': "3900"},
        'Q8': {'enunciado': "Em um teatro, há 126 poltronas distribuídas igualmente em 9 fileiras. Quantas poltronas foram colocadas em cada fileira?", 'resposta_esperada': "14"},
        'Q9': {'enunciado': "Curió comprou três camisas de R$ 25,00 cada e duas calças de R$ 20,00 cada. Ele pagou com cinco notas de R$ 20,00 e uma nota de R$ 50,00. Quanto ele recebeu de troco?", 'resposta_esperada': "35"},
        'Q10': {'enunciado': "Se diariamente são gastos 105 litros de água com uma bacia sanitária não ecológica (que utiliza 15 litros por descarga), e ao substituí-la por uma bacia ecológica (que gasta 6 litros por descarga), qual será a economia diária de água?", 'resposta_esperada': "63"}
    },
    'lista2': {
        'Q1': {'enunciado': "Um fazendeiro plantou 5.300 pés de milho em uma safra e 6.150 pés de milho na safra seguinte. Quantos pés de milho ele plantou no total nas duas safras?", 'resposta_esperada': "11450"},
        'Q2': {'enunciado': "Uma loja de carros oferece um automóvel por R$ 26.454,00 à vista e R$ 38.392,00 a prazo. A diferença entre esses valores é o juro. Qual é a quantia que se pagará de juros ao comprar a prazo?", 'resposta_esperada': "11938"},
        'Q3': {'enunciado': "Um carro bem regulado percorre 12 quilômetros com um litro de gasolina. Se numa viagem foram consumidos 46 litros, qual a distância em quilômetros que o carro percorreu?", 'resposta_esperada': "552"},
        'Q4': {'enunciado': "Uma turma de 30 alunos vai visitar um museu. Se cada carro pode levar 5 alunos, quantos carros serão necessários para levar todos os alunos?", 'resposta_esperada': "6"},
        'Q5': {'enunciado': "No zoológico, nasceram 43 filhotes de pássaros, 15 filhotes de macacos e 28 filhotes de leões. Quantos filhotes nasceram no total no zoológico?", 'resposta_esperada': "86"},
        'Q6': {'enunciado': "Um reservatório de água tinha 10.000 litros e foram utilizados 2.560 litros. Quantos litros de água restam no reservatório?", 'resposta_esperada': "7440"},
        'Q7': {'enunciado': "Em um teatro, há 18 fileiras de poltronas, e em cada fileira foram colocadas 26 poltronas. Quantas poltronas há nesse teatro?", 'resposta_esperada': "468"},
        'Q8': {'enunciado': "Uma padaria produziu 450 pães e vai embalá-los em sacos com 6 pães cada. Quantos sacos serão necessários para embalar todos os pães?", 'resposta_esperada': "75"},
        'Q9': {'enunciado': "Um carro vai percorrer 420 km. O motorista planeja parar a cada 70 km para descansar. Cada parada dura 15 minutos. Quantas paradas ele fará no total?", 'resposta_esperada': "6"},
        'Q10': {'enunciado': "Uma família tem uma renda mensal de R$ 4.500,00. As despesas fixas (aluguel, contas) somam R$ 2.800,00. As despesas variáveis (alimentação, lazer) correspondem a R$ 1.200,00. Se a família quiser dividir o restante do dinheiro igualmente entre 4 membros para gastos pessoais, quanto cada um terá?", 'resposta_esperada': "125"}
    },
    'lista3': {
        'Q1': {'enunciado': "Para organizar um evento, foram vendidos 2.345 ingressos online e 1.987 ingressos na bilheteria. Qual foi o número total de ingressos vendidos para o evento?", 'resposta_esperada': "4332"},
        'Q2': {'enunciado': "Em uma cidade, a população era de 79.412 habitantes em 1980 e passou a ser de 94.070 habitantes em 1991. Qual foi o aumento da população dessa cidade nesse período?", 'resposta_esperada': "14658"},
        'Q3': {'enunciado': "Uma fábrica produz 1.050 brinquedos por dia. Quantos brinquedos essa fábrica produzirá em 15 dias?", 'resposta_esperada': "15750"},
        'Q4': {'enunciado': "Quantos garrafões de 5 litros são necessários para engarrafar 315 litros de vinho?", 'resposta_esperada': "63"},
        'Q5': {'enunciado': "Um atleta correu 7.500 metros em um dia e 6.800 metros no dia seguinte. Qual foi a distância total percorrida pelo atleta nesses dois dias?", 'resposta_esperada': "14300"},
        'Q6': {'enunciado': "Maria tinha 2.000 adesivos em sua coleção e deu 450 adesivos para sua irmã. Com quantos adesivos Maria ficou?", 'resposta_esperada': "1550"},
        'Q7': {'enunciado': "Para a festa de aniversário, foram compradas 5 caixas de refrigerante, e cada caixa contém 24 latas. Quantas latas de refrigerante foram compradas no total?", 'resposta_esperada': "120"},
        'Q8': {'enunciado': "Um professor tem 180 lápis para distribuir igualmente entre 20 alunos. Quantos lápis cada aluno receberá?", 'resposta_esperada': "9"},
        'Q9': {'enunciado': "Estoque de Camisetas e Lucro: Uma loja começou o mês com 250 camisetas em estoque. Na primeira semana, vendeu 85 camisetas. Na segunda semana, vendeu mais 60. Se recebeu uma nova remessa de 120 camisetas e cada camiseta é vendida por R$ 30,00, qual o valor total em reais do estoque final de camisetas (as que sobraram) e quantas camisetas sobraram?", 'resposta_esperada': "225"},
        'Q10': {'enunciado': "Produção de Sucos e Distribuição: Uma fábrica produz 1.200 litros de suco de laranja por dia. Esse suco é embalado em garrafas de 2 litros. As garrafas são transportadas em caixas que contêm 10 garrafas cada. Quantas caixas são necessárias para transportar a produção de 5 dias e quantos litros de suco sobram se 15 dessas caixas forem enviadas para outro estado?", 'resposta_esperada': "5700"}
    },
    'lista4': {
        'Q1': {'enunciado': "Uma empresa produziu 15.670 peças de um produto em janeiro e 18.905 peças em fevereiro. Qual foi a produção total da empresa nesses dois meses?", 'resposta_esperada': "34575"},
        'Q2': {'enunciado': "Um livro tem 560 páginas. Se Ana já leu 325 páginas, quantas páginas ainda faltam para ela terminar o livro?", 'resposta_esperada': "235"},
        'Q3': {'enunciado': "Um agricultor colheu 350 sacas de café, e cada saca pesa 60 kg. Quantos quilos de café ele colheu no total?", 'resposta_esperada': "21000"},
        'Q4': {'enunciado': "Um total de 105 litros de água são gastos diariamente com um tipo de bacia sanitária que usa 15 litros por descarga. Quantas descargas são realizadas nesse dia?", 'resposta_esperada': "7"},
        'Q5': {'enunciado': "Em uma coleta de lixo reciclável, foram recolhidos 2.100 kg de papel, 1.550 kg de plástico e 890 kg de vidro. Quantos quilos de material reciclável foram recolhidos no total?", 'resposta_esperada': "4540"},
        'Q6': {'enunciado': "Um campeonato de futebol teve 120 jogos. Se 78 jogos já foram realizados, quantos jogos ainda faltam para o campeonato acabar?", 'resposta_esperada': "42"},
        'Q7': {'enunciado': "Um livro custa R$ 45,00. Se uma escola comprou 230 livros para a biblioteca, quanto a escola gastou no total?", 'resposta_esperada': "10350"},
        'Q8': {'enunciado': "Uma corda de 240 metros precisa ser dividida em pedaços de 8 metros cada. Quantos pedaços de corda serão obtidos?", 'resposta_esperada': "30"},
        'Q9': {'enunciado': "Uma família tem uma renda mensal de R$ 4.500,00. As despesas fixas (aluguel, contas) somam R$ 2.800,00. As despesas variáveis (alimentação, lazer) correspondem a R$ 1.200,00. Se a família quiser dividir o restante do dinheiro igualmente entre 4 membros para gastos pessoais, quanto cada um terá?", 'resposta_esperada': "125"},
        'Q10': {'enunciado': "Um pedreiro precisa de 320 tijolos para construir um muro. Ele já tem 150 tijolos e comprou mais 5 pacotes com 30 tijolos cada. Quantos tijolos ainda faltam para ele completar o muro?", 'resposta_esperada': "20"}
    },
    'lista5': {
        'Q1': {'enunciado': "Uma loja de eletrônicos vendeu 54 celulares na primeira semana, 78 na segunda semana e 92 na terceira semana. Quantos celulares a loja vendeu no total nessas três semanas?", 'resposta_esperada': "224"},
        'Q2': {'enunciado': "No Maranhão, ocorreram 2.548 casos de febre amarela, e em Pernambuco, 2.095 casos. Qual é a diferença no número de casos ocorridos entre o Maranhão e o Pernambuco?", 'resposta_esperada': "453"},
        'Q3': {'enunciado': "Se um gotejamento lento desperdiça 400 litros de água por mês, quantos litros serão desperdiçados em 4 meses?", 'resposta_esperada': "1600"},
        'Q4': {'enunciado': "Um total de 96 balas será dividido igualmente entre 8 crianças. Quantas balas cada criança receberá?", 'resposta_esperada': "12"},
        'Q5': {'enunciado': "Numa classe há 15 meninos e 13 meninas. Quantas crianças ao todo nessa classe?", 'resposta_esperada': "28"},
        'Q6': {'enunciado': "Uma torta de 12 pedaços teve 7 pedaços comidos. Quantos pedaços de torta sobraram?", 'resposta_esperada': "5"},
        'Q7': {'enunciado': "Se Otávio precisa calcular o dobro de 167 e o triplo de 92, quais são esses valores?", 'resposta_esperada': "334 e 276"},
        'Q8': {'enunciado': "Se um carro percorreu 360 km em 6 horas, mantendo uma velocidade constante, quantos quilômetros ele percorreu por hora?", 'resposta_esperada': "60"},
        'Q9': {'enunciado': "Em um jogo de tabuleiro, Paula começou com 500 pontos. Na primeira rodada, ela perdeu 150 pontos. Na segunda, ela dobrou seus pontos restantes. Na terceira, ela ganhou mais 75 pontos. Com quantos pontos Paula terminou a terceira rodada?", 'resposta_esperada': "775"},
        'Q10': {'enunciado': "Uma doceira fez 350 brigadeiros e 280 beijinhos. Ela vendeu 1/2 dos brigadeiros e 1/4 dos beijinhos. Se cada doce vendido custa R$ 2,00, quanto ela arrecadou no total com as vendas?", 'resposta_esperada': "490"}
    }
}

# --- Lógica de Simulação e Classificação ---
def simular_resposta_aluno(nome_estudante: str, lista_id: str, questao_id: str) -> dict:
    """
    Simula a classificação e justificativa para a resposta de um aluno, com lógica
    especial para a Ana Clara na primeira questão de todas as listas.
    """
    classificacao = ""
    subtipo_erro = ""
    justificativa = ""

    # Lógica Específica para Ana Clara na Questão 1 de cada lista
    if nome_estudante == "Ana Clara Santos" and questao_id == "Q1":
        classificacao = "Incorreto"
        subtipo_erro = "Erro de Interpretação"
        justificativa = "O estudante cometeu um Erro de Interpretação, não conseguindo associar as palavras-chave 'total' e 'recebeu' com a operação de soma, optando por subtrair os valores."
    else:
        tipo_resposta = random.choices(
            ['correta', 'parcialmente_correta', 'incorreta'],
            weights=[0.3, 0.4, 0.3]
        )[0]
        
        if tipo_resposta == 'correta':
            classificacao = "Correto"
            subtipo_erro = ""
            justificativa = "O estudante demonstrou total compreensão e precisão na resolução do problema."
        elif tipo_resposta == 'parcialmente_correta':
            classificacao = "Parcialmente Correto"
            subtipo_erro = "Erro Numérico"
            justificativa = "O estudante identificou a operação correta, mas cometeu um Erro Numérico no cálculo."
        elif tipo_resposta == 'incorreta':
            erro_subtipos = ['Erro de Interpretação', 'Erro Relacional', 'Não Respondeu']
            subtipo_erro = random.choice(erro_subtipos)
            
            classificacao = "Incorreto"
            if subtipo_erro == 'Erro de Interpretação':
                justificativa = "O estudante cometeu um Erro de Interpretação, falhando em compreender o enunciado."
            elif subtipo_erro == 'Erro Relacional':
                justificativa = "O estudante cometeu um Erro Relacional, escolhendo a operação inadequada."
            else:
                justificativa = "O estudante não conseguiu iniciar a resolução ou não apresentou resposta."

    enunciado = LISTA_PROBLEMAS[lista_id][questao_id]['enunciado']
    
    return {
        'nome_estudante': nome_estudante,
        'lista': lista_id,
        'questao': questao_id,
        'enunciado': enunciado,
        'classificacao': classificacao,
        'subtipo_erro': subtipo_erro,
        'justificativa': justificativa
    }


def salvar_resultados_md(resultados: list, output_path: str):
    """Salva os resultados da simulação em um único arquivo Markdown consolidado."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Análise de Desempenho - 6º Ano (Consolidado)\n\n")
        f.write(f"**Simulação gerada em:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for resultado in resultados:
            f.write("---" * 10 + "\n\n")
            f.write(f"### Estudante: {resultado['nome_estudante']}\n\n")
            f.write(f"**Lista:** {resultado['lista'].capitalize()} | **Questão:** {resultado['questao']}\n\n")
            f.write(f"**Enunciado:** {resultado['enunciado']}\n\n")
            f.write(f"**Classificação:** **{resultado['classificacao']}**\n\n")
            if resultado['subtipo_erro']:
                f.write(f"**Subtipo de Erro:** {resultado['subtipo_erro']}\n\n")
            f.write(f"**Justificativa:** {resultado['justificativa']}\n\n")

def salvar_resultados_csv(resultados: list, output_path: str):
    """Salva os resultados da simulação em um único arquivo CSV consolidado."""
    df = pd.DataFrame(resultados)
    df = df[['nome_estudante', 'lista', 'questao', 'enunciado', 'classificacao', 'subtipo_erro', 'justificativa']]
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Arquivo CSV '{output_path}' gerado com sucesso.")

def executar_simulacao_consolidada():
    """Executa a simulação completa para todas as listas e consolida os resultados."""
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    output_dir_md = os.path.join(output_dir, 'documentos')
    output_dir_csv = os.path.join(output_dir, 'analise_dados')
    
    os.makedirs(output_dir_md, exist_ok=True)
    os.makedirs(output_dir_csv, exist_ok=True)
    
    print("--- Simulação de Análise de Desempenho (6º Ano, Consolidado) ---")
    
    resultados_totais_para_salvar = []
    
    for lista_nome, dados_lista in LISTA_PROBLEMAS.items():
        print(f"Simulando respostas para {lista_nome}...")
        for nome_estudante in NOMES_ESTUDANTES:
            for questao_id in dados_lista.keys():
                resultado_simulado = simular_resposta_aluno(nome_estudante, lista_nome, questao_id)
                resultados_totais_para_salvar.append(resultado_simulado)
    
    # --- Salvando os Resultados Consolidados ---
    print("\nSimulação concluída. Salvando resultados consolidados...")
    
    output_path_md = os.path.join(output_dir_md, "6ano_completo.md")
    salvar_resultados_md(resultados_totais_para_salvar, output_path_md)
    print(f"Arquivo '{output_path_md}' gerado com sucesso.")

    output_path_csv = os.path.join(output_dir_csv, "6ano_completo.csv")
    salvar_resultados_csv(resultados_totais_para_salvar, output_path_csv)
    print(f"O arquivo '{output_path_csv}' foi gerado com sucesso.")

# --- Execução Principal ---
if __name__ == "__main__":
    executar_simulacao_consolidada()