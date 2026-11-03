class ServicoTelemetriaEspacial():
    def __init__(self) -> None:
        self.relatorios = []
        self.alertas = []

    def enviar_relatorio_status(self, status):
        self.relatorios.append(status)
        return True

    def disparar_alerta_crise(self, mensagem, taxa_emergencia):
        self.alertas.append({"mensagem": mensagem, "taxa_emergencia": taxa_emergencia})
        return True
