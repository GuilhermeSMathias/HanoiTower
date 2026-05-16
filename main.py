# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────
# Importando bibliotecas
# ─────────────────────────────────────────────
import pygame.freetype

from screens import *
from renderer import *
from game_logic import *
from constants import *


async def main():
    # Inicializa todos os módulos do pygame
    pygame.init()
    # Cria a janela com dimensões pré-definidas
    surf = pygame.display.set_mode((W, H))
    # Display do título do jogo
    pygame.display.set_caption('Torre de Hanói')

    # Define as fontes do jogo
    font_lg = pygame.font.Font(None, 52)
    font_md = pygame.font.Font(None, 36)
    font_sm = pygame.font.Font(None, 26)
    font_xs = pygame.font.Font(None, 20)

    # ── Tela de entrada ──────────────────────────────────────────────
    num_discos = await tela_entrada(surf, font_lg, font_md, font_sm, font_xs)

    # ── Inicializa jogo ──────────────────────────────────────────────
    torre = criar_torre(num_discos)
    min_move = 2 ** num_discos - 1
    contador = 0
    state = 'playing'  # 'playing' | 'win' | 'lose'
    mensagem = ''

    # Inicializa variáveis de controle
    dragging = False
    drag_disk = None
    drag_origin = None
    drag_pos = (0, 0)

    # ── Loop principal ───────────────────────────────────────────────
    while True:
        # Pega posições x e y do mouse na tela
        mx, my = pygame.mouse.get_pos()
        # Pega a posição do pino mais próximo do mouse se ele está arrastando um disco
        hover_peg = peg_at(mx) if dragging else None

        # Percorre todos os eventos capturados pelo pygame
        for ev in pygame.event.get():
            # Evento de fechar a tela
            if ev.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            # Evento de pressionar R para Reiniciar
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_r:
                # Reinicia valores do jogo
                num_discos = await tela_entrada(surf, font_lg, font_md, font_sm, font_xs)
                torre = criar_torre(num_discos)
                min_move = 2 ** num_discos - 1
                contador = 0
                state = 'playing'
                dragging = False
                drag_disk = None

            # Evento de clique do mouse
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and state == 'playing':
                # Pega o índice do pino clicado
                pi = peg_at(mx)
                # Verifica se o pino existe e se possui discos
                if pi is not None and not estado.plataforma[pi].is_empty():
                    # Obtém a lista de discos do pino
                    items = estado.plataforma[pi].items
                    # Índice do disco no topo
                    si = len(items) - 1
                    # Valor do disco no topo
                    top_dv = items[si]
                    # Calcula o retângulo do disco
                    r = disco_rect(pi, si, top_dv, num_discos)
                    # Verifica se o clique ocorreu exatamente sobre o disco
                    if r.collidepoint(mx, my):
                        # Disco está sendo arrastado
                        dragging = True
                        # Armazena disco selecionado
                        drag_disk = top_dv
                        # Salva pino de origem
                        drag_origin = pi
                        # Salva posição inicial do mouse
                        drag_pos = (mx, my)

            # Evento de soltar o clique do mouse
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and dragging:
                # Pino mais próximo do mouse
                pi = peg_at(mx)
                # Verifica se pino existe e se é válido (diferente do pino de origem)
                if pi is not None and pi != drag_origin:
                    # Executa a lógica para verificar se o movimento é válido
                    valido, invalido_visual = mover_disco(drag_origin, pi)
                    # Se for, execute
                    if valido:
                        contador += 1
                        # Verifica condição de vitória
                        if checar_torre(torre, num_discos):
                            if contador <= min_move:
                                state = 'win'
                        # Verifica condição de derrota
                        elif contador == min_move:
                            if not checar_torre(torre, num_discos):
                                state = 'lose'
                    elif invalido_visual:
                        # Finaliza visualmente o arrasto antes de desenhar
                        dragging = False
                        # Mostra mensagem de movimento inválido
                        mensagem = 'Jogada inválida!'
                        # Atualiza a tela mostrando disco no lugar errado
                        criar_cena(surf, num_discos, font_sm, font_md, font_lg, font_xs, dragging, drag_disk, drag_pos,
                                   drag_origin, contador, min_move, state, hover_peg, mensagem)
                        pygame.display.flip()
                        # Espera 500ms
                        await asyncio.sleep(0.5)
                        # Desfaz o movimento
                        desfazer_movimento(drag_origin, pi)
                        mensagem = ''
                # Finaliza arrasto do disco
                dragging = False
                drag_disk = None

            # Atualiza continuamente a posição do disco enquanto ele é arrastado
            elif ev.type == pygame.MOUSEMOTION and dragging:
                drag_pos = (mx, my)

        # Renderiza a cena
        criar_cena(surf, num_discos, font_sm, font_md, font_lg, font_xs,
                   dragging, drag_disk, drag_pos, drag_origin,
                   contador, min_move, state, hover_peg, mensagem)
        # Atualiza a cena
        pygame.display.flip()
        # Controle taxa de atualização
        await asyncio.sleep(1.0 / FPS)


if __name__ == '__main__':
    asyncio.run(main())
