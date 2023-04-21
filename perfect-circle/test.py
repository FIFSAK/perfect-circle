import pygame
import math
pygame.init()
sc = pygame.display.set_mode((600, 600))
check = True
check_draw = False
color = "white"
start_pos = (0, 0)
end_pps = (0, 0)
width_line = 2
threshold = 1  # Distance threshold for line closure

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

while check:
    pygame.draw.circle(sc, 'white', (300, 300), 10)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                check = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            start_pos = event.pos
            check_draw = True
        if event.type == pygame.MOUSEMOTION:
            if check_draw:
                end_pos = event.pos
                pygame.draw.line(sc, color, start_pos, end_pos, width_line)
                start_pos = end_pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            check_draw = False
            if distance(start_pos, event.pos) <= threshold:
                sc.fill(0)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            sc.fill(0)
    pygame.display.update()

pygame.quit()
