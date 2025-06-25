-----

# README do Projeto de Chatbots Pedagógicos (RAG + Gemini API)

Este projeto apresenta dois chatbots pedagógicos iniciais, um focado em **Matemática** e outro em **Língua Portuguesa**. Ambos servem como **primeiros testes** da arquitetura Retrieval-Augmented Generation (RAG) combinada com a API Gemini, utilizando **apenas um documento de contexto** para cada área para fornecer feedback contextualizado aos professores sobre o desempenho de seus estudantes.

-----

## 💻 Parte Técnica: Como Usar os Chats

Esta seção detalha o processo de configuração e execução dos chatbots.

### Pré-requisitos

Certifique-se de ter o Python (versão 3.10 ou superior é recomendada) e o `pip` (gerenciador de pacotes do Python) instalados em seu sistema.

### 1\. Clonar o Repositório

Primeiro, clone este repositório para sua máquina local. Abra o terminal e execute:

```bash
git clone <https://github.com/thiago-laza/rag-educacional>
cd mat_port_rag # Navegue até a pasta raiz do projeto
```

### 2\. Configurar o Ambiente Virtual

É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto.

```bash
python3 -m venv venv_rag
source venv_rag/bin/activate # No Linux/macOS
# Para Windows: .\venv_rag\Scripts\activate
```

### 3\. Instalar as Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias listadas no arquivo `requirements.txt`. Certifique-se de ter gerado ou atualizado este arquivo conforme instruído anteriormente com `pip freeze > requirements.txt`.

```bash
pip install -r requirements.txt
```

Este comando instalará:

  * `google-generativeai`: Para interagir com a API Gemini.
  * `langchain-community`: Para carregamento de documentos e integração com o Qdrant.
  * `qdrant-client`: Para o banco de dados vetorial em memória.
  * `huggingface-hub` e `sentence-transformers`: Para os embeddings do HuggingFace.
  * `python-dotenv`: Para gerenciar variáveis de ambiente (sua API Key).
  * `gradio`: Para a interface do usuário dos chatbots.
  * `unstructured` (e suas dependências como `markdown`, `lxml`, etc.): Para carregar documentos `.md` e `.docx`.

### 4\. Obter e Configurar a Chave da API Gemini

Para usar o Gemini, você precisará de uma chave de API:

1.  Acesse o Google AI Studio: [https://aistudio.google.com/](https://aistudio.google.com/)

2.  Crie ou selecione um projeto.

3.  Gere uma nova chave de API.

4.  Crie um arquivo `.env` na **raiz do seu projeto** (na mesma pasta onde está este README).

5.  Adicione sua chave de API a este arquivo no formato:

    ```
    GEMINI_API_KEY=SUA_CHAVE_API_AQUI
    ```

    **Importante**: Não suba seu arquivo `.env` para o GitHub\! Adicione-o ao seu `.gitignore`.

### 5\. Preparar os Documentos de Contexto Pedagógico

Os chatbots utilizam documentos de contexto para suas respostas.

  * **Para o Chat de Matemática:**

      * O documento esperado é `contexto_pedagogico.md` (ou `.txt`, `.docx`) na pasta `mat_rag/documentos/`.
      * Caminho no código: `base_path = "/home/laza/chat_RAG_hf/api/chat_05_MAT/documentos/contexto_pedagogico"`

  * **Para o Chat de Língua Portuguesa:**

      * O documento esperado é `contexto_pedagogico.md` (ou `.txt`, `.docx`) na pasta `port_rag/documentos/`.
      * Caminho no código: `base_path = "/home/laza/mat_port_rag/port_rag/documentos/contexto_pedagogico"`

    **Verifique os caminhos nos arquivos `interface_gradio.py` de cada módulo (`mat_rag/interface` e `port_rag/interface`) para garantir que `CONTEXT_DOC_BASE_PATH` aponte para o local correto do seu documento de contexto.**

### 6\. Executar os Chatbots

Você pode rodar os chatbots separadamente, navegando para a pasta específica de cada um:

  * **Para o Chat de Matemática:**

    ```bash
    cd mat_rag/interface
    python interface_gradio.py
    ```

  * **Para o Chat de Língua Portuguesa:**

    ```bash
    cd port_rag/interface
    python interface_gradio.py
    ```

Após executar, uma URL local (geralmente `http://127.0.0.1:7860`) será exibida no seu terminal. Abra-a no navegador para interagir com o chatbot.

-----

## 📚 Parte Pedagógica: Contexto e Aplicação

Este projeto não é apenas uma demonstração técnica, mas uma ferramenta pedagógica projetada para auxiliar professores na **análise contextualizada do desempenho de seus estudantes** em Matemática e Língua Portuguesa.

### O Desafio Pedagógico

No cotidiano escolar, professores frequentemente se deparam com a necessidade de **avaliar profundamente** as respostas dos alunos, compreendendo não apenas o resultado final, mas o **processo de pensamento** por trás delas. Isso é particularmente desafiador em turmas grandes ou quando as respostas são complexas e multifacetadas, como na resolução de problemas matemáticos ou na análise de textos.

Um feedback eficaz e personalizado requer que o professor tenha em mente **critérios de avaliação claros** e seja capaz de **correlacionar as respostas dos estudantes** a esses critérios, identificando lacunas e pontos fortes específicos.

### A Solução com RAG e IA Generativa

É aqui que nossos chatbots entram em ação, utilizando a arquitetura **Retrieval-Augmented Generation (RAG)** e a **Inteligência Artificial Generativa (Gemini API)** para criar um contexto específico para o professor.

1.  **Contexto Pedagógico (Os "Documentos de Conhecimento"):**

      * Cada chatbot é alimentado com um **documento de contexto pedagógico detalhado** (como os que você forneceu para Matemática e Língua Portuguesa). Estes documentos contêm:
          * **Critérios de Análise:** Descrições claras das habilidades esperadas dos estudantes (e.g., etapas de compreensão, estratégia, cálculo/análise).
          * **Níveis de Classificação:** Escalas que permitem ao professor categorizar o desempenho do estudante (e.g., Iniciante, Básico, Intermediário, Avançado), com descrições específicas para cada nível em relação aos critérios.
          * **Exemplos de Problemas e Respostas Esperadas:** Para um baseline de comparação.
          * **Respostas Simuladas de Estudantes:** Exemplos práticos de como os estudantes respondem, que o chat pode usar para análise.

2.  **O Processo RAG:**

      * Quando um professor insere uma pergunta (por exemplo, "Como devo avaliar a resposta do aluno X para o problema Y de matemática?" ou "Classifique a interpretação de texto do aluno Z conforme os níveis de análise narrativa"), o chatbot não gera uma resposta baseada apenas em seu conhecimento geral.
      * Ele primeiro usa o componente **Retrieval (Recuperação)** do RAG para buscar as informações mais relevantes **dentro do documento de contexto pedagógico** armazenado no banco de dados vetorial (Qdrant). Se o professor perguntar sobre "compreensão" na matemática, o sistema buscará a seção de "Compreensão" e seus níveis correspondentes.
      * Em seguida, essas informações relevantes são passadas para o componente **Generation (Geração)**, que é a API Gemini. A Gemini, agora contextualizada com os critérios pedagógicos específicos, gera uma resposta que não é apenas genérica, mas **diretamente aplicável e fundamentada** nos princípios e classificações definidos no documento de conhecimento.

### Benefícios para o Professor

  * **Feedback Contextualizado:** O professor recebe avaliações e sugestões alinhadas aos critérios pedagógicos específicos do projeto, evitando respostas genéricas de uma IA.
  * **Agilidade na Avaliação:** Ajuda a classificar e compreender o desempenho dos alunos de forma mais rápida, especialmente em cenários com muitas respostas ou complexas.
  * **Padronização da Análise:** Contribui para uma avaliação mais consistente entre diferentes professores ou ao longo do tempo, pois todos os feedbacks são baseados nos mesmos critérios.
  * **Suporte à Tomada de Decisão Pedagógica:** Ao destacar os pontos fortes e as lacunas em cada etapa do processo do estudante, o chatbot empodera o professor com insights acionáveis para planejar intervenções pedagógicas mais direcionadas e eficazes.

Este projeto visa ser um aliado tecnológico para que os educadores possam focar no que fazem de melhor: ensinar e guiar seus estudantes, tendo um suporte inteligente para a desafiadora tarefa da avaliação.

-----

## 💡 Perguntas para Testar os Chats

Use as seguintes perguntas para interagir com os chatbots e explorar suas capacidades:

### Perguntas para o Chat de Matemática

  * `qual a estrutura das atividades de matemática?`
  * `quais os níveis de classificação para a resolução de problemas matemáticos?`
  * `qual o enunciado do problema 1?`
  * `qual a interpretação esperada do problema 1?`
  * `qual a estratégia esperada para o problema 1?`
  * `qual o cálculo esperado para o problema 1?`
  * `qual a resposta final esperada do problema 1?`
  * `quais os nomes dos estudantes que responderam ao problema 1 de matemática?`
  * `em qual nível o/a estudante Ana está classificado(a)?`
  * `qual a interpretação do-da estudante Eduarda?`
  * `qual a estratégia do-da estudante Fernando?`
  * `qual o cálculo do-da estudante Bernardo?`
  * `qual a resposta final do-da estudante Wallace?`

### Perguntas para o Chat de Língua Portuguesa

  * `qual a estrutura das atividades de língua portuguesa?`
  * `quais os níveis de classificação para a análise da narrativa?`
  * `qual o enunciado do problema 1?`
  * `qual a compreensão dos elementos da narrativa esperada para o problema 1?`
  * `qual a compreensão do enredo esperada para o problema 1?`
  * `qual a proposta de solução esperada para o problema 1?`
  * `quais os nomes dos estudantes que responderam ao problema 1 de língua portuguesa?`
  * `qual o nível que o-a estudante Felipe Rocha está classificado(a)?`
  * `qual a compreensão dos elementos da narrativa do(a) estudante Igor Pereira?`
  * `qual a compreensão do enredo do(a) estudante Yuri Castro?`
  * `qual a proposta de solução do(a) estudante Nicole Ferreira?`

-----