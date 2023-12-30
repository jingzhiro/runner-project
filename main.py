import pygame
from sys import exit
from random import randint

def display_score():
    score = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = pixel_font.render(f'Score: {score}', False, 'white')
    score_rect = score_surf.get_rect(center = (w / 2, 80))
    screen.blit(score_surf, score_rect)
    return score

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for rect in obstacle_list:
            rect.x -= 5
            if rect.bottom == floor_rect.top:
                screen.blit(obstacle_surface, rect)
            else: 
                screen.blit(aerial_surface, rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if rect.x > -100]
        return obstacle_rect_list
    else: return []

def is_player_collision(player_rect, obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player_rect.colliderect(obstacle_rect):
                return True
            
    return False

def player_animation():
    global player_surface, player_index
    player_index += 0.1
    if player_index >= len(player_walk):player_index = 0
    player_surface = player_walk[int(player_index)]


pygame.init()
pygame.display.set_caption("runner-prototype")
pygame_icon = pygame.image.load('assets/graphics/moon.png')
pygame.display.set_icon(pygame_icon)
bg_music = pygame.mixer.Sound('assets/audio/Chris Christodoulou - Risk of Rain 2  Risk of Rain 2 (2020).mp3')
bg_music.play(loops = -1)
bg_music.set_volume(0.1)

pixel_font = pygame.font.Font('assets/fonts/dogica.ttf', 30)

# Creates a window
screen = pygame.display.set_mode((w := 1280, h := 720))
screen_rect = screen.get_rect()

# Other surfaces
floor_surface = pygame.Surface((1280, 100))
floor_surface.fill('white')
floor_rect = floor_surface.get_rect(bottomright = (1280, 720))

player_walk_1 = pygame.Surface((50, 50))
player_walk_1.fill('green')
player_walk_2 = pygame.Surface((50, 50))
player_walk_2.fill('lightgreen')
player_index = 0
player_walk = [player_walk_1, player_walk_2]
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(bottomleft = (180, floor_rect.top)) 

obstacle_surface = pygame.Surface((40, 100))
obstacle_surface.fill('red')
aerial_surface = pygame.Surface((40, 40))
aerial_surface.fill('purple')

obstacle_rect_list = []

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

# Misc. values
player_gravity = 0
game_active = True
start_menu = True
start_time = 0

# Clock object controls the frame rate
clock = pygame.time.Clock()

# Game Loop
while True:
    # If the exit button is clicked, calls pygame and system to exit

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if start_menu and game_active:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                start_menu = False
        if game_active and not start_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == floor_rect.top:
                    player_gravity = -20
            if event.type == obstacle_timer:
                if randint(0, 3) == 1:
                    obstacle_rect_list.append(
                        aerial_surface.get_rect(
                            midtop = (randint(screen_rect.right, screen_rect.right + 200), 
                                      floor_rect.top - 200)))
                else:
                    obstacle_rect_list.append(
                        obstacle_surface.get_rect(
                            bottomright = (randint(screen_rect.right, screen_rect.right + 100), 
                                           floor_rect.top)))
        elif not game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True  
                    obstacle_rect_list = []
                    start_time = pygame.time.get_ticks()    
    if start_menu and game_active:
        screen.fill('black')
        play_surf = pixel_font.render('Press any button to play', False, 'white')
        play_rect = play_surf.get_rect(center = (w / 2, h / 2))
        screen.blit(play_surf, play_rect)
        
    elif game_active and not start_menu:
        screen.fill((10, 10, 10))
        screen.blit(floor_surface, floor_rect)
        score = display_score()

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= floor_rect.top: 
            player_rect.bottom = floor_rect.top
        screen.blit(player_surface, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = not is_player_collision(player_rect, obstacle_rect_list)

    else: 
        screen.fill('black')
        score_surf = pixel_font.render(f'Score: {score}', False, 'white')
        score_rect = score_surf.get_rect(center = (w / 2, 80))
        game_over = pixel_font.render('Game Over', False, 'white')
        game_over_rect = game_over.get_rect(midbottom = (w / 2, h / 2 - 25))
        play_again = pixel_font.render('Press any key', False, 'white')
        play_again_rect = play_again.get_rect(midtop = (w / 2, h / 2 + 25))
        
        screen.blit(score_surf, score_rect)
        screen.blit(game_over, game_over_rect)
        screen.blit(play_again, play_again_rect)
    
    pygame.display.update()
    clock.tick(60)

