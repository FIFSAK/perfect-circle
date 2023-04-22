import pygame
import math
import time

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def clearing(sc, center_dot, radius_dot):
    sc.fill(0)
    pygame.draw.circle(sc, 'white', center_dot, radius_dot)
    pos_hist.clear()
    percent_hist.clear()

def linefun(pos1, pos2):
    x1 = pos1[0]
    y1 = pos1[1]
    x2 = pos2[0]
    y2 = pos2[1]
    k = (y1 - y2) / (x1 - x2)
    b = y2 - k * x2
    return k, b

def valuefun(k, b, pos):
    return pos[1] == k * pos[0] + b

pygame.init()
sc = pygame.display.set_mode((600, 600))
running = True
drawing = False
start_pos = (0, 0)
end_pos = (0, 0)
width_line = 1
pos_hist = []
center_dot = (300, 300)
radius_dot = 3
min_distance = 50

f = pygame.font.SysFont('EightBits', 40)
too_close_table = f.render('too close to dot', True, 'red')
too_close_table_center = too_close_table.get_rect(center=(300, 330))
too_slow_table = f.render('draw faster', True, 'red')
too_slow_table_center = too_slow_table.get_rect(center=(300, 270))

coord_counter = 0
start_time = 0
percent = None
percent_hist = []
radius_perfect_circle = None
reference_line = None
check_for_valuefun = False

while running:
    sc.fill(0)
    pygame.draw.circle(sc, 'white', center_dot, radius_dot)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            start_pos = event.pos
            radius_perfect_circle = distance((300, 300), start_pos)
            drawing = True
            coord_counter = 0
            start_time = time.time()
            reference_line = start_pos
            k, b = linefun(center_dot, reference_line)
        elif event.type == pygame.MOUSEMOTION and drawing:
            end_pos = event.pos
            if distance(end_pos, center_dot) > radius_dot + min_distance:
                pos_hist.append(end_pos)
                coord_counter += 1
                pygame.draw.line(sc, (255, 255, 255), start_pos, end_pos, width_line)
                start_pos = end_pos
            else:
                clearing(sc, center_dot, radius_dot)
                sc.blit(too_close_table, too_close_table_center)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            drawing = False
            clearing(sc, center_dot, radius_dot)

        if coord_counter < 300 and (time.time() - start_time) >= 2:
            clearing(sc, center_dot, radius_dot)
            coord_counter = 0
            sc.blit(too_slow_table, too_slow_table_center)
        elif coord_counter > 300 and (time.time() - start_time) >= 2:
            start_time = time.time()
            coord_counter = 0
        pygame.display.update()