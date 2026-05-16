import asyncio
import pygame

from constants import *


def calcular_largura_prop_disco(valor_disco, num_discos):
    """
    Calcula a largura proporcional ao valor do disco.
    :param valor_disco: o valor do disco de 1 a num_discos
    :param num_discos: quantos discos foram criados
    :return: o valor que deve ser usado para a largura do disco
    """
    razao = valor_disco / num_discos
    return int(MIN_DISK_W + razao * (MAX_DISK_W - MIN_DISK_W))


def peg_at(mx):
    """
    Calcula qual o pino mais próximo do mouse
    :param mx: posição x do mouse
    :return: o índice do pino mais próximo ou None
    """
    for i, px in enumerate(PEG_X):
        if abs(mx - px) < BASE_W // 2:
            return i
    return None


def tela_input(surf, font_lg, font_md,
               font_sm, font_xs, value_str, error):
    """
    Renderiza a tela inicial de entrada de dados do jogo
    :param surf: Superfície principal onde os elementos serão desenhados
    :param font_sm:  Fonte pequena utilizada em mensagens auxiliares e de erro
    :param font_md: Fonte média utilizada no texto de solicitação do número de discos
    :param font_lg: Fonte grande utilizada no título principal e no valor digitado
    :param font_xs: Fonte utilizada para o rodapé
    :param value_str: Texto digitado pelo usuário representando a quantidade de discos
    :param error: Mensagem de erro exibida caso o valor informado seja inválido
    :return: None
    """
    # Preenche o background
    surf.fill(BG)
    # Renderiza título do jogo
    t = font_lg.render('Torre de Hanói', True, ACCENT)
    # Centraliza o texto na tela
    surf.blit(t, (W // 2 - t.get_width() // 2, 120))

    # Renderiza texto que solicita ao jogador quantidade de discos
    p = font_md.render('Número de discos (1–10): ', True, TEXT_COL)
    # Centraliza o texto na tela
    surf.blit(p, (W // 2 - p.get_width() // 2, 230))

    # Renderiza a caixa de input
    box = pygame.Rect(W // 2 - 80, 285, 160, 52)
    pygame.draw.rect(surf, (35, 30, 60), box, border_radius=10)
    pygame.draw.rect(surf, ACCENT, box, 2, border_radius=10)
    # Renderiza o valor digitado pelo usuário
    val_surf = font_lg.render(value_str if value_str else '_', True, TEXT_COL)
    # Centraliza e desenha o valor dentro da caixa
    surf.blit(val_surf, (box.centerx - val_surf.get_width() // 2,
                         box.centery - val_surf.get_height() // 2))
    # Caso valor digitado seja inválido
    if error:
        # Renderiza o texto de erro
        err = font_sm.render(error, True, LOSE_COL)
        # Centraliza o texto na tela
        surf.blit(err, (W // 2 - err.get_width() // 2, 355))
    # Renderiza texto auxiliar
    hint = font_sm.render('Pressione ENTER para começar', True, (120, 110, 160))
    # Centraliza texto na tela
    surf.blit(hint, (W // 2 - hint.get_width() // 2, 400))
    # Desenha rodapé
    desenhar_rodape(surf, font_sm, font_xs)


async def tela_entrada(surf, font_lg, font_md, font_sm, font_xs):
    """
    Controla a tela de entrada do jogo, a função é responsável por:
    - Capturar o valor digitado pelo usuário;
    - Validar a quantidade de discos informada;
    - Exibir mensagens de erro quando necessário;
    - Atualizar continuamente a interface gráfica até que um valor válido seja fornecido
    :param surf: Superfície principal onde os elementos gráficos serão desenhados
    :param font_lg: Fonte grande utilizada no título e valores destacados
    :param font_md: Fonte média utilizada nos textos principais
    :param font_sm: Fonte pequena utilizada em mensagens auxiliares e erros
    :param font_xs: Fonte do rodapé
    :return: Quantidade de discos válida escolhida pelo jogador
    """
    # Declaração de variáveis iniciais
    num_discos = None
    input_val = ''
    input_err = ''

    # Enquanto usuário não digitar um valor válido, itere
    while num_discos is None:
        # Percorre todos os eventos capturados pelo pygame
        for ev in pygame.event.get():
            # Evento de fechamento de janela
            if ev.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            # Evento interação com teclado
            elif ev.type == pygame.KEYDOWN:
                # Evento de tecla ENTER
                if ev.key == pygame.K_RETURN:
                    # Tente validar entrada
                    if input_val:
                        n = int(input_val)
                        if 1 <= n <= 10:
                            num_discos = n
                        else:
                            input_err = 'Digite um número entre 1 e 10'
                    else:
                        input_err = 'Valor inválido'
                # Evento de tecla BACKSPACE
                elif ev.key == pygame.K_BACKSPACE:
                    # Apaga valores digitados
                    input_val = input_val[:-1]
                # Permite apenas entrada de valores númericos
                elif ev.unicode.isdigit():
                    input_val += ev.unicode

        # Chama função para renderizar a tela
        tela_input(surf, font_lg, font_md, font_sm, font_xs, input_val, input_err)
        # Atualiza o conteúdo exibido na tela
        pygame.display.flip()
        # Controle taxa de atualização
        await asyncio.sleep(1.0 / FPS)

    return num_discos


def desenhar_rodape(surf, font_sm, font_xs):
    """
    Renderiza o rodapé do trabalho na tela
    :param surf: Superfície onde o rodapé vai ser renderizado
    :param font_sm: Fonte pequena auxiliar
    :param font_xs: Fonte do texto do rodapé
    :return: None
    """
    # Cria área do rodapé
    footer_rect = pygame.Rect(0, H - FOOTER_H, W, FOOTER_H)
    # Renderiza o rodapé
    pygame.draw.rect(surf, (22, 18, 44), footer_rect)
    # Linha separadora no topo do rodapé
    pygame.draw.line(surf, ACCENT, (0, H - FOOTER_H), (W, H - FOOTER_H), 1)
    # Linhas a serem escritas
    linha1 = 'Universidade Tecnológica Federal do Paraná (UTFPR) - Campus Londrina'
    linha2 = 'Disciplina: Matemática Discreta  |  Professor: Alireza Mohebi Ashtiani'
    linha3 = 'Discente: Guilherme Sant\'Ana Mathias'
    # Cor das linhas
    cor1 = (160, 150, 210)
    cor2 = (160, 150, 210)
    cor3 = TEXT_COL
    # Define dimensões do rodapé
    y_base = H - FOOTER_H + 12
    for texto, cor, fonte in [
        (linha1, cor1, font_xs),
        (linha2, cor2, font_xs),
        (linha3, cor3, font_sm),
    ]:
        # Renderiza rodapé na tela
        s = fonte.render(texto, True, cor)
        surf.blit(s, (W // 2 - s.get_width() // 2, y_base))
        y_base += fonte.get_height() + 4
