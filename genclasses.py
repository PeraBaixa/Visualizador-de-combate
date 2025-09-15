from random import choice

listatipos = [
    "concussivo",
    "cortante",
    "perfurante",
    "ácido",
    "elétrico",
    "energético",
    "ígneo",
    "gélido",
    "necrótico",
    "psíquico",
    "radiante",
    "trovejante",
    "venenoso"
    ]

listaraca = [
    "Anão",
    "Elfo",
    "Halfling",
    "Humano",
    "Draconato",
    "Gnomo",
    "Orc",
    "Tiefling"
]

listaclasses = [
    "Bárbaro",
    "Bardo",
    "Bruxo",
    "Clérigo",
    "Druida",
    "Feiticeiro",
    "Guerreiro",
    "Ladino",
    "Mago",
    "Monge",
    "Paladino",
    "Patrulheiro"
]

class Personagem:
    def __init__(obj, nome, raca, classe, nvl):
        obj.nome = nome
        if raca in listaraca:
            obj.raca = raca
        else:
            obj.raca = choice(listaraca)
        if classe in listaclasses:
            obj.classe = classe
        else:
            obj.classe = choice(listaclasses)
        obj.nvl = nvl

        obj.caracs = []
        obj.ataques = []
        obj.inventorio = []
        obj.fraq, obj.resists, obj.imunis = [], [], []

class Item:
    def __init__(obj, nome, desc):
        obj.nome = nome
        obj.desc = desc
    
    def adiItem(obj, perso):
        perso.inventorio.append(obj)

class Arma(Item):
    def __init__(obj, nome, desc, dano, tipo):
        super().__init__(nome, desc)
        obj.dano = dano.lower() + " " + tipo.lower()
    
    def adiItem(obj, perso):
        super().adiItem(perso)
        espaco = obj.dano.index(" ")
        perso.ataques.append(Ataque(obj.nome, obj.dano[:espaco], obj.dano[(espaco+1):]))

class Ataque:
    def __init__(obj, nome, dano, tipo, bonusbase=0):
        obj.nome = nome
        obj.qtdado, obj.dado, obj.bonus = 0, 0, 0
        obj.tipo = "concussivo"
        if tipo in listatipos: obj.tipo = tipo.lower()
        obj.iniciaDano(dano.lower())
        obj.bonusbase = bonusbase

    def iniciaDano(obj, dano):
        d = dano.index('d')
        if '+' in dano: b = dano.index('+')
        else: b = 0

        obj.qtdado = int(dano[:d])
        if b: obj.dado = int(dano[(d+1):b])
        else: obj.dado = int(dano[(d+1):])
        if b: obj.bonus = int(dano[(b+1):])
    
    def __str__(obj):
        if obj.bonus > 0: bon = '+'+str(obj.bonus)
        else: bon = ''
        return f"O ataque '{obj.nome}' dá {obj.qtdado}d{obj.dado}{bon} de dano {obj.tipo}"

class Caracteristica:
    def __init__(obj):
        pass

link = Personagem("Link", "Elfo", "Guerreiro", 15)
Arma("Espada maneira", "Uma espada muito maneira", "1d12+3", "Cortante").adiItem(link)

print(link.ataques[0].tipo)