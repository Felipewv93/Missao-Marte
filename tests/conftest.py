import pytest
from pathlib import Path
from src.gerenciador_recursos import GerenciadorRecursosMarte
from src.servico_telemetria import ServicoTelemetriaEspacial


@pytest.fixture(scope="module")
def parametros_habitat():

    return {"oxigenio": 1000, "agua": 2000}


@pytest.fixture(scope="function")
def gerenciador(parametros_habitat):

    telemetria = ServicoTelemetriaEspacial()
    gestor = GerenciadorRecursosMarte(parametros_habitat["oxigenio"], parametros_habitat["agua"], telemetria)
    
    yield gestor


@pytest.fixture
def painel_path():

    return Path(__file__).parents[1] / "web" / "painel.html"
