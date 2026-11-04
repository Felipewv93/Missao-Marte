# language: pt

Funcionalidade: Solicitação de oxigênio
  Como astronauta do Habitat de Marte
  Quero solicitar uma cota extra de oxigênio
  Para manter a tripulação em segurança

  Cenário: Solicitação aprovada em condição normal
    Dado o habitat possui 1000 kg de oxigênio
    Quando a tripulação solicita 100 kg de oxigênio
    Então o estoque de oxigênio deve ser 1100 kg

  Cenário: Consumo aprovado em condição normal
    Dado o habitat possui 1000 kg de oxigênio
    Quando 4 astronautas consomem recursos durante 2 dias
    Então o estoque de oxigênio deve ser 980 kg

  Cenário: Solicitação rejeitada com quantidade inválida
    Dado o habitat possui 1000 kg de oxigênio
    Quando a tripulação solicita 0 kg de oxigênio
    Então a solicitação deve ser rejeitada

  Cenário: Alerta disparado em condição de crise
    Dado o habitat possui 1000 kg de oxigênio
    Quando o habitat possui apenas 2 dias de recursos
    Então um alerta de crise deve ser enviado com taxa 0.8

  Cenário: Consumo rejeitado em condição de crise
    Dado o habitat possui 5 kg de oxigênio
    Quando 4 astronautas consomem recursos durante 2 dias
    Então o consumo deve ser rejeitado por falta de oxigênio