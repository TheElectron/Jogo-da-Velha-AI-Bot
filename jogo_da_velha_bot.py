import sys
import pygame
from jogo_da_velha import JogoDaVelha

# Inicialização do Pygame
pygame.init()

# Constantes
OFFSET_Y = 100
TAMANHO_LINHA = 15
LINHAS, COLUNAS = 3, 3
LARGURA, ALTURA = 600, 800
TAMANHO_QUADRADO = LARGURA // COLUNAS

# Cores
COR_X = (84, 84, 84)
COR_O = (242, 235, 211)

COR_BG = (28, 170, 156)
COR_LINHA = (23, 145, 135)
COR_TEXTO = (255, 255, 255)
COR_LINHA_VENCEDORA = (255, 0, 0)

# Tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('AI Bot | Tic Tac Toe')

# Fontes
FONTE_PLACAR = pygame.font.SysFont('consolas', 40)
FONTE_BOTAO = pygame.font.SysFont('consolas', 30)

def desenhar_placar(placar_jogador, placar_bot):
    """Desenha o placar na parte superior da tela."""
    texto_jogador = FONTE_PLACAR.render(f"Jogador: {placar_jogador}", True, COR_TEXTO)
    texto_bot = FONTE_PLACAR.render(f"Bot: {placar_bot}", True, COR_TEXTO)
    tela.blit(texto_jogador, (20, 15))
    tela.blit(texto_bot, (LARGURA - texto_bot.get_width() - 20, 15))

def desenhar_botao_restart(rect):
    """Desenha um botão de reiniciar."""
    pygame.draw.rect(tela, COR_LINHA, rect, border_radius=15)
    texto = FONTE_BOTAO.render("Reiniciar", True, COR_TEXTO)
    texto_rect = texto.get_rect(center=rect.center)
    tela.blit(texto, texto_rect)

def desenhar_grade():
    # Linhas Horizontais
    pygame.draw.line(tela, COR_LINHA, (0, TAMANHO_QUADRADO + OFFSET_Y), (LARGURA, TAMANHO_QUADRADO + OFFSET_Y), TAMANHO_LINHA)
    pygame.draw.line(tela, COR_LINHA, (0, 2 * TAMANHO_QUADRADO + OFFSET_Y), (LARGURA, 2 * TAMANHO_QUADRADO + OFFSET_Y), TAMANHO_LINHA)
    # Linhas Verticais
    pygame.draw.line(tela, COR_LINHA, (TAMANHO_QUADRADO, OFFSET_Y), (TAMANHO_QUADRADO, ALTURA - 100), TAMANHO_LINHA)
    pygame.draw.line(tela, COR_LINHA, (2 * TAMANHO_QUADRADO, OFFSET_Y), (2 * TAMANHO_QUADRADO, ALTURA - 100), TAMANHO_LINHA)

def desenhar_figuras(tabuleiro):
    for linha in range(LINHAS):
        for col in range(COLUNAS):
            if tabuleiro[linha][col] == 'X':
                x_pos = col * TAMANHO_QUADRADO
                y_pos = linha * TAMANHO_QUADRADO + OFFSET_Y
                margem = TAMANHO_QUADRADO // 4
                pygame.draw.line(tela, COR_X, (x_pos + margem, y_pos + margem), (x_pos + TAMANHO_QUADRADO - margem, y_pos + TAMANHO_QUADRADO - margem), 25)
                pygame.draw.line(tela, COR_X, (x_pos + margem, y_pos + TAMANHO_QUADRADO - margem), (x_pos + TAMANHO_QUADRADO - margem, y_pos + margem), 25)
            elif tabuleiro[linha][col] == 'O':
                centro_x = int(col * TAMANHO_QUADRADO + TAMANHO_QUADRADO / 2)
                centro_y = int(linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO / 2 + OFFSET_Y)
                raio = TAMANHO_QUADRADO // 3
                pygame.draw.circle(tela, COR_O, (centro_x, centro_y), raio, 15)

def desenhar_linha_vencedora(vencedor_info):
    tipo_vitoria, indice = vencedor_info
    if tipo_vitoria == 'row':
        y_pos = int(indice * TAMANHO_QUADRADO + TAMANHO_QUADRADO / 2 + OFFSET_Y)
        pygame.draw.line(tela, COR_LINHA_VENCEDORA, (15, y_pos), (LARGURA - 15, y_pos), 15)
    elif tipo_vitoria == 'col':
        x_pos = int(indice * TAMANHO_QUADRADO + TAMANHO_QUADRADO / 2)
        pygame.draw.line(tela, COR_LINHA_VENCEDORA, (x_pos, 15 + OFFSET_Y), (x_pos, ALTURA - 115), 15)
    elif tipo_vitoria == 'diag':
        if indice == 1:
            pygame.draw.line(tela, COR_LINHA_VENCEDORA, (25, OFFSET_Y + 25), (LARGURA - 25, ALTURA - 125), 25)
        elif indice == 2:
            pygame.draw.line(tela, COR_LINHA_VENCEDORA, (25, ALTURA - 125), (LARGURA - 25, OFFSET_Y + 25), 25)

def main():
    jogo = JogoDaVelha()
    turno = jogo.humano
    game_over = False
    vencedor_info = None
    # --- VARIÁVEIS DA SESSÃO ---
    placar_jogador = 0
    placar_bot = 0
    # --- RETÂNGULO DO BOTÃO ---
    botao_restart_rect = pygame.Rect(LARGURA // 2 - 150, ALTURA - 75, 300, 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Se o botão de reiniciar for clicado
                if botao_restart_rect.collidepoint(event.pos):
                    placar_jogador = 0
                    placar_bot = 0
                    game_over = True # Força o reinicio do jogo
                
                # Se o clique for no tabuleiro durante a vez do jogador
                elif not game_over and turno == jogo.humano:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1] - OFFSET_Y
                    if 0 < mouseY < LARGURA: # Clicou dentro da área do tabuleiro
                        linha_clicada = int(mouseY // TAMANHO_QUADRADO)
                        coluna_clicada = int(mouseX // TAMANHO_QUADRADO)
                        if jogo.fazer_jogada(linha_clicada, coluna_clicada, jogo.humano):
                            vencedor, info = jogo.verificar_estado_jogo()
                            if vencedor:
                                game_over = True
                                vencedor_info = info
                                if vencedor == jogo.humano: placar_jogador += 1
                                elif vencedor == jogo.bot: placar_bot += 1
                            turno = jogo.bot
        # Vez do Bot
        if turno == jogo.bot and not game_over:
            jogada = jogo.encontrar_melhor_jogada()
            if jogada:
                jogo.fazer_jogada(jogada[0], jogada[1], jogo.bot)
                vencedor, info = jogo.verificar_estado_jogo()
                if vencedor:
                    game_over = True
                    vencedor_info = info
                    if vencedor == jogo.humano: placar_jogador += 1
                    elif vencedor == jogo.bot: placar_bot += 1
            turno = jogo.humano
        # --- DESENHO DA TELA ---
        tela.fill(COR_BG)
        desenhar_grade()
        desenhar_figuras(jogo.tabuleiro)
        desenhar_placar(placar_jogador, placar_bot)
        desenhar_botao_restart(botao_restart_rect)
        if vencedor_info:
            desenhar_linha_vencedora(vencedor_info)
        pygame.display.update()

        # --- FIM DE JOGO E REINÍCIO ---
        if game_over:
            pygame.time.wait(1500)
            jogo.reset()
            game_over = False
            vencedor_info = None

if __name__ == '__main__':
    main()