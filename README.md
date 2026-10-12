# Visualizador Educacional de Compiladores

Projeto de software educacional interativo para o ensino de disciplinas de Compiladores, focado em demonstrar visualmente as etapas de análise léxica e sintática.

## 1. Escopo Tecnológico e Pedagógico

### Linguagem Escolhida: Mini-C
A linguagem alvo de análise para este projeto será um subconjunto da linguagem C, que chamaremos de **Mini-C**. 

**Subconjunto inicial abordado:**
- **Tipos de dados:** Declaração de variáveis primitivas (`int`, `float`).
- **Operadores:** Aritméticos básicos (`+`, `-`, `*`, `/`) e de atribuição (`=`).
- **Estruturas de controle:** Condicionais simples (`if`, `else`).

**Justificativa:** A escolha da linguagem C (neste caso, simplificada) deve-se à sua proximidade com a arquitetura de hardware, forte tipagem estática e sintaxe amplamente conhecida no meio acadêmico. Isso facilita a compreensão de como o código é efetivamente transformado em árvores sintáticas (AST). A limitação do escopo para "Mini-C" garante a viabilidade do projeto, permitindo foco exclusivo na didática da transição entre a teoria de autômatos e a prática computacional, sem a sobrecarga de lidar com as regras de uma linguagem completa.

## 2. Estrutura do Projeto
- `backend/`: API em Python (FastAPI) responsável por executar as análises de compilação.
- `frontend/`: Interface de usuário interativa em Python (Streamlit).
- `docker-compose.yml`: Arquivo de orquestração dos contêineres.

## 3. Guia de Execução

### Comandos de Inicialização
Para construir e rodar o projeto de forma limpa, abra o terminal na raiz do repositório e execute:

```bash
docker-compose up --build -d
cat << 'EOF' > README.md
# Visualizador Educacional de Compiladores

Projeto de software educacional interativo para o ensino de disciplinas de Compiladores, focado em demonstrar visualmente as etapas de análise léxica e sintática.

## 1. Escopo Tecnológico e Pedagógico

### Linguagem Escolhida: Mini-C
A linguagem alvo de análise para este projeto será um subconjunto da linguagem C, que chamaremos de **Mini-C**. 

**Subconjunto inicial abordado:**
- **Tipos de dados:** Declaração de variáveis primitivas (`int`, `float`).
- **Operadores:** Aritméticos básicos (`+`, `-`, `*`, `/`) e de atribuição (`=`).
- **Estruturas de controle:** Condicionais simples (`if`, `else`).

**Justificativa:** A escolha da linguagem C (neste caso, simplificada) deve-se à sua proximidade com a arquitetura de hardware, forte tipagem estática e sintaxe amplamente conhecida no meio acadêmico. Isso facilita a compreensão de como o código é efetivamente transformado em árvores sintáticas (AST). A limitação do escopo para "Mini-C" garante a viabilidade do projeto, permitindo foco exclusivo na didática da transição entre a teoria de autômatos e a prática computacional, sem a sobrecarga de lidar com as regras de uma linguagem completa.

## 2. Estrutura do Projeto
- `backend/`: API em Python (FastAPI) responsável por executar as análises de compilação.
- `frontend/`: Interface de usuário interativa em Python (Streamlit).
- `docker-compose.yml`: Arquivo de orquestração dos contêineres.

## 3. Guia de Execução

### Comandos de Inicialização
Para construir e rodar o projeto de forma limpa, abra o terminal na raiz do repositório e execute:

```bash
docker-compose up --build -d
