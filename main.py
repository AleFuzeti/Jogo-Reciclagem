import pygame
import random
import datetime
import os

from sprites import RecyclableItem
from settings import COLORS, ITEM_IMAGES, HEIGHT, WIDTH
from initialize import inicializa

# Inicializa o Pygame
screen, font, small_font, smaller_font, bins, item_list = inicializa()

# Função para criar um item a partir da lista de itens restantes
def create_item_from_list(item_list):
    if not item_list:
        return None
    category, image_path = item_list.pop()
    x, y = WIDTH // 2, random.randint(50, 150)
    return RecyclableItem(x, y, category, image_path)

# Função para desenhar o nome do item na tela
def draw_item_name(item):
    # Extrai apenas o nome do arquivo sem o diretório
    item_name = os.path.basename(item.name)  # Isso vai resultar em "garrafa.png"
    # Renderiza o texto para exibir na tela
    text = font.render(item_name, True, (0, 0, 0))    
    text_rect = text.get_rect(center=(WIDTH // 2, 200))
    screen.blit(text, text_rect)


def save_results(results, score, player_name):
    with open("resultados.txt", "a") as file:  # 'a' para anexar sem sobrescrever
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        file.write(f"Data: {now}\n")
        file.write(f"Nome: {player_name}\n")
        # pont final- total
        file.write(f"Pontuação final: {score}/{sum(len(items) for items in results.values())}\n\n")
        for bin_category, items in results.items():
            file.write(f"Lixeira {bin_category}:\n")
            file.write(f"  Acertos: {len([item for item in items if item[1]])}/{len(items)}\n")
            for item_name, correct in items:
                status = "Correto" if correct else "Incorreto"
                item_name = os.path.basename(item_name)
                file.write(f"    - {item_name}: {status}\n")
            file.write("\n")

# Função para mostrar os resultados anteriores
def display_scores():
    running = True
    player_scores = {}  # Dicionário para armazenar pontuações por nome de jogador

    # Ler o arquivo e agrupar resultados por nome de jogador
    try:
        with open("resultados.txt", "r") as file:
            lines = file.readlines()
            current_name = None
            score_block = []
            for line in lines:
                if line.startswith("Nome: "):
                    current_name = line.split(": ")[1].strip()
                    player_scores[current_name] = []
                if current_name:
                    score_block.append(line)
                    if line.strip() == "":
                        player_scores[current_name].append("".join(score_block))
                        score_block = []
    except FileNotFoundError:
        player_scores = {"Nenhum resultado encontrado.": []}

    font_height = smaller_font.get_height()
    player_names = list(player_scores.keys())
    selected_player = None

    while running:
        screen.fill((255, 255, 255))
        title_text = font.render("Pontuações", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 10))
        
        # exibir um botão de limpar resultados do resultados.txt e volta para tela inicial
        clear_button = pygame.Rect(WIDTH - 180, 15, 140, 30)
        pygame.draw.rect(screen, (255, 0, 0), clear_button)
        clear_text = smaller_font.render("Limpar resultados", True, (255, 255, 255))
        screen.blit(clear_text, (WIDTH - 180 + 70 - clear_text.get_width() // 2, 20))
        
        if clear_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            with open("resultados.txt", "w") as file:
                file.write("")
            running = False    
        
        # Exibir lista de nomes de jogadores
        y_offset = 20
        for name in player_names:
            name_text = small_font.render(name, True, (0, 0, 0))
            name_rect = name_text.get_rect(topleft=(20, y_offset))
            screen.blit(name_text, name_rect)
            if name_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                selected_player = name
            y_offset += font_height + 5

        # Exibir detalhes do jogador selecionado
        if selected_player:
            screen.fill((255, 255, 255))
            score_lines = player_scores[selected_player]
            y_offset = 5
            x_offset = 0
            for line in score_lines:
                for subline in line.split("\n"):
                    score_text = smaller_font.render(subline, True, (0, 0, 0))
                    screen.blit(score_text, (x_offset, y_offset))
                    y_offset += font_height + 5
                    if y_offset > HEIGHT - font_height:
                        y_offset = 10  # Resetar se passar da tela
                        x_offset += 300  # Mover para a direita
            
            # Exibir botão de voltar no final inferior da tela
            back_button = pygame.Rect(WIDTH - 180, HEIGHT - 50, 140, 30)
            pygame.draw.rect(screen, (0, 0, 255), back_button)
            back_text = smaller_font.render("Voltar", True, (255, 255, 255))
            screen.blit(back_text, (WIDTH - 180 + 70 - back_text.get_width() // 2, HEIGHT - 45))
            if back_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                running = False
                selected_player = None

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pressione ESC para voltar à tela inicial
                    running = False
                    selected_player = None

# Função para mostrar a tela de senha e exibir os resultados
def enter_password_screen():
    password = ""
    while True:
        screen.fill((255, 255, 255))
        password_prompt = small_font.render("Digite a senha:", True, (0, 0, 0))
        screen.blit(password_prompt, (WIDTH // 2 - 100, 200))

        password_text = small_font.render(password, True, (0, 0, 0))
        screen.blit(password_text, (WIDTH // 2 - 100, 230))

        submit_button = pygame.Rect(WIDTH // 2 - 50, 300, 100, 50)
        pygame.draw.rect(screen, (0, 255, 0), submit_button)
        submit_text = small_font.render("Enviar", True, (0, 0, 0))
        screen.blit(submit_text, (WIDTH // 2 - submit_text.get_width() // 2, 310))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                elif event.key == pygame.K_RETURN:
                    if password == "1234":
                        display_scores()
                        return
                    else:
                        # Exibir mensagem de erro se necessário
                        pass
                else:
                    password += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button.collidepoint(event.pos):
                    if password == "1234":
                        display_scores()
                        return
                    else:
                        # Exibir mensagem de erro se necessário
                        pass

# Atualizar a função start_screen() para chamar enter_password_screen() ao invés de solicitar a senha pelo terminal
def start_screen():
    player_name = ""
    while True:
        screen.fill((255, 255, 255))
        title_text = font.render("Jogo de Reciclagem", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        name_prompt = small_font.render("Digite seu nome:", True, (0, 0, 0))
        screen.blit(name_prompt, (WIDTH // 2 - 100, 200))

        name_text = small_font.render(player_name, True, (0, 0, 0))
        screen.blit(name_text, (WIDTH // 2 - 100, 230))

        start_button = pygame.Rect(WIDTH // 2 - 70, 300, 140, 50)
        pygame.draw.rect(screen, (0, 255, 0), start_button)
        start_text = small_font.render("Iniciar", True, (0, 0, 0))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 310))

        score_button = pygame.Rect(WIDTH // 2 - 70, 370, 140, 50)
        pygame.draw.rect(screen, (0, 0, 255), score_button)
        score_text = small_font.render("Pontuações", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 380))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    if player_name.strip():
                        main(player_name)
                elif score_button.collidepoint(event.pos):
                    enter_password_screen()

# Função para inicializar o estado do jogo
def initialize_game_state():
    global item_list, bins
    screen, font, small_font, smaller_font, bins, item_list = inicializa()

# Função principal do jogo
def main(player_name):
    initialize_game_state()
    running = True
    clock = pygame.time.Clock()
    items = pygame.sprite.Group()
    current_item = create_item_from_list(item_list)
    if current_item:
        items.add(current_item)
    score = 0
    results = {category: [] for category in COLORS.keys()}

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_item and current_item.rect.collidepoint(event.pos):
                    current_item.dragging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if current_item and current_item.dragging:
                    current_item.dragging = False
                    for bin in bins:
                        if bin.rect.colliderect(current_item.rect):
                            correct = bin.category == current_item.category
                            if correct:
                                score += 1
                            results[bin.category].append((current_item.name, correct))
                            items.remove(current_item)
                            current_item = create_item_from_list(item_list)
                            if current_item:
                                items.add(current_item)
                            break

        if current_item:
            current_item.update(mouse_pos)

        screen.fill((255, 255, 255))
        bins.draw(screen)
        items.draw(screen)
        if current_item:
            draw_item_name(current_item)
        else:
            game_over_text = font.render("Fim do jogo!", True, (0, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        pygame.display.flip()
        clock.tick(60)

    save_results(results, score, player_name)
    start_screen()

if __name__ == "__main__":
    start_screen()