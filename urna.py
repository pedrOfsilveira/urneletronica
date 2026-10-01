import aroeira as ar

UF = "RS"

tela = ar.Tela("Urna", 960, 540, "cinza")
stringVoto = ""
contagem = 0
pronto = False
tipo_voto = ""
aguardando_conferencia = False
ticks_conferencia = 0
texto_conferencia = None
painel_elementos = []
numtextos = []
em_fim = False
ticks_fim = 0
voto_senador_1 = ""

tecladoX = 580
tecladoY = 150

nomes_cargo = [
    "Deputado Federal",
    "Deputado Estadual",
    "Senador",
    "Senador",
    "Governador",
    "Presidente",
]

cargos_csv = [
    "DEPUTADO FEDERAL",
    "DEPUTADO ESTADUAL",
    "SENADOR",
    "SENADOR",
    "GOVERNADOR",
    "PRESIDENTE",
]

digitos_cargo = [4, 5, 3, 3, 2, 2]

chaves_apuracao = [
    "Deputado Federal",
    "Deputado Estadual",
    "Senador (1º voto)",
    "Senador (2º voto)",
    "Governador",
    "Presidente",
]

apuracao = {}
votosAnotados = []
candidatos = {}

for chave in chaves_apuracao:
    apuracao[chave] = {"valido": 0, "branco": 0, "nulo": 0}


def ler_csv(nome_arquivo):
    arquivo = open(nome_arquivo, encoding="latin-1")
    cabecalho = arquivo.readline()
    colunas = cabecalho.replace('"', "").split(";")

    i_cargo = colunas.index("DS_CARGO")
    i_numero = colunas.index("NR_CANDIDATO")
    i_nome = colunas.index("NM_URNA_CANDIDATO")
    i_partido = colunas.index("SG_PARTIDO")

    linha = arquivo.readline()
    while linha != "":
        campos = linha.replace('"', "").split(";")
        cargo = campos[i_cargo]
        numero = campos[i_numero]
        nome = campos[i_nome]
        partido = campos[i_partido]
        chave = cargo + ";" + numero

        if chave not in candidatos:
            candidatos[chave] = [nome, partido]

        linha = arquivo.readline()

    arquivo.close()


ler_csv("consulta_cand_2026/consulta_cand_2026_" + UF + ".csv")
ler_csv("consulta_cand_2026/consulta_cand_2026_BR.csv")


def bip():
    print("bip")


def limpar_painel():
    global stringVoto, pronto, tipo_voto, aguardando_conferencia, ticks_conferencia
    global texto_conferencia

    for elemento in numtextos:
        tela.remover(elemento)
    numtextos.clear()

    for elemento in painel_elementos:
        tela.remover(elemento)
    painel_elementos.clear()

    stringVoto = ""
    pronto = False
    tipo_voto = ""
    aguardando_conferencia = False
    ticks_conferencia = 0
    texto_conferencia = None


def colocar_texto(x, y, texto, tamanho, negrito):
    item = ar.Texto(ar.Ponto(x, y), texto, tamanho, "preto", negrito)
    tela.adicionar(item)
    painel_elementos.append(item)


def buscar(cargo, numero):
    chave = cargo + ";" + numero
    if chave in candidatos:
        return candidatos[chave]
    return None


def mostrar_candidato(cargo, numero):
    dados = buscar(cargo, numero)
    if dados == None:
        colocar_texto(20, 120, "NÚMERO ERRADO", 22, True)
        colocar_texto(20, 155, "VOTO NULO", 18, True)
        return "nulo"

    colocar_texto(20, 120, dados[0], 22, True)
    colocar_texto(20, 150, dados[1], 18, False)

    if cargo == "GOVERNADOR":
        vice = buscar("VICE-GOVERNADOR", numero)
        if vice != None:
            colocar_texto(20, 180, "Vice: " + vice[0] + " (" + vice[1] + ")", 16, False)
    elif cargo == "PRESIDENTE":
        vice = buscar("VICE-PRESIDENTE", numero)
        if vice != None:
            colocar_texto(20, 180, "Vice: " + vice[0] + " (" + vice[1] + ")", 16, False)
    elif cargo == "SENADOR":
        s1 = buscar("1º SUPLENTE", numero)
        s2 = buscar("2º SUPLENTE", numero)
        y = 180
        if s1 != None:
            colocar_texto(20, y, "1º suplente: " + s1[0] + " (" + s1[1] + ")", 16, False)
            y = y + 24
        if s2 != None:
            colocar_texto(20, y, "2º suplente: " + s2[0] + " (" + s2[1] + ")", 16, False)

    return "valido"


def iniciar_conferencia():
    global aguardando_conferencia, ticks_conferencia, texto_conferencia

    aguardando_conferencia = True
    ticks_conferencia = 0
    texto_conferencia = ar.Texto(
        ar.Ponto(20, 250), "CONFIRA SEU VOTO", 18, "preto", True
    )
    tela.adicionar(texto_conferencia)
    painel_elementos.append(texto_conferencia)


def finalizar_conferencia():
    global aguardando_conferencia, pronto, texto_conferencia

    if texto_conferencia != None:
        tela.remover(texto_conferencia)
        painel_elementos.remove(texto_conferencia)
        texto_conferencia = None

    aguardando_conferencia = False
    pronto = True


def voto(num):
    global stringVoto, tipo_voto

    if em_fim or pronto or aguardando_conferencia or tipo_voto != "":
        return

    max_digitos = digitos_cargo[contagem]
    if len(stringVoto) >= max_digitos:
        bip()
        return

    stringVoto = stringVoto + str(num)
    item = ar.Texto(
        ar.Ponto(20 + len(stringVoto) * 30, 60), str(num), 25, "preto", True
    )
    numtextos.append(item)
    tela.adicionar(item)

    if len(stringVoto) == max_digitos:
        cargo = cargos_csv[contagem]
        tipo_voto = mostrar_candidato(cargo, stringVoto)
        iniciar_conferencia()


def num0():
    voto(0)


def num1():
    voto(1)


def num2():
    voto(2)


def num3():
    voto(3)


def num4():
    voto(4)


def num5():
    voto(5)


def num6():
    voto(6)


def num7():
    voto(7)


def num8():
    voto(8)


def num9():
    voto(9)


def branco():
    global tipo_voto

    if em_fim or aguardando_conferencia:
        return
    if stringVoto != "" or tipo_voto != "":
        bip()
        return

    tipo_voto = "branco"
    colocar_texto(20, 120, "VOTO EM BRANCO", 22, True)
    iniciar_conferencia()


def corrige():
    if em_fim or aguardando_conferencia:
        return
    limpar_painel()


def registrar_voto():
    global voto_senador_1

    chave = chaves_apuracao[contagem]
    apuracao[chave][tipo_voto] = apuracao[chave][tipo_voto] + 1

    texto = chave + ": " + tipo_voto
    if stringVoto != "":
        texto = texto + " " + stringVoto
    votosAnotados.append(texto)

    if contagem == 2 and tipo_voto == "valido":
        voto_senador_1 = stringVoto


def confirma():
    global contagem, voto_senador_1, em_fim, ticks_fim

    if em_fim or aguardando_conferencia:
        return
    if not pronto:
        bip()
        return

    if contagem == 3 and tipo_voto == "valido" and stringVoto == voto_senador_1:
        bip()
        return

    registrar_voto()

    if contagem == len(nomes_cargo) - 1:
        limpar_painel()
        textocandidato.conteudo = ""
        colocar_texto(200, 200, "FIM", 80, True)
        em_fim = True
        ticks_fim = 0
        return

    limpar_painel()
    contagem = contagem + 1
    textocandidato.conteudo = nomes_cargo[contagem]


def tick_urna():
    global ticks_fim, ticks_conferencia, contagem, voto_senador_1, em_fim

    if aguardando_conferencia:
        ticks_conferencia = ticks_conferencia + 1
        if ticks_conferencia >= 60:
            finalizar_conferencia()
        return

    if not em_fim:
        return

    ticks_fim = ticks_fim + 1
    if ticks_fim >= 120:
        limpar_painel()
        contagem = 0
        voto_senador_1 = ""
        em_fim = False
        textocandidato.conteudo = nomes_cargo[0]


def salvar_apuracao():
    arquivo = open("apuracao.txt", "w")
    arquivo.write("APURACAO DA SESSAO\n")
    arquivo.write("UF: " + UF + "\n\n")

    for i in range(len(chaves_apuracao)):
        cargo = chaves_apuracao[i]
        arquivo.write(cargo + "\n")
        arquivo.write("  Validos: " + str(apuracao[cargo]["valido"]) + "\n")
        arquivo.write("  Brancos: " + str(apuracao[cargo]["branco"]) + "\n")
        arquivo.write("  Nulos: " + str(apuracao[cargo]["nulo"]) + "\n\n")

    arquivo.write("VOTOS REGISTRADOS\n")
    for i in range(len(votosAnotados)):
        arquivo.write(votosAnotados[i] + "\n")

    arquivo.close()


def ao_fechar():
    salvar_apuracao()


textocandidato = ar.Texto(
    ar.Ponto(20, 20), nomes_cargo[contagem], 25, "preto", True
)
tela.adicionar(textocandidato)

botao1 = ar.Botao(ar.Ponto(tecladoX, tecladoY), "1", num1, "preto")
botao2 = ar.Botao(ar.Ponto(tecladoX + 60, tecladoY), "2", num2, "preto")
botao3 = ar.Botao(ar.Ponto(tecladoX + 120, tecladoY), "3", num3, "preto")
botao4 = ar.Botao(ar.Ponto(tecladoX, tecladoY + 40), "4", num4, "preto")
botao5 = ar.Botao(ar.Ponto(tecladoX + 60, tecladoY + 40), "5", num5, "preto")
botao6 = ar.Botao(ar.Ponto(tecladoX + 120, tecladoY + 40), "6", num6, "preto")
botao7 = ar.Botao(ar.Ponto(tecladoX, tecladoY + 80), "7", num7, "preto")
botao8 = ar.Botao(ar.Ponto(tecladoX + 60, tecladoY + 80), "8", num8, "preto")
botao9 = ar.Botao(ar.Ponto(tecladoX + 120, tecladoY + 80), "9", num9, "preto")
botao0 = ar.Botao(ar.Ponto(tecladoX + 60, tecladoY + 120), "0", num0, "preto")
botaobranco = ar.Botao(
    ar.Ponto(tecladoX + 180, tecladoY),
    "BRANCO",
    branco,
    "branco",
    "preto",
)
botaocorrige = ar.Botao(
    ar.Ponto(tecladoX + 180, tecladoY + 40), "CORRIGE", corrige, "laranja", "preto"
)
botaoconfirma = ar.Botao(
    ar.Ponto(tecladoX + 180, tecladoY + 80), "CONFIRMA", confirma, "verde", "preto"
)

tela.adicionar(botao1)
tela.adicionar(botao2)
tela.adicionar(botao3)
tela.adicionar(botao4)
tela.adicionar(botao5)
tela.adicionar(botao6)
tela.adicionar(botao7)
tela.adicionar(botao8)
tela.adicionar(botao9)
tela.adicionar(botao0)
tela.adicionar(botaobranco)
tela.adicionar(botaocorrige)
tela.adicionar(botaoconfirma)

tela.ao_fechar(ao_fechar)
tela.animar(tick_urna, fps=60)
tela.executar()
