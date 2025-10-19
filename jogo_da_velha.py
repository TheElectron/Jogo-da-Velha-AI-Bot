import math

class JogoDaVelha:
    def __init__(self):
        self.tabuleiro = [[' ' for _ in range(3)] for _ in range(3)]
        self.humano = 'X'
        self.bot = 'O'
    def fazer_jogada(self, linha, col, jogador):
        if self.tabuleiro[linha][col] == ' ':
            self.tabuleiro[linha][col] = jogador
            return True
        return False

    def verificar_estado_jogo(self):
        for i in range(3):
            if self.tabuleiro[i][0] == self.tabuleiro[i][1] == self.tabuleiro[i][2] != ' ':
                return self.tabuleiro[i][0], ('row', i)
        for i in range(3):
            if self.tabuleiro[0][i] == self.tabuleiro[1][i] == self.tabuleiro[2][i] != ' ':
                return self.tabuleiro[0][i], ('col', i)
        if self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] != ' ':
            return self.tabuleiro[0][0], ('diag', 1)
        if self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] != ' ':
            return self.tabuleiro[0][2], ('diag', 2)
        if all(self.tabuleiro[i][j] != ' ' for i in range(3) for j in range(3)):
            return 'empate', None
        return None, None

    def espacos_vazios(self):
        vazios = []
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] == ' ':
                    vazios.append((i, j))
        return vazios

    def minimax(self, profundidade, eh_maximizador):
        vencedor, _ = self.verificar_estado_jogo()
        if vencedor == self.bot: return 10
        if vencedor == self.humano: return -10
        if vencedor == 'empate': return 0
        if eh_maximizador:
            melhor_score = -math.inf
            for (linha, col) in self.espacos_vazios():
                self.tabuleiro[linha][col] = self.bot
                score = self.minimax(profundidade + 1, False)
                self.tabuleiro[linha][col] = ' '
                melhor_score = max(score, melhor_score)
            return melhor_score
        else:
            melhor_score = math.inf
            for (linha, col) in self.espacos_vazios():
                self.tabuleiro[linha][col] = self.humano
                score = self.minimax(profundidade + 1, True)
                self.tabuleiro[linha][col] = ' '
                melhor_score = min(score, melhor_score)
            return melhor_score

    def encontrar_melhor_jogada(self):
        melhor_score = -math.inf
        melhor_jogada = None
        for (linha, col) in self.espacos_vazios():
            self.tabuleiro[linha][col] = self.bot
            score = self.minimax(0, False)
            self.tabuleiro[linha][col] = ' '
            if score > melhor_score:
                melhor_score = score
                melhor_jogada = (linha, col)
        return melhor_jogada

    def reset(self):
        self.tabuleiro = [[' ' for _ in range(3)] for _ in range(3)]

