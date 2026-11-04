import pytest
from src.gerenciador_recursos import GerenciadorRecursosMarte, AguaInsuficienteError, NivelEmergenciaInvalidoError, OxigenioInsuficienteError


@pytest.mark.parametrize(("astronautas", "dias", "oxigenio", "agua"), [(1, 1, 2.5, 3), (3, 2, 15, 18), (6, 5, 75, 90)],)
@pytest.mark.parametrize(("dias_restantes", "taxa_esperada"), [(15, 0), (10, 0), (5, 0.5), (0, 1)])
def test_calcula_consumo_e_taxa_de_emergencia(gerenciador, astronautas, dias, oxigenio, agua, dias_restantes, taxa_esperada):
    assert gerenciador.calcular_consumo_diario(astronautas, dias) == {"oxigenio": oxigenio, "agua": agua}
    assert gerenciador.calcular_taxa_emergencia(dias_restantes) == taxa_esperada


def test_recursos_iniciais_negativos():
    with pytest.raises(ValueError):
        GerenciadorRecursosMarte(-1, 100)


@pytest.mark.parametrize(("astronautas", "dias"), [(-1, 1), (1, -1)])
def test_consumo_com_parametros_negativos(gerenciador, astronautas, dias):
    with pytest.raises(ValueError):
        gerenciador.calcular_consumo_diario(astronautas, dias)


@pytest.mark.parametrize(("dias_restantes", "minimo_dias"), [(-1, 10), (1, 0)])
def test_taxa_de_emergencia_com_parametros_invalidos(gerenciador, dias_restantes, minimo_dias):
    with pytest.raises(NivelEmergenciaInvalidoError):
        gerenciador.calcular_taxa_emergencia(dias_restantes, minimo_dias)


def test_aplica_racionamento(gerenciador):
    assert gerenciador.aplicar_cota_racionamento({"oxigenio": 100, "agua": 80}, 0.25) == {"oxigenio": 75, "agua": 60}


def test_consumo_atualiza_estoque(gerenciador):
    assert gerenciador.consumir(2) == {"oxigenio": 5, "agua": 6}
    assert gerenciador.obter_status() == {"oxigenio": 995, "agua": 1994}


def test_oxigenio_insuficiente(gerenciador):
    with pytest.raises(OxigenioInsuficienteError):
        gerenciador.consumir(500)


def test_agua_insuficiente():
    gestor = GerenciadorRecursosMarte(1000, 1)
    with pytest.raises(AguaInsuficienteError):
        gestor.consumir(1)


def test_taxa_invalida(gerenciador):
    with pytest.raises(NivelEmergenciaInvalidoError):
        gerenciador.aplicar_cota_racionamento({"oxigenio": 10}, 1.1)


def test_solicitacao_envia_relatorio_para_telemetria(gerenciador, mocker):
    envio = mocker.patch("src.gerenciador_recursos.ServicoTelemetriaEspacial.enviar_relatorio_status")
    status = gerenciador.solicitar_cota_extra_oxigenio(50)
    envio.assert_called_once_with(status)
    assert status["oxigenio"] == 1050


def test_solicitacao_integrada_registra_relatorio_na_telemetria(gerenciador):
    status = gerenciador.solicitar_cota_extra_oxigenio(50)

    assert gerenciador.telemetria.relatorios == [status]


def test_emergencia_dispara_alerta(gerenciador, mocker):
    alerta = mocker.patch("src.gerenciador_recursos.ServicoTelemetriaEspacial.disparar_alerta_crise")
    taxa = gerenciador.monitorar_emergencia(2)
    alerta.assert_called_once_with("Nível de recursos em estado de emergência", taxa)
    assert taxa == 0.8


def test_emergencia_integrada_registra_alerta(gerenciador):
    taxa = gerenciador.monitorar_emergencia(2)

    assert gerenciador.telemetria.alertas == [{"mensagem": "Nível de recursos em estado de emergência", "taxa_emergencia": taxa}]
