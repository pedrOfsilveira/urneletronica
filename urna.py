import aroeira as ar

UF = "RS"
URL_FOTOS = "https://resultados.tse.jus.br/oficial/ele2026/"

cargos = [
    "DEPUTADO FEDERAL",
    "DEPUTADO ESTADUAL",
    "SENADOR",
    "SENADOR",
    "GOVERNADOR",
    "PRESIDENTE",
]

digitos = [4, 5, 3, 3, 2, 2]

candidatos = {}
votos = []
elementos_painel = []
caixas_numeros = []

etapa = 0
numero_digitado = ""
tipo_voto = ""
primeiro_senador = ""
estado = "digitando"
quadros = 0
texto_aviso = None


def carregar_candidatos(uf):
    caminho = "consulta_cand_2026/consulta_cand_2026_" + uf + ".csv"
    arquivo = open(caminho, encoding="latin-1")
    cabecalho = arquivo.readline().strip().replace('"', "").split(";")

    coluna_cargo = cabecalho.index("DS_CARGO")
    coluna_numero = cabecalho.index("NR_CANDIDATO")
    coluna_nome = cabecalho.index("NM_URNA_CANDIDATO")
    coluna_partido = cabecalho.index("SG_PARTIDO")
    coluna_eleicao = cabecalho.index("CD_ELEICAO")
    coluna_regiao = cabecalho.index("SG_UE")
    coluna_codigo = cabecalho.index("SQ_CANDIDATO")

    for linha in arquivo:
        campos = linha.strip().replace('"', "").split(";")
        chave = campos[coluna_cargo] + ";" + campos[coluna_numero]
        eleicao = campos[coluna_eleicao]
        regiao = campos[coluna_regiao].lower()
        codigo = campos[coluna_codigo]
        foto = URL_FOTOS + eleicao + "/fotos/" + regiao + "/" + codigo + ".jpeg"

        if chave not in candidatos:
            candidatos[chave] = {
                "nome": campos[coluna_nome],
                "partido": campos[coluna_partido],
                "foto": foto,
            }

    arquivo.close()


def buscar_candidato(cargo, numero):
    chave = cargo + ";" + numero
    if chave in candidatos:
        return candidatos[chave]
    return None


def adicionar_ao_painel(elemento):
    tela.adicionar(elemento)
    elementos_painel.append(elemento)


def mostrar_texto(x, y, conteudo, tamanho=35, negrito=False):
    texto = ar.Texto(ar.Ponto(x, y), conteudo, tamanho, "preto", negrito)
    adicionar_ao_painel(texto)
    return texto


def limpar_painel():
    for elemento in elementos_painel:
        tela.remover(elemento)
    elementos_painel.clear()
    caixas_numeros.clear()


def iniciar_cargo():
    global numero_digitado, tipo_voto, estado, quadros

    limpar_painel()
    numero_digitado = ""
    tipo_voto = ""
    estado = "digitando"
    quadros = 0
    texto_cargo.conteudo = cargos[etapa].title()

    for posicao in range(digitos[etapa]):
        caixa = ar.Retangulo(
            ar.Ponto(40 + posicao * 60, 100),
            largura=50,
            altura=70,
            cor="branco",
            borda="preto",
            espessura_borda=3,
        )
        adicionar_ao_painel(caixa)
        caixas_numeros.append(caixa)


def mostrar_acompanhante(cargo, numero, titulo, y):
    candidato = buscar_candidato(cargo, numero)
    if candidato is not None:
        texto = titulo + candidato["nome"] + " (" + candidato["partido"] + ")"
        mostrar_texto(37, y, texto, 30)


def mostrar_candidato(cargo, numero):
    candidato = buscar_candidato(cargo, numero)

    if candidato is None:
        mostrar_texto(37, 190, "NÚMERO ERRADO", 45)
        mostrar_texto(250, 600, "VOTO NULO", 50, True)
        return "nulo"

    if etapa == 3 and numero == primeiro_senador:
        mostrar_texto(37, 190, "CANDIDATO REPETIDO", 45)
        mostrar_texto(250, 600, "VOTO NULO", 50, True)
        return "nulo"

    mostrar_texto(37, 220, candidato["nome"], 35, True)
    mostrar_texto(37, 310, candidato["partido"])
    foto = ar.Imagem(ar.Ponto(1000, 100), candidato["foto"], largura=250, altura=320)
    adicionar_ao_painel(foto)

    if cargo == "GOVERNADOR":
        mostrar_acompanhante("VICE-GOVERNADOR", numero, "Vice: ", 400)
    elif cargo == "PRESIDENTE":
        mostrar_acompanhante("VICE-PRESIDENTE", numero, "Vice: ", 400)
    elif cargo == "SENADOR":
        mostrar_acompanhante("1º SUPLENTE", numero, "1º suplente: ", 400)
        mostrar_acompanhante("2º SUPLENTE", numero, "2º suplente: ", 490)

    return "valido"


def iniciar_conferencia():
    global estado, quadros, texto_aviso

    estado = "conferindo"
    quadros = 0
    linha = ar.Linha(ar.Ponto(10, 700), ar.Ponto(900, 700), espessura=4)
    adicionar_ao_painel(linha)
    texto_aviso = mostrar_texto(37, 710, "CONFIRA SEU VOTO", 35, True)


def digitar_numero(numero):
    global numero_digitado, tipo_voto

    if estado != "digitando":
        return

    posicao = len(numero_digitado)
    caixas_numeros[posicao].borda = "preto"
    numero_digitado = numero_digitado + str(numero)
    mostrar_texto(50 + posicao * 60, 95, str(numero), 50, True)

    if len(numero_digitado) == digitos[etapa]:
        tipo_voto = mostrar_candidato(cargos[etapa], numero_digitado)
        iniciar_conferencia()


def digitar_zero():
    digitar_numero(0)


def digitar_um():
    digitar_numero(1)


def digitar_dois():
    digitar_numero(2)


def digitar_tres():
    digitar_numero(3)


def digitar_quatro():
    digitar_numero(4)


def digitar_cinco():
    digitar_numero(5)


def digitar_seis():
    digitar_numero(6)


def digitar_sete():
    digitar_numero(7)


def digitar_oito():
    digitar_numero(8)


def digitar_nove():
    digitar_numero(9)


def votar_em_branco():
    global tipo_voto

    if estado != "digitando" or numero_digitado != "":
        return

    limpar_painel()
    tipo_voto = "branco"
    mostrar_texto(170, 290, "VOTO EM BRANCO", 60, True)
    iniciar_conferencia()


def corrigir():
    if estado == "digitando" or estado == "pronto":
        iniciar_cargo()


def salvar_votos():
    arquivo = open("apuracao.csv", "a", encoding="utf-8")
    for voto in votos:
        arquivo.write(voto + ",")
    arquivo.write("\n")
    arquivo.close()
    votos.clear()


def confirmar():
    global etapa, primeiro_senador, estado, quadros

    if estado != "pronto":
        return

    if numero_digitado == "":
        votos.append(tipo_voto)
    else:
        votos.append(numero_digitado)

    if etapa == 2 and tipo_voto == "valido":
        primeiro_senador = numero_digitado

    etapa = etapa + 1

    if etapa < len(cargos):
        iniciar_cargo()
    else:
        salvar_votos()
        limpar_painel()
        texto_cargo.conteudo = ""
        mostrar_texto(200, 200, "FIM", 80, True)
        estado = "fim"
        quadros = 0


def atualizar_tela():
    global quadros, estado, etapa, primeiro_senador

    quadros = quadros + 1

    if estado == "conferindo" and quadros >= 50:
        estado = "pronto"
        texto_aviso.conteudo = "Aperte a tecla:"
        mostrar_texto(130, 770, "CONFIRMA para CONFIRMAR este voto")
        mostrar_texto(165, 830, "CORRIGE para REINICIAR este voto")
    elif estado == "fim" and quadros >= 120:
        etapa = 0
        primeiro_senador = ""
        iniciar_cargo()
    elif estado == "digitando" and quadros % 20 == 0:
        caixa = caixas_numeros[len(numero_digitado)]
        if caixa.borda == "preto":
            caixa.borda = "cinza"
        else:
            caixa.borda = "preto"


carregar_candidatos(UF)
carregar_candidatos("BR")

tela = ar.Tela("Urna", 1920, 1000, "cinza")
fundo = ar.Retangulo(
    ar.Ponto(10, 10),
    largura=1300,
    altura=990,
    cor="branco",
    borda="preto",
    espessura_borda=4,
)
tela.adicionar(fundo)

texto_cargo = ar.Texto(ar.Ponto(37, 15), "", 45, "preto", True)
tela.adicionar(texto_cargo)

moldura = ar.Retangulo(
    ar.Ponto(1375, 280),
    largura=500,
    altura=475,
    cor="#212121",
    borda="#616161",
    espessura_borda=3,
)
tela.adicionar(moldura)

titulo_teclado = ar.Texto(ar.Ponto(1540, 300), "TECLADO DE VOTAÇÃO", 15, "branco", True)
tela.adicionar(titulo_teclado)

acoes_numeros = [
    digitar_um,
    digitar_dois,
    digitar_tres,
    digitar_quatro,
    digitar_cinco,
    digitar_seis,
    digitar_sete,
    digitar_oito,
    digitar_nove,
]

for posicao in range(9):
    coluna = posicao % 3
    linha = posicao // 3
    ponto = ar.Ponto(1400 + coluna * 155, 350 + linha * 65)
    botao = ar.Botao(
        ponto, str(posicao + 1), acoes_numeros[posicao], "preto", "branco", 140
    )
    tela.adicionar(botao)

botao_zero = ar.Botao(ar.Ponto(1555, 545), "0", digitar_zero, "preto", "branco", 140)
botao_branco = ar.Botao(
    ar.Ponto(1400, 625), "BRANCO", votar_em_branco, "branco", "preto", 225
)
botao_corrige = ar.Botao(
    ar.Ponto(1640, 625), "CORRIGE", corrigir, "laranja", "preto", 225
)
botao_confirma = ar.Botao(
    ar.Ponto(1400, 690), "CONFIRMA", confirmar, "verde", "branco", 450
)

for botao in [botao_zero, botao_branco, botao_corrige, botao_confirma]:
    tela.adicionar(botao)

iniciar_cargo()
tela.animar(atualizar_tela, fps=60)
tela.executar()
