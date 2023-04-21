import pygame

pygame.init()
sc = pygame.display.set_mode((600, 600))
check = True
check_draw = False
color = "white"
start_pos = (0, 0)
end_pps = (0, 0)
width_line = 4
pos_hist = []


def clearing():
    sc.fill(0)
    pos_hist.clear()
    return False


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
                if start_pos not in pos_hist:
                    pos_hist.append(start_pos)
                    end_pos = event.pos
                    pygame.draw.line(sc, color, start_pos, end_pos, width_line)
                    start_pos = end_pos
                else:
                    check_draw = clearing()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            check_draw = clearing()
    pygame.display.update()

pygame.quit()
