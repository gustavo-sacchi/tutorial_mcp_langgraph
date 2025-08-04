# Tutorial MCP + LangGraph

Este projeto demonstra como integrar o **Model Context Protocol (MCP)** com **LangGraph** para criar um agente ReAct inteligente que pode acessar dados financeiros em tempo real.

## Objetivo

- Como criar um servidor MCP com ferramentas personalizadas
- Como conectar um agente LangGraph ao servidor MCP
- Como implementar memoria de conversacao persistente
- Como usar ferramentas de analise financeira via MCP

## Pre-requisitos

- Python 3.13+
- Chaves de API do OpenAI e/ou Groq
- FastMCP
- LangGraph MCP Adapter

## Instalacao

### 1. Instalar UV (Gerenciador de Pacotes Python)

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clonar e Configurar o Projeto

```bash
# Clone o repositorio
git clone https://github.com/seu-usuario/tutorial_mcp_langgraph.git
cd tutorial_mcp_langgraph

# Instale as dependencias e crie o ambiente virtual
uv sync

# Configure as variaveis de ambiente
cp .env.exemple .env
```

### 3. Configurar Chaves de API

Edite o arquivo `.env` e adicione suas chaves:

```bash
OPENAI_API_KEY=sua-chave-openai-aqui
GROQ_API_KEY=sua-chave-groq-aqui
```

## Como Usar

### 1. Iniciar o Servidor MCP

Em um terminal:

```bash
uv run server_mcp.py
```

O servidor estara disponivel em `http://localhost:4200`

### 2. Executar o Cliente (Agente)

Em outro terminal:

```bash
uv run client_mcp.py
```

### 3. Interagir com o Agente

Agora voce pode fazer perguntas sobre financas:

```
User: Qual e o preco atual da acao da Apple?
User: Me de um resumo completo da VALE3.SA
User: Pesquise noticias recentes sobre investimentos em IA
```

## Testando o MCP

Para testar a interface MCP diretamente:

```bash
npx @modelcontextprotocol/inspector uv run server_mcp.py
```

## Arquitetura

```
┌─────────────────┐    HTTP     ┌─────────────────┐
│  Client         │◄──────────►│  MCP Server     │
│  (LangGraph)    │             │  (FastMCP)      │
│                 │             │                 │
│ • ChatOpenAI    │             │ • YFinance      │
│ • ReAct Agent   │             │ • DuckDuckGo    │
│ • Memory        │             │ • Web Scraping  │
└─────────────────┘             └─────────────────┘
```

## Ferramentas Disponiveis

O servidor MCP fornece estas ferramentas financeiras:

- **Resumo de Acoes**: Preco, volume e data
- **Estimativas de Analistas**: Precos-alvo
- **Recomendacoes**: Buy/Hold/Sell
- **Dividendos**: Historico de pagamentos
- **Setor/Industria**: Classificacao da empresa
- **Demonstracoes Financeiras**: Balanco, DRE, Fluxo de Caixa
- **Pesquisa Web**: Noticias e conteudo relevante

## Video Tutorial

Este projeto foi criado para acompanhar o tutorial no YouTube. Assista ao video completo para entender todos os detalhes da implementacao:

**[📺 Assistir no YouTube](https://youtu.be/UDk9iUY5Yz4)**

## Personalizacao

- **Modelos**: Altere entre OpenAI e Groq no `client_mcp.py`
- **Transporte**: Configure HTTP ou stdio no `server_mcp.py`
- **Ferramentas**: Adicione novas ferramentas MCP no servidor
- **Prompts**: Customize os prompts disponiveis