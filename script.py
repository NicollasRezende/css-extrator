from rich.prompt import Prompt
from rich.console import Console
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import os
import requests

# Constantes
DEFAULT_DOWNLOAD_DIR = "css_downloads"
DEVTOOLS_WAIT_TIME = 2
POPUP_DELAY = 1000

# Configuração do Console Rich
console = Console()

def configurar_firefox_options() -> Options:
    """Configura as opções do Firefox para DevTools."""
    options = Options()
    options.set_preference("devtools.toolbox.host", "window")
    options.set_preference("devtools.toolbox.previousHost", "window")
    options.set_preference("devtools.toolbox.selectedTool", "styleeditor")
    options.set_preference("devtools.chrome.enabled", True)
    options.add_argument("--devtools")
    return options

def iniciar_driver() -> webdriver.Firefox:
    """Inicializa e retorna o driver do Firefox com as configurações necessárias."""
    options = configurar_firefox_options()
    service = Service("geckodriver")
    return webdriver.Firefox(service=service, options=options)

def contar_arquivos_css(driver: webdriver.Firefox) -> int:
    """Conta o número de arquivos CSS na página."""
    return driver.execute_script("""
        try {
            return document.styleSheets.length;
        } catch(e) {
            console.error(e);
            return 0;
        }
    """)

def fechar_devtools_mostrar_alerta(driver: webdriver.Firefox) -> None:
    """Fecha o DevTools e mostra alerta para voltar ao terminal."""
    driver.execute_script(f"""
        if (window.windowUtils) {{
            window.windowUtils.closeToolbox();
        }}
        setTimeout(() => {{
            alert('Por favor, volte ao terminal para continuar!');
        }}, {POPUP_DELAY});
    """)

def baixar_arquivos_css(driver: webdriver.Firefox, pasta_destino: str = DEFAULT_DOWNLOAD_DIR) -> list:
    """
    Obtém e baixa os arquivos CSS da página.
    
    Args:
        driver: Instância do Firefox WebDriver
        pasta_destino: Caminho da pasta para download dos arquivos
        
    Returns:
        list: Lista de URLs dos arquivos CSS encontrados
    """
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    css_urls = driver.execute_script("""
        return Array.from(document.styleSheets)
            .filter(sheet => sheet.href)
            .map(sheet => sheet.href);
    """)
    
    for url in css_urls:
        try:
            nome_arquivo = url.split('/')[-1]
            caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
            
            response = requests.get(url)
            response.raise_for_status()
            
            with open(caminho_arquivo, 'wb') as f:
                f.write(response.content)
            
            console.print(f"[green]✓ Baixado: {nome_arquivo}[/green]")
        
        except Exception as e:
            console.print(f"[red]✗ Erro ao baixar {url}: {str(e)}[/red]")
    
    return css_urls

def main():
    """Função principal do programa."""
    try:
        url = Prompt.ask("\n[bold cyan]Digite a URL do site que deseja acessar[/bold cyan]")
        
        console.print("\n[bold green]Iniciando navegador...[/bold green]")
        driver = iniciar_driver()
        
        try:
            console.print(f"\n[bold yellow]Acessando {url}...[/bold yellow]")
            driver.get(url)
            time.sleep(DEVTOOLS_WAIT_TIME)
            
            num_arquivos = contar_arquivos_css(driver)
            fechar_devtools_mostrar_alerta(driver)
            
            console.print(f"\n[bold green]Encontrados {num_arquivos} arquivos CSS[/bold green]")
            
            if num_arquivos > 0:
                resposta = Prompt.ask(
                    "\n[bold yellow]Deseja baixar os arquivos CSS encontrados?[/bold yellow]",
                    choices=["s", "n"],
                    default="n"
                ).lower()
                
                if resposta == 's':
                    css_urls = baixar_arquivos_css(driver)
                    console.print("\n[bold green]Download concluído![/bold green]")
            
            input("\nPressione ENTER para fechar...")
            
        finally:
            driver.quit()
            
    except Exception as e:
        console.print(f"[bold red]Erro:[/bold red] {str(e)}")

if __name__ == "__main__":
    main()