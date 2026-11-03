from .servico_telemetria import ServicoTelemetriaEspacial


class OxigenioInsuficienteError(Exception):
    pass


class AguaInsuficienteError(Exception):
    pass


class NivelEmergenciaInvalidoError(ValueError):
    pass


class GerenciadorRecursosMarte():
    consumo_oxigenio = 2.5
    consumo_agua = 3.0

    def __init__(self, oxigenio, agua, telemetria=None):
        if oxigenio < 0 or agua < 0:
            raise ValueError("Os recursos iniciais não podem ser negativos")

        self.oxigenio = float(oxigenio)
        self.agua = float(agua)
        self.telemetria = telemetria or ServicoTelemetriaEspacial()

    def calcular_consumo_diario(self, astronautas, dias=1):
        if astronautas < 0 or dias < 0:
            raise ValueError("Astronautas e dias devem ser não negativos")

        return {"oxigenio": astronautas * dias * self.consumo_oxigenio, "agua": astronautas * dias * self.consumo_agua,}

    def calcular_taxa_emergencia(self, dias_restantes, minimo_dias=10):
        if dias_restantes < 0 or minimo_dias <= 0:
            raise NivelEmergenciaInvalidoError("Os dias devem ser válidos")

        taxa = (minimo_dias - dias_restantes) / minimo_dias
        return round(max(0, min(1, taxa)), 2)

    def aplicar_cota_racionamento(self, consumo, taxa):
        if taxa < 0 or taxa > 1:
            raise NivelEmergenciaInvalidoError("A taxa deve estar entre 0 e 1")

        return {recurso: round(valor * (1 - taxa), 2) for recurso, valor in consumo.items()}

    def consumir(self, astronautas, dias=1):
        consumo = self.calcular_consumo_diario(astronautas, dias)

        if self.oxigenio < consumo["oxigenio"]:
            raise OxigenioInsuficienteError("Oxigênio insuficiente")
        if self.agua < consumo["agua"]:
            raise AguaInsuficienteError("Água insuficiente")

        self.oxigenio -= consumo["oxigenio"]
        self.agua -= consumo["agua"]
        return consumo

    def solicitar_cota_extra_oxigenio(self, quantidade):
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero")

        self.oxigenio += quantidade
        status = self.obter_status()
        self.telemetria.enviar_relatorio_status(status)
        return status

    def monitorar_emergencia(self, dias_restantes):
        taxa = self.calcular_taxa_emergencia(dias_restantes)

        if taxa > 0:
            self.telemetria.disparar_alerta_crise("Nível de recursos em estado de emergência", taxa)

        return taxa

    def obter_status(self):
        return {"oxigenio": round(self.oxigenio, 2), "agua": round(self.agua, 2),}
