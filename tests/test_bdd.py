import pytest
from pytest_bdd import given, parsers, scenarios, then, when
from src.gerenciador_recursos import GerenciadorRecursosMarte, OxigenioInsuficienteError
from src.servico_telemetria import ServicoTelemetriaEspacial


scenarios("features/solicitacao_oxigenio.feature")


@pytest.fixture
def contexto():
    return {}


@given(parsers.parse("o habitat possui {quantidade:g} kg de oxigênio"))
def habitat_com_oxigenio(contexto, quantidade):
    contexto["gestor"] = GerenciadorRecursosMarte(quantidade, 2000, ServicoTelemetriaEspacial())


@when(parsers.parse("a tripulação solicita {quantidade:g} kg de oxigênio"))
def tripulacao_solicita(contexto, quantidade):
    try:
        contexto["resultado"] = contexto["gestor"].solicitar_cota_extra_oxigenio(quantidade)
    except ValueError:
        contexto["rejeitada"] = True


@when(parsers.parse("{astronautas:d} astronautas consomem recursos durante {dias:d} dias"))
def astronautas_consumem(contexto, astronautas, dias):
    try:
        contexto["consumo"] = contexto["gestor"].consumir(astronautas, dias)
    except OxigenioInsuficienteError as erro:
        contexto["erro"] = erro


@when(parsers.parse("o habitat possui apenas {dias:d} dias de recursos"))
def habitat_em_crise(contexto, dias):
    contexto["taxa"] = contexto["gestor"].monitorar_emergencia(dias)


@then(parsers.parse("o estoque de oxigênio deve ser {esperado:g} kg"))
def estoque_deve_ser(contexto, esperado):
    if "resultado" in contexto:
        assert contexto["resultado"]["oxigenio"] == esperado
    else:
        assert contexto["gestor"].obter_status()["oxigenio"] == esperado


@then("a solicitação deve ser rejeitada")
def solicitacao_rejeitada(contexto):
    assert contexto["rejeitada"] is True


@then(parsers.parse("um alerta de crise deve ser enviado com taxa {taxa:g}"))
def alerta_de_crise(contexto, taxa):
    assert contexto["taxa"] == taxa
    assert len(contexto["gestor"].telemetria.alertas) == 1


@then("o consumo deve ser rejeitado por falta de oxigênio")
def consumo_rejeitado(contexto):
    assert contexto["erro"].__class__.__name__ == "OxigenioInsuficienteError"
