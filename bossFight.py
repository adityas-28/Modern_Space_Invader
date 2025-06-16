import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load(r'resources\images\spaceship.png')
pygame.display.set_icon(icon)

background = pygame.image.load(r'resources\images\boss_bg.png')
background = pygame.transform.scale(background, (800, 600))

mixer.music.load(r'resources\sounds\strangerThingdBGMTrim.mp3')
mixer.music.set_volume(0.3)  
# mixer.music.play(-1) 

boss_image = pygame.image.load(r'resources\images\ufo.png')
boss_image = pygame.transform.scale(boss_image, (85, 85))
boss_x = 370
boss_y = 50
boss_x_change = 0
boss_y_change = 0

def show_boss(x, y):
    screen.blit(boss_image, (x, y)) 

playerImage = pygame.image.load(r'resources\images\spaceship (1).png')
playerImage = pygame.transform.scale(playerImage, (55, 55))
playerX = 375
playerY = 500
playerX_change = 0
playerY_change = 0

bulletImage = pygame.image.load(r'resources\images\bullet.png');
bulletImage = pygame.transform.scale(bulletImage, (15, 15))
bullet_state = False
bulletX = 0
bulletY = 0

enemyBulletImage = pygame.image.load(r'resources\images\bulletEnemy.png');
enemyBulletImage = pygame.transform.scale(enemyBulletImage, (15, 15))
enemy_bullet_state = False
enemy_bulletX = 0
enemy_bulletY = 0

def show_player(x, y):
    screen.blit(playerImage, (x, y))

def render_wrapped_text(text, font, color, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    lines.append(current_line)  # Add the last line
    return lines


start_font = pygame.font.Font(r'resources\fonts\typewriter.ttf', 28)


def main_message():
    timer = pygame.time.Clock()
    messages = [
        "I've locked onto the source — a rogue planet on the edge of the system.",
        "Dark. Dead. Orbiting nothing.",
        "That’s where he waits.",
        "This is my final descent.",
        "No retreat. No surrender.",
        "Zarnax — I’m coming for you."
    ]
    current_message = 0
    counter = 0
    speed = 1
    done = False
    box_width, box_height = 800, 200
    box_x = (800 - box_width) // 2 
    box_y = (600 - box_height) // 2  

    while True:
        screen.blit(background, (0, 0))
        timer.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and done:
                    if current_message < len(messages) - 1:
                        current_message += 1
                        counter = 0
                        done = False
                    else:
                        return  # Done with all messages

        dialogue_box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        dialogue_box.fill((0, 0, 0, 180))
        screen.blit(dialogue_box, (box_x, box_y))

        if counter < speed * len(messages[current_message]):
            counter += 1
        else:
            done = True

        text_to_display = messages[current_message][0:counter // speed]
        wrapped_lines = render_wrapped_text(text_to_display, start_font, (255, 255, 255), box_width - 40)

        for i, line in enumerate(wrapped_lines):
            snip = start_font.render(line, True, (255, 255, 255))
            line_y = box_y + 20 + i * 30
            screen.blit(snip, (box_x + 20, line_y))

        pygame.display.update()

running = True
show_intro = True

while running:
    if show_intro:
        main_message()
        show_intro = False  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    show_boss(358, 75)
    show_player(375, 450)

    pygame.display.update()
