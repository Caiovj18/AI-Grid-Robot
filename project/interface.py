import pygame
import sys
from GridSearchNoWeight import Gera_Problema

class Node:
    def __init__(self, pai, estado, v1, v2, anterior, proximo):
        self.pai = pai
        self.estado = estado
        self.v1 = v1
        self.v2 = v2
        self.anterior = anterior
        self.proximo = proximo

class listaDEnc:
    def __init__(self):
        self.head = None
        self.tail = None

    def inserePrimeiro(self, st, v1, v2, p):
        novo_no = Node(p, st, v1, v2, None, None)
        if self.head == None:
            self.tail = novo_no
            self.head = novo_no
        else:
            novo_no.proximo = self.head
            self.head.anterior = novo_no
            self.head = novo_no

    def insereUltimo(self, st, v1, v2, p):
        novo_no = Node(p, st, v1, v2, None, None)
        if self.head is None:
            self.head = novo_no
            self.tail = novo_no
        else:
            self.tail.proximo = novo_no
            novo_no.anterior = self.tail
            self.tail = novo_no

    def deletaPrimeiro(self):
        if self.head is None:
            return None
        else:
            no = self.head
            self.head = self.head.proximo
            if self.head is not None:
                self.head.anterior = None
            else:
                self.tail = None
            return no

    def deletaUltimo(self):
        if self.tail is None:
            return None
        else:
            no = self.tail
            self.tail = self.tail.anterior
            if self.tail is not None:
                self.tail.proximo = None
            else:
                self.head = None
            return no

    def primeiro(self):
        return self.head
    
    def ultimo(self):
        return self.tail

    def vazio(self):
        return self.head is None
        
    def exibeLista(self):
        aux = self.head
        str1 = []
        while aux != None:
            temp = [aux.estado, aux.v1]
            if aux.pai != None:
                temp.append(aux.pai.estado)
            else:
                temp.append("nó raiz")
            str1.append(temp)
            aux = aux.proximo
        return str1
    
    def exibeCaminho(self):
        atual = self.tail
        path = []
        while atual.pai is not None:
            path.append(atual.estado)
            atual = atual.pai
        path.append(atual.estado)
        return path[::-1]
    
    def exibeCaminho1(self, valor):
        atual = self.head
        while atual.estado != valor:
            atual = atual.proximo
        path = []
        atual = atual.pai
        while atual.pai is not None:
            path.append(atual.estado)
            atual = atual.pai
        path.append(atual.estado)
        return path

class PathFinder:
    def __init__(self, grid_size=(10, 10), obstacles=20):
        # Configurações da grid
        self.nx, self.ny = grid_size
        self.qtd_obstacles = obstacles
        
        # Gera a grid inicial
        self.reset_grid()
        
        # Configurações do pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
        pygame.display.set_caption("Path Finding Animation")
        self.clock = pygame.time.Clock()
        
        # Carrega a imagem do personagem
        self.load_character_image()
        
        # Configurações de animação
        self.animation_speed = 0.5  # Segundos por célula
        self.last_move_time = 0
        self.current_segment = 0
    
    def reset_grid(self):
        """Gera uma nova grid com obstáculos"""
        self.grid = Gera_Problema(self.nx, self.ny, self.qtd_obstacles)
        self.start_pos = (0, 0)
        self.end_pos = (self.nx-1, self.ny-1)
        
        # Garante que início e fim não são obstáculos
        self.grid[self.start_pos[0]][self.start_pos[1]] = 0
        self.grid[self.end_pos[0]][self.end_pos[1]] = 0
        
        # Encontra o caminho inicial
        self.find_path()
        
        # Reseta o estado da animação
        self.character_pos = list(self.start_pos)
        self.current_segment = 0
        self.last_move_time = pygame.time.get_ticks()
    
    def load_character_image(self):
        """Carrega a imagem do personagem ou cria uma padrão"""
        try:
            self.character_image = pygame.image.load("project/PR_ATO.png")
            self.character_image = pygame.transform.scale(self.character_image, (40, 40))
        except:
            # Fallback visual se a imagem não carregar
            self.character_image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.character_image, (0, 0, 255), (20, 20), 20)
    
    def sucessores(self, estado):
        """Gera os sucessores válidos para um estado"""
        x, y = estado
        moves = [
            (x+1, y), (x-1, y), (x, y+1), (x, y-1),  # Movimentos cardinais
            (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)  # Movimentos diagonais
        ]
        
        valid_moves = []
        for nx, ny in moves:
            if 0 <= nx < self.nx and 0 <= ny < self.ny and self.grid[nx][ny] == 0:
                valid_moves.append([nx, ny])
        return valid_moves
    
    def find_path(self):
        """Encontra o caminho usando busca em amplitude"""
        l1 = listaDEnc()
        l2 = listaDEnc()
        
        l1.insereUltimo(self.start_pos, 0, 0, None)
        l2.insereUltimo(self.start_pos, 0, 0, None)
        
        visitado = [[self.start_pos, 0]]
        
        while not l1.vazio():
            atual = l1.deletaPrimeiro()
            
            for novo in self.sucessores(atual.estado):
                # Verifica se já foi visitado
                flag = True
                for aux in visitado:
                    if aux[0] == novo:
                        if aux[1] <= (atual.v1 + 1):
                            flag = False
                        else:
                            aux[1] = atual.v1 + 1
                        break
                
                if flag:
                    l1.insereUltimo(novo, atual.v1 + 1, 0, atual)
                    l2.insereUltimo(novo, atual.v1 + 1, 0, atual)
                    visitado.append([novo, atual.v1 + 1])
                    
                    if novo == list(self.end_pos):
                        self.path = l2.exibeCaminho()
                        return
        
        # Se não encontrou caminho
        self.path = []
    
    def update_animation(self):
        """Atualiza a posição do personagem na animação"""
        if not self.path or self.current_segment >= len(self.path) - 1:
            return False  # Animação concluída
        
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_move_time) / 1000  # Segundos
        
        if elapsed >= self.animation_speed:
            self.current_segment += 1
            self.last_move_time = current_time
            if self.current_segment >= len(self.path) - 1:
                self.character_pos = list(self.end_pos)
                return False  # Animação concluída
        
        # Calcula posição interpolada
        start = self.path[self.current_segment]
        end = self.path[self.current_segment + 1]
        progress = min(1.0, elapsed / self.animation_speed)
        
        self.character_pos[0] = start[0] + (end[0] - start[0]) * progress
        self.character_pos[1] = start[1] + (end[1] - start[1]) * progress
        
        return True  # Animação em andamento
    
    def draw(self):
        """Desenha toda a cena"""
        width, height = self.screen.get_size()
        cell_size = min(width // self.ny, height // self.nx)
        
        # Desenha a grid
        for x in range(self.nx):
            for y in range(self.ny):
                color = (255, 255, 255) if self.grid[x][y] == 0 else (255, 0, 0)
                pygame.draw.rect(self.screen, color, 
                                (y * cell_size, x * cell_size, cell_size, cell_size))
                pygame.draw.rect(self.screen, (0, 0, 0), 
                                (y * cell_size, x * cell_size, cell_size, cell_size), 1)
        
        # Desenha o caminho
        if self.path:
            for i in range(len(self.path) - 1):
                start = self.path[i]
                end = self.path[i+1]
                pygame.draw.line(self.screen, (0, 255, 0),
                               (start[1] * cell_size + cell_size//2, start[0] * cell_size + cell_size//2),
                               (end[1] * cell_size + cell_size//2, end[0] * cell_size + cell_size//2), 3)
        
        # Desenha início e fim
        pygame.draw.circle(self.screen, (0, 255, 0), 
                         (self.start_pos[1] * cell_size + cell_size//2, 
                          self.start_pos[0] * cell_size + cell_size//2), 10)
        pygame.draw.circle(self.screen, (255, 0, 0), 
                         (self.end_pos[1] * cell_size + cell_size//2, 
                          self.end_pos[0] * cell_size + cell_size//2), 10)
        
        # Desenha o personagem
        char_rect = self.character_image.get_rect(
            center=(self.character_pos[1] * cell_size + cell_size//2, 
                    self.character_pos[0] * cell_size + cell_size//2))
        self.screen.blit(self.character_image, char_rect)
        
        # Mostra informações
        font = pygame.font.SysFont(None, 24)
        info_text = f"Path length: {len(self.path)} | Press R to reset"
        text_surface = font.render(info_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))
    
    def run(self):
        """Loop principal"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:  # Reinicia com nova grid
                        self.reset_grid()
            
            # Atualiza animação
            self.update_animation()
            
            # Desenha tudo
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = PathFinder()
    app.run()