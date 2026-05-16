from pile import Pile
import state as estado


def criar_torre(num_discos):
    """
    Cria a plataforma com os discos da torre no pino 0
    :param num_discos: número de discos a criar
    :return: lista contendo as pilhas que representam os pinos
    """
    # Reinicia estado da plataforma por cada novo jogo
    estado.plataforma = [Pile(), Pile(), Pile()]
    for n in range(num_discos):
        estado.plataforma[0].push(num_discos - n)
    return estado.plataforma


def validar_movimento(pino_destino):
    if estado.plataforma[pino_destino].size() <= 1:
        return True
    topo = estado.plataforma[pino_destino].pop()
    abaixo = estado.plataforma[pino_destino].peek()
    estado.plataforma[pino_destino].push(topo)
    if topo > abaixo:
        return False
    return True


def desfazer_movimento(pino_origem, pino_destino):
    """
    Desfaz o último movimento feito
    :param pino_origem: o índice do pino de origem
    :param pino_destino: o índice do pino de destino
    :return: None
    """
    disco = estado.plataforma[pino_destino].pop()
    estado.plataforma[pino_origem].push(disco)


def mover_disco(pino_origem, pino_destino):
    """
    Lógica para mover um disco de um pino de origem para um pino de destino
    :param pino_origem: a posição na lista que identifica o pino de origem
    :param pino_destino: a posição na lista que identifica o pino de destino
    :return: True se o movimento é válido, False caso contrário
    """
    try:
        disco = estado.plataforma[pino_origem].peek()
        # Executa o movimento
        estado.plataforma[pino_destino].push(disco)
        estado.plataforma[pino_origem].pop()
        # Valida após mover
        valido = validar_movimento(pino_destino)
        # Movimento válido
        if valido:
            return True, False
        # Movimento inválido
        return False, True
    except IndexError:
        return False, False


def checar_torre(torre, num_discos):
    """
    Verifica o estado dos pinos 1 e 2 para ver se a torre foi montada nelas
    :param torre: lista que contém as pilhas que representam os pinos
    :param num_discos: número de discos que devem estar no pino
    :return: True caso a torre esteja montada no pino 1 ou 2, False caso contrário
    """
    return (
            torre[1].size() == num_discos or
            torre[2].size() == num_discos
    )
