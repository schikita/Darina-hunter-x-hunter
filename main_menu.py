import pygame
import sys
from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Hunter x Hunter - главное меню")

pygame.font.init()
font = pygame.font.SysFont("Montsterrat", 36)

pygame.mixer.init()

pygame.mixer.music.load("assets/tileset/main_menu_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

select_sound = pygame.mixer.Sound('assets/tileset/select.mp3')

menu_items = ["Начать игру",
               "Продолжить",
                 "Настройки",
                  "Управление",
                   "Выход" ]

selected = 0

background = pygame.image.load("assets/ui/mainmenu.jpg")

def draw_menu():
    screen.blit(background, (0, 0))

    base_x = 50
    base_y = HEIGHT - (len(menu_items) * 45) - 30

    title_font = pygame.font.SysFont("Monsterrat", 45, bold=True)

    for i, item in enumerate(menu_items):
        color = YELLOW if i == selected else GRAY
        text_surface = font.render(item, True, color)
        screen.blit(text_surface, (base_x, base_y + i * 45))

    pygame.display.flip()

def main_menu_loop():
    global selected
    clock = pygame.time.Clock()

    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)
                    select_sound.play()
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                    select_sound.play()
                elif event.key == pygame.K_RETURN:
                    handle_menu_selection(menu_items[selected])

        clock.tick(FPS)

def handle_menu_selection(choice):
    if choice == "Начать игру":
        print("Старт новой игры")
    elif choice == "Продолжить":
        print("загрузка последней игры...")    # ост пункты
    elif choice == "Выход":
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main_menu_loop()

    
        


