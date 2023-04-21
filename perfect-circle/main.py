import pygame
import math


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def clearing():
    sc.fill(0)
    pos_hist.clear()
    return False


pygame.init()
sc = pygame.display.set_mode((600, 600))
check = True
check_draw = False
color = "white"
start_pos = (0, 0)
end_pos = (0, 0)
width_line = 4
pos_hist = []
center_dot = (300, 300)
radius_dot = 10
min_distance = 50
f = pygame.font.SysFont('EightBits', 40)
text_table = f.render('too close to dote', True, 'red')
text_table_center = text_table.get_rect(center=(300, 330))

while check:
    pygame.draw.circle(sc, 'white', center_dot, radius_dot)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                check = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            start_pos = event.pos
            check_draw = True
        if event.type == pygame.MOUSEMOTION:
            if check_draw:
                if start_pos not in pos_hist and distance(start_pos, center_dot) > radius_dot + min_distance:
                    pos_hist.append(start_pos)
                    end_pos = event.pos
                    pygame.draw.line(sc, color, start_pos, end_pos, width_line)
                    start_pos = end_pos
                else:
                    check_draw = clearing()
                    sc.blit(text_table, text_table_center)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            check_draw = clearing()
    pygame.display.update()

pygame.quit()
