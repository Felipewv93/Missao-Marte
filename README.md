# Missão Marte: ECLSS

[![Testes ECLSS](https://github.com/Felipewv93/Missao-Marte/actions/workflows/pipeline.yml/badge.svg)](https://github.com/Felipewv93/Missao-Marte/actions/workflows/pipeline.yml)

Projeto prático **ECLSS** (*Environmental Control and Life Support System*) do Habitat de Marte, que faz parte da disciplina de **Automação de Testes de Software**. O projeto reúne testes unitários, integração com mocks, automação web com Selenium, cenários BDD e integração contínua com GitHub Actions.

## Objetivos

- Validar o consumo de oxigênio e água por astronauta e por dia.
- Validar estoque insuficiente e exceções customizadas.
- Calcular taxas de emergência e aplicar cotas de racionamento.
- Isolar a telemetria espacial durante os testes unitários.
- Testar a solicitação de oxigênio pelo painel web.
- Descrever cenários normais e de crise usando Gherkin.
- Executar a suíte automaticamente em Python 3.12 na integração contínua.
- Manter a cobertura do código de `src/` em 100%.

## Requisitos

- Python 3.10 ou superior;
- Google Chrome instalado para o teste Selenium;
- conexão com a internet na primeira execução do Selenium, para o Selenium
  Manager localizar o driver compatível;
- dependências listadas em [requirements.txt](requirements.txt).

## Estrutura do projeto

```text
projeto-missao-marte/
├── .github/
│   └── workflows/
│       └── pipeline.yml
├── assets/
│   └── Exercício ATS13.pdf
├── src/
│   ├── __init__.py
│   ├── gerenciador_recursos.py
│   └── servico_telemetria.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_gerenciador.py
│   ├── test_selenium_e2e.py
│   ├── test_bdd.py
│   └── features/
│       └── solicitacao_oxigenio.feature
├── web/
│   └── painel.html
├── requirements.txt
└── README.md
```

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/Felipewv93/Missao-Marte.git
cd Missao-Marte
```

É recomendado criar um ambiente virtual.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Executando os testes

Na raiz do projeto, execute toda a suíte com relatório de cobertura:

```bash
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=100
```

O parâmetro `--cov-fail-under=100` faz a execução falhar caso a cobertura do
código em `src/` fique abaixo de 100%.

Para executar os testes sem cobertura:

```bash
python -m pytest -v
```

Para executar somente os testes do gerenciador:

```bash
python -m pytest tests/test_gerenciador.py -v
```

Para executar somente os cenários BDD:

```bash
python -m pytest tests/test_bdd.py -v
```

Para executar somente o teste E2E:

```bash
python -m pytest tests/test_selenium_e2e.py -v
```

## Componentes e testes

### Gerenciador de recursos

O [GerenciadorRecursosMarte](src/gerenciador_recursos.py) concentra as regras
de negócio:

- consumo diário de oxigênio e água;
- verificação do estoque durante o consumo;
- `OxigenioInsuficienteError` e `AguaInsuficienteError`;
- cálculo da taxa de emergência;
- `NivelEmergenciaInvalidoError`;
- aplicação da cota de racionamento;
- solicitação de cota extra de oxigênio.

O arquivo [test_gerenciador.py](tests/test_gerenciador.py) utiliza:

- fixture de módulo para os parâmetros iniciais do habitat;
- fixture de função para criar um gerenciador limpo em cada teste;
- `yield` na preparação da fixture;
- `pytest.mark.parametrize` para vários consumos e taxas;
- `pytest.raises` para as regras de erro;
- `mocker.patch` e `assert_called_once_with` para validar a telemetria;
- testes integrados com a implementação local da telemetria.

### Telemetria

O [ServicoTelemetriaEspacial](src/servico_telemetria.py) representa a
dependência externa que envia relatórios de status e alertas de crise para a
estação na Terra. Nos testes unitários, suas chamadas são substituídas por
mocks para que a regra de negócio não dependa de comunicação externa real.

### Painel web e Selenium

O [painel.html](web/painel.html) mostra os níveis atuais de oxigênio e água e
permite solicitar uma cota extra de oxigênio.

O [test_selenium_e2e.py](tests/test_selenium_e2e.py):

- cria uma fixture de navegador;
- executa o Chrome em modo headless;
- preenche e envia o formulário;
- usa `WebDriverWait` e `expected_conditions`;
- verifica a atualização do nível no DOM;
- encerra o navegador com `driver.quit()`;
- salva `evidencia-falha-painel.png` quando uma validação falha.

### BDD

Os cenários estão descritos em português no arquivo
[solicitacao_oxigenio.feature](tests/features/solicitacao_oxigenio.feature).
Eles cobrem:

- solicitação aprovada em condição normal;
- consumo aprovado em condição normal;
- solicitação inválida;
- alerta de crise;
- consumo rejeitado por falta de oxigênio.

Os passos são implementados com `given`, `when` e `then` no arquivo
[test_bdd.py](tests/test_bdd.py).

## Integração contínua

O workflow [pipeline.yml](.github/workflows/pipeline.yml) é executado em
`push` e `pull_request`. Ele:

1. faz checkout com `actions/checkout@v4`;
2. configura Python 3.12 com `actions/setup-python@v5`;
3. instala as dependências;
4. executa todos os testes;
5. exibe a cobertura no terminal;
6. falha se a cobertura de `src/` for menor que 100%.

## Autor

**Felipe Viana**