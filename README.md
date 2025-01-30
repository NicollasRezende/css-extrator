
# Documentação do Projeto

## Descrição
Este projeto é um script Python que permite fazer download automático de arquivos CSS de uma página web utilizando Selenium WebDriver com Firefox.

## Requisitos
- Python 3.x
- Bibliotecas Python listadas em 

requirements.txt

:
  - selenium==4.15.2
  - rich==13.7.0 
  - requests==2.31.0
- Firefox instalado
- Geckodriver instalado (

geckodriver

)

## Estrutura do Projeto
```
.
├── css_downloads/      # Pasta onde os arquivos CSS são salvos
├── script.py          # Script principal
└── requirements.txt   # Dependências do projeto
```

## Principais Funções

### 

configurar_firefox_options()


Configura as opções do Firefox para uso do DevTools:

```python
def configurar_firefox_options() -> Options:
    options = Options()
    options.set_preference("devtools.toolbox.host", "window") 
    options.set_preference("devtools.toolbox.selectedTool", "styleeditor")
    options.add_argument("--devtools")
    return options
```

### 

iniciar_driver()


Inicializa o WebDriver do Firefox:

```python
def iniciar_driver() -> webdriver.Firefox:
    options = configurar_firefox_options()
    service = Service("/snap/bin/geckodriver")
    return webdriver.Firefox(service=service, options=options)
```

### 

baixar_arquivos_css()


Faz o download dos arquivos CSS encontrados na página:

```python
def baixar_arquivos_css(driver: webdriver.Firefox, pasta_destino: str = "css_downloads") -> list:
    # Cria pasta se não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        
    # Obtém URLs dos arquivos CSS
    css_urls = driver.execute_script("""
        return Array.from(document.styleSheets)
            .filter(sheet => sheet.href)
            .map(sheet => sheet.href);
    """)
    
    # Faz download dos arquivos
    for url in css_urls:
        try:
            nome_arquivo = url.split('/')[-1]
            caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
            response = requests.get(url)
            response.raise_for_status()
            with open(caminho_arquivo, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            console.print(f"[red]✗ Erro ao baixar {url}: {str(e)}[/red]")
```

## Como Usar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o script:
```bash
python script.py
```

3. Digite a URL do site desejado quando solicitado

4. O script irá:
   - Abrir o Firefox com DevTools
   - Identificar os arquivos CSS
   - Fazer download para a pasta 

css_downloads



## Observações
- O script requer o geckodriver instalado em 

geckodriver


- É necessário ter o Firefox instalado
- Os arquivos são salvos por padrão em 

css_downloads


- Uma interface de linha de comando colorida é fornecida pela biblioteca 

rich


## Constantes
```python
DEFAULT_DOWNLOAD_DIR = "css_downloads"
DEVTOOLS_WAIT_TIME = 2
POPUP_DELAY = 1000
```
