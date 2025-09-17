from random import choice

listaAtaques = []
cods = 0

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

class Criatura:
    def __init__(obj, nome):
        obj.nome = nome
        obj.vidamax = 0
        obj.vida = [0,0] #pontos de vida atuais/pontos de vida temporários
        obj.armadura = 10
        obj.atrs = {
            "FOR": 10,
            "DES": 10,
            "CON": 10,
            "INT": 10,
            "SAB": 10,
            "CON": 10
        }
        obj.cod = 0
        obj.ataqTur = 1

        obj.caracs = []
        obj.ataques = []
        obj.inventario = []
        obj.fraq, obj.resists, obj.imunis = [], [], []

    def setAtrs(obj, f, d, con, i, s, car):
        obj.atrs = {
            "FOR": f,
            "DES": d,
            "CON": con,
            "INT": i,
            "SAB":s,
            "CAR": car
        }

        obj.armadura += obj.atrs['DES']

class Personagem(Criatura):
    def __init__(obj, nome, raca, classe, nvl):
        super().__init__(nome)
        if raca in listaraca:
            obj.raca = raca
        else:
            obj.raca = choice(listaraca)
        obj.classe = classe
        obj.adiClasse()
        obj.nvl = nvl
        obj.adiClasse()
        cods+=1
        obj.cod = cods
        Ataque("Ataque Desarmado", "1d4", "Concussivo", "FOR").adiAtaque(obj)

    def adiClasse(obj):
        match obj.classe:
            case "Barbáro":
                obj.vidamax = 10
            case "Bardo":
                pass
            case "Bruxo":
                pass
            case "Clérigo":
                pass
            case "Druida":
                pass
            case "Feiticeiro":
                pass
            case "Guerreiro":
                pass
            case "Ladino":
                pass
            case "Mago":
                pass
            case "Monge":
                pass
            case "Paladino":
                pass
            case "Patrulheiro":
                pass
            case __:
                obj.classe = choice(listaclasses)
                print(F"A classe de {obj.nome} se tornou '{obj.classe}'")
                obj.adiClasse()

class Item:
    def __init__(obj, nome, desc):
        obj.nome = nome
        obj.desc = desc
    
    def adiItem(obj, perso):
        perso.inventario.append(obj)
    
    def perdeItem(obj, perso):
        i = encontraObj(obj, perso.inventario)
        if i != "Não":
            del perso.inventario[i]
        else:
            print("Esse personagem não tem este item")

class Arma(Item):
    def __init__(obj, nome, desc, dano, tipo):
        super().__init__(nome, desc)
        obj.dano = dano.lower() + " " + tipo.lower()
    
    def adiItem(obj, perso):
        super().adiItem(perso)
        espaco = obj.dano.index(" ")
        perso.ataques.append(Ataque(obj.nome, obj.dano[:espaco], obj.dano[(espaco+1):]))
    
    def perdeItem(obj, perso):
        super().perdeItem(perso)
        i = encontraObj(obj, perso.ataques)
        if i != "Não":
            del perso.ataques[i]
        else:
            print("O personagem não tem o ataque dessa arma")

class Ataque:
    def __init__(obj, nome, dano, tipo, atrbon="", bonusbase=0):
        obj.nome = nome
        obj.qtdado, obj.dado, obj.bonus = 0, 0, 0
        obj.tipo = "concussivo"
        if tipo in listatipos: obj.tipo = tipo.lower()
        obj.iniciaDano(dano.lower())
        obj.bonusbase = bonusbase
        obj.atrbon = atrbon
        obj.perso = None
        listaAtaques.append(obj)

    def iniciaDano(obj, dano):
        d = dano.index('d')
        if '+' in dano: b = dano.index('+')
        else: b = 0

        obj.qtdado = int(dano[:d])
        if b: obj.dado = int(dano[(d+1):b])
        else: obj.dado = int(dano[(d+1):])
        if b: obj.bonus = int(dano[(b+1):])
    
    def adiAtaque(obj, perso):
        obj.perso = perso.cod
        perso.ataques.append(obj.nome)

    #MUDARRRRRRRRRRRRRRRRRRR
    def perdeAtaque(obj, perso):
        i = encontraObj(obj, perso.ataques)
        if i != "Não":
            del perso.ataques[i]
        else:
            print("Esse personagem não tem este ataque")

    def __str__(obj):
        if obj.bonus > 0: bon = '+'+str(obj.bonus)+'atrbon'
        else: bon = ''
        return f"O ataque '{obj.nome}' dá {obj.qtdado}d{obj.dado}{bon} de dano {obj.tipo}"

class Caracteristica:
    def __init__(obj, nome, desc):
        obj.nome = nome
        obj.desc = desc

    def adiCarac(obj, perso):
        perso.caracs.append(obj)
    
    def perdeCarac(obj, perso):
        perso.caracs
    
    def __str__(obj):
        return f"Essa Carcterística não tem efeitos mecânicos"

class LinguaDeVeludo(Caracteristica):
    def __init__(obj):
        super().__init__("Língua de Veludo", "O personagem é um safado")


def encontraObj(elemento, lista):
    index = "Não"

    for e in range(len(lista)):
        if lista[e].nome == elemento.nome:
            index = e
            break

    return index

link = Personagem("Link", "Elfo", "Guerreiro", 15)
Arma("Espada maneira", "Uma espada muito maneira", "1d12+3", "Cortante").adiItem(link)
Item("Poção de vida", "Uma poção que faz alguma coisa").adiItem(link)

print([x.nome for x in link.inventario], [x.nome for x in link.ataques])
Arma("Espada maneira", "Uma espada muito maneira", "1d12+3", "Cortante").perdeItem(link)
print([x.nome for x in link.inventario], [x.nome for x in link.ataques])
