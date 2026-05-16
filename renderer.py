import pygame

import state as estado
from constants import *
from screens import calcular_largura_prop_disco, desenhar_rodape


def disco_rect(pos_peg, pos_pilha, valor_disco, num_discos):
    """
    Retorna o Rect (objeto retangular) de um disco na pilha (stack_pos=0 é o fundo).
    :param pos_peg: posição do pino na plataforma (pilha)
    :param pos_pilha: posição do disco na pilha (disco)
    :param valor_disco: o valor númerico atribuído ao disco
    :param num_discos: o número de discos
    :return: o objeto retangular do pygame com as dimensões proporcionais ao seu valor de disco e na posição correta
    """
    # Calculo da largura proporcional do disco
    w = calcular_largura_prop_disco(valor_disco, num_discos)
    # Calculo da posição do disco no pino (em qual pino na plataforma)
    x = PEG_X[pos_peg] - w // 2
    # Calculo da posição do disco na pilha (em qual altura do pino)
    y = BASE_Y - BASE_H - (pos_pilha + 1) * (DISK_H + DISK_GAP)
    # Cria o objeto no espaço correto com as dimensões corretas
    return pygame.Rect(x, y, w, DISK_H)


def desenhar_rect(surf, color, rect, radius=10, shadow=True):
    """
    Função para desenhar o objeto retangular estilizado na tela
    O retângulo pode possuir:
    - cantos arredondados;
    - sombra projetada;
    - efeito de brilho (highlight) na parte superior.
    :param surf: Superfície principal onde o objeto será desenhado
    :param color: Cor principal do retângulo no formato RGB
    :param rect: Objeto pygame.Rect contendo: posição (X, Y), largura (w) e altura (h) do objeto
    :param radius: Define o arredondamento das bordas do retângulo
    :param shadow: Se True, desenha uma sombra atrás do retângulo
    :return: None
    """
    if shadow:
        # Cria um novo retângulo levemente deslocado em relação ao original, simulando a posição da sombra
        sr = rect.move(3, 4)
        # Cria uma superfície transparente (canal alpha) com mesmo tamanho da sombra
        s = pygame.Surface((sr.w, sr.h), pygame.SRCALPHA)
        # Desenha a sombra usando preto semi-transparente, o valor 80 representa a opacidade (alpha)
        pygame.draw.rect(s, (0, 0, 0, 80), s.get_rect(), border_radius=radius)
        # Renderiza a superfície da sombra sobre a superfície principal
        surf.blit(s, sr.topleft)
    # Desenha o retângulo principal com cantos arredondados
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    # Cria um pequeno retângulo na parte superior do objeto (efeito highlight)
    hl = pygame.Rect(rect.x + 4, rect.y + 3, rect.w - 8, 5)
    # Desenha o highlight com bordas levemente arredondadas enquanto clareia a cor original do objeto
    pygame.draw.rect(surf, tuple(min(c + 60, 255) for c in color), hl, border_radius=4)


def criar_cena(surf, num_discos, font_sm, font_md,
               font_lg, font_xs, dragging, drag_disk, drag_pos, drag_origin,
               contador, min_move, state, hover_peg, mensagem):
    """
    Renderiza todos os elementos visuais da cena do jogo
    :param surf: Superfície principal onde todos os elementos serão desenhados
    :param num_discos: Número de discos
    :param font_sm: Fonte pequena utilizada em textos auxiliares e rótulos
    :param font_md: Fonte média utilizada em mensagens de estado
    :param font_lg: Fonte grande utilizada no título do jogo
    :param font_xs: Fonte do texto de rodapé
    :param dragging: Flag se o jogador está arrastando um disco no momento
    :param drag_disk: Valor do disco atualmente sendo arrastado
    :param drag_pos: Posição atual do mouse durante o arrasto do disco
    :param drag_origin: Índice do pino de origem do disco arrastado
    :param contador: Número atual de movimentos realizados pelo jogador
    :param min_move: Quantidade mínima de movimentos necessária para resolver o jogo
    :param state: Estado atual do jogo ('playing', 'win', 'lose')
    :param hover_peg: Índice do pino atualmente destacado pelo mouse, None caso nenhum esteja em destaque
    :param mensagem: Mensagem para jogadas inválidas
    :return: None
    """
    # Preenche o background com cor definida
    surf.fill(BG)

    # Renderiza título do jogo
    title = font_lg.render('Torre de Hanói', True, ACCENT)
    # Centraliza o texto do título na tela
    surf.blit(title, (W // 2 - title.get_width() // 2, 18))

    # Renderiza texto com contador e mínimo de movimentos
    info = font_sm.render(
        f'Movimentos: {contador}   |   Mínimo: {min_move}', True, TEXT_COL)
    # Centraliza o texto na tela
    surf.blit(info, (W // 2 - info.get_width() // 2, 60))

    # Desenha a plataforma (base) e os pinos (peg)
    for i, px in enumerate(PEG_X):
        # Destaca visualmente o pino quando o mouse está sobre ele enquanto um disco está sendo arrastado
        if hover_peg == i and dragging:
            glow = pygame.Surface((BASE_W + 20, BASE_H + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*ACCENT, 50), glow.get_rect(), border_radius=12)
            surf.blit(glow, (px - BASE_W // 2 - 10, BASE_Y - BASE_H // 2 - 10))

        # Cria o retângulo da base do pino
        base_rect = pygame.Rect(px - BASE_W // 2, BASE_Y - BASE_H // 2, BASE_W, BASE_H)
        # Desenha a base
        desenhar_rect(surf, BASE_COL, base_rect, radius=8)

        # Cria o retângulo vertical do pino
        peg_rect = pygame.Rect(px - PEG_W // 2, BASE_Y - BASE_H - PEG_H, PEG_W, PEG_H)
        # Desenha o pino
        pygame.draw.rect(surf, PEG_COL, peg_rect, border_radius=6)

        # Cria o texto do rótulo do pino
        lbl = font_sm.render(f'Pino {i}', True, PEG_COL)
        # Desenha o rótulo abaixo do pino
        surf.blit(lbl, (px - lbl.get_width() // 2, BASE_Y + 16))

    # Discos em cada pino
    for pi in range(3):
        # Obtém a lista de discos do pino atual
        items = estado.plataforma[pi].items
        for si, dv in enumerate(items):
            # Se o disco estiver sendo arrastado, não desenha o disco do topo no pino de origem
            if dragging and pi == drag_origin and si == len(items) - 1:
                continue
            # Calcula o retângulo do disco
            r = disco_rect(pi, si, dv, num_discos)
            # Escolhe a cor do disco
            col = DISK_COLORS[(dv - 1) % len(DISK_COLORS)]
            # Desenha o disco
            desenhar_rect(surf, col, r, radius=8)
            # Cria o texto identificador do disco
            lbl = font_sm.render(str(dv), True, (255, 255, 255))
            # Centraliza e desenha o número do disco
            surf.blit(lbl, (r.centerx - lbl.get_width() // 2,
                            r.centery - lbl.get_height() // 2))

    # Disco sendo arrastado
    if dragging and drag_disk is not None:
        # Calcula a largura proporcional do disco
        w = calcular_largura_prop_disco(drag_disk, num_discos)
        # Cria o retângulo do disco seguindo o mouse
        r = pygame.Rect(drag_pos[0] - w // 2, drag_pos[1] - DISK_H // 2, w, DISK_H)
        # Escolhe a cor do disco
        col = DISK_COLORS[(drag_disk - 1) % len(DISK_COLORS)]
        # Desenha o disco com sombra
        desenhar_rect(surf, col, r, radius=8, shadow=True)
        # Cria o texto do número do disco
        lbl = font_sm.render(str(drag_disk), True, (255, 255, 255))
        # Centraliza e desenha o número no disco
        surf.blit(lbl, (r.centerx - lbl.get_width() // 2,
                        r.centery - lbl.get_height() // 2))

    # Mensagem de estado
    if state == 'win':
        # Mensagem de vitória
        msg = font_md.render('Parabéns! Resolvido no mínimo de movimentos!', True, WIN_COL)
        surf.blit(msg, (W // 2 - msg.get_width() // 2, H - 150))
    elif state == 'lose':
        # Mensagem de derrota
        linha1 = font_md.render('Game Over!', True, LOSE_COL)
        linha2 = font_sm.render(
            'Você atingiu o número mínimo de movimentos',
            True,
            LOSE_COL
        )
        linha3 = font_sm.render(
            'sem completar a solução.',
            True,
            LOSE_COL
        )

        surf.blit(linha1, (W // 2 - linha1.get_width() // 2, H - 150))
        surf.blit(linha2, (W // 2 - linha2.get_width() // 2, H - 125))
        surf.blit(linha3, (W // 2 - linha3.get_width() // 2, H - 110))
    elif state == 'playing':
        if mensagem:
            msg = font_sm.render(mensagem, True, LOSE_COL)
            surf.blit(msg, (W // 2 - msg.get_width() // 2, H - 120))
        # Mensagem de instrução durante o jogo
        hint = font_sm.render('Arraste um disco de um pino para outro', True, (120, 110, 160))
        surf.blit(hint, (W // 2 - hint.get_width() // 2, H - 550))

    if state in ('win', 'lose'):
        # Mensagem de reinício
        restart = font_sm.render('Pressione R para reiniciar', True, (180, 170, 220))
        surf.blit(restart, (W // 2 - restart.get_width() // 2, H - 550))

    desenhar_rodape(surf, font_sm, font_xs)
