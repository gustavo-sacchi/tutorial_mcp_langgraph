import asyncio
import yfinance as yf

import httpx

from duckduckgo_search import DDGS
from markdownify import markdownify

from fastmcp import FastMCP

mcp = FastMCP("TutorialMCPServer")

## Função auxiliar para acessar sites e converter em Markdown:

def buscar_conteudo_completo_site(url: str):
    """
    Busca o conteúdo HTML de uma URL e o converte para o formato markdown.

    Utiliza um tempo limite de 10 segundos para evitar travamentos em sites lentos ou páginas muito grandes.
    """
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()
            return markdownify(response.text)
    except Exception as e:
        print(f"Aviso: Falha ao buscar o conteúdo completo da página para {url}: {str(e)}")
        return None

## Ferramentas MCPs:

@mcp.tool()
def duckduckgo_pesquisa(consulta: str, max_resultados: int = 2):
    """Realiza uma busca na web usando o DuckDuckGo e retorna os resultados formatados.

    :argument:
        consulta (str): A consulta de busca a ser executada
        max_resultados (int, opcional): Número máximo de resultados a serem retornados. Padrão é 2.

    :return: Dicionário com a resposta da busca contendo.
    """
    try:
        print(f"Ferramenta de pesquisa chamada com - consulta: {consulta} e max_resultados: {max_resultados}")
        with DDGS() as ddgs:
            resultados = []
            resultados_pesquisa = list(ddgs.text(consulta, max_results=max_resultados))

            for r in resultados_pesquisa:
                url = r.get('href')
                titulo = r.get('title')
                conteudo_resumido = r.get('body')

                if not all([url, titulo, conteudo_resumido]):
                    print(f"Aviso: Resultado incompleto do DuckDuckGo. Ignorar: {r}")
                    continue

                conteudo_completo = buscar_conteudo_completo_site(url)

                # Adiciona os resultados na lista de sites pesquisados
                dicionario_resultados = {
                    "titulo": titulo,
                    "url": url,
                    "conteudo_resumido": conteudo_resumido,
                    "conteudo_completo": conteudo_completo
                }
                resultados.append(dicionario_resultados)
            print(f"Ferramenta de pesquisa finalizou - resultados: {resultados}")
            return {"resultados": resultados}
    except Exception as e:
        print(f"Erro em DuckDuckGo: {str(e)}")
        return {"resultados": []}

@mcp.tool()
def busca_resumo_de_acao(ticker: str) -> str:
    """
    Busca um resumo da ação especificada incluindo preço de fechamento, volume e data.
    
    Args:
        ticker (str): Símbolo da ação (ex: 'AAPL', 'VALE3.SA')
    
    Returns:
        str: Resumo formatado com preço de fechamento, volume e data da última negociação
    """
    try:
        print(f"Ferramenta de resumo de ação iniciada - ticker: {ticker}")
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")

        if hist.empty:
            return f"No recent data found for {ticker.upper()}."

        latest = hist.iloc[-1]
        summary = (
            f"{ticker.upper()} Summary:\n"
            f"Close Price: ${latest['Close']:.2f}\n"
            f"Volume: {int(latest['Volume'])}\n"
            f"Date: {latest.name.date()}\n"
        )

        return summary
    except Exception as e:
        return f"Error retrieving stock data for {ticker}: {str(e)}"

@mcp.tool()
def busca_estimativas_de_preco_de_analistas(ticker: str) -> dict:
    """
    Busca as estimativas de preço dos analistas para uma ação específica.
    
    Args:
        ticker (str): Símbolo da ação (ex: 'AAPL', 'VALE3.SA')
    
    Returns:
        dict: Dicionário com as estimativas de preço-alvo dos analistas ou mensagem de erro
    """
    try:
        print(f"Ferramenta de busca_estimativas_de_preco_de_analistas iniciada - ticker: {ticker}")
        stock = yf.Ticker(ticker)
        return stock.analyst_price_targets
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def busca_recomendacoes(ticker: str) -> list:
    """
    Busca as recomendações dos analistas para uma ação específica.
    
    Args:
        ticker (str): Símbolo da ação (ex: 'AAPL', 'VALE3.SA')
    
    Returns:
        list: Lista com as recomendações dos analistas (Buy, Hold, Sell) ou mensagem de erro
    """
    try:
        print(f"Ferramenta de busca_recomendacoes iniciada - ticker: {ticker}")
        stock = yf.Ticker(ticker)
        recs = stock.recommendations
        return recs.to_dict("records") if hasattr(recs, 'to_dict') else list(recs)
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def busca_dividendos(ticker: str) -> dict:
    """
    Busca o histórico de dividendos pagos por uma ação específica.
    
    Args:
        ticker (str): Símbolo da ação (ex: 'AAPL', 'VALE3.SA')
    
    Returns:
        dict: Dicionário com as datas e valores dos dividendos pagos ou mensagem de erro
    """
    try:
        print(f"Ferramenta de busca_dividendos iniciada - ticker: {ticker}")
        stock = yf.Ticker(ticker)
        divs = stock.dividends
        return divs.to_dict() if hasattr(divs, 'to_dict') else dict(divs)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def busca_setor_da_acao(ticker: str) -> dict:
    """
    Busca informações sobre o setor e indústria de uma ação específica.
    
    Args:
        ticker (str): Símbolo da ação (ex: 'AAPL', 'VALE3.SA')
    
    Returns:
        dict: Dicionário com informações do setor e indústria da empresa ou mensagem de erro
    """
    try:
        print(f"Ferramenta de busca_setor_da_acao iniciada - ticker: {ticker}")
        stock = yf.Ticker(ticker)
        info = stock.info
        sector = info.get('sector')
        industry = info.get('industry')
        return {"sector": sector, "industry": industry}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def busca_demonstracoes_financeiras(ticker: str) -> dict:
    """
    Busca as principais demonstrações financeiras de uma empresa.
    
    Args:
        ticker (str): Símbolo da ação (ex: 'AAPL', 'VALE3.SA')
    
    Returns:
        dict: Dicionário contendo balanço patrimonial, demonstração de resultados e fluxo de caixa ou mensagem de erro
    """
    try:
        print(f"Ferramenta de busca_demonstracoes_financeiras iniciada - ticker: {ticker}")
        stock = yf.Ticker(ticker)
        return {
            "balanco_patrimonial": stock.balance_sheet.to_dict() if hasattr(stock.balance_sheet, 'to_dict') else dict(stock.balance_sheet),
            "demonstracao_de_resultados": stock.income_stmt.to_dict() if hasattr(stock.income_stmt, 'to_dict') else dict(stock.income_stmt),
            "fluxo_de_caixa": stock.cashflow.to_dict() if hasattr(stock.cashflow, 'to_dict') else dict(stock.cashflow)
        }
    except Exception as e:
        return {"error": str(e)}

# Servindo Prompts Personalizados

@mcp.prompt()
def prompt_stock_summary(ticker: str) -> str:
    """
    Gera um prompt para solicitar um resumo abrangente de uma ação específica.
    
    Args:
        ticker (str): Símbolo da ação (ex: 'AAPL', 'VALE3.SA')
    
    Returns:
        str: Prompt formatado solicitando resumo completo incluindo preço, volume, notícias e eventos
    """
    return f"Por favor, forneça um resumo abrangente para a ação '{ticker}'. Inclua preço recente, volume, notícias e quaisquer eventos notáveis."

@mcp.prompt()
def prompt_investment_thesis(ticker: str) -> str:
    """
    Gera um prompt para elaborar uma tese de investimento detalhada para uma ação.
    
    Args:
        ticker (str): Símbolo da ação (ex: 'AAPL', 'VALE3.SA')
    
    Returns:
        str: Prompt formatado solicitando análise SWOT e recomendações de analistas
    """
    return f"Elabore uma tese de investimento para '{ticker}'. Inclua forças da empresa, fraquezas, oportunidades, ameaças e um resumo das recomendações recentes dos analistas."


# Executando nosso MCP
if __name__ == "__main__":
    mcp.run(transport="http", port=4200) # transporte via http
    # mcp.run() # transporte via stdio

## Testando o MCP via interface de teste: npx @modelcontextprotocol/inspector uv run server_mcp.py
## Para iniciar o servidor: uv run server_mcp.py