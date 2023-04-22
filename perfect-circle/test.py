import pygame
import math
import time


# Function to find distance between 2 points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Function to clear surface and change check to false (mostly to change check_draw)
def clearing():
    sc.fill(0)
    pygame.draw.circle(sc, 'white', center_dot, radius_dot)
    pos_hist.clear()
    return False


pygame.init()
sc = pygame.display.set_mode((600, 600))
check = True  # Check for main while loop
check_draw = False  # Check for drawing
red_intensity = 0
green_intensity = 255
start_pos = (0, 0)
end_pos = (0, 0)
width_line = 4
pos_hist = []  # All mouse position history to use to catch moment when circle is finished
center_dot = (300, 300)  # Center of dot around which the drawing will be done
radius_dot = 3
min_distance = 50  # Minimum distance when drawing is possible

# Font and size of texts too slow and too close
f = pygame.font.SysFont('EightBits', 40)

# Surface for text too close
too_close_table = f.render('too close to dot', True, 'red')
# Center for text too close for correct blit
too_close_table_center = too_close_table.get_rect(center=(300, 330))

# Surface for text too slow
too_slow_table = f.render('draw faster', True, 'red')
# Center for text too slow for correct blit
too_slow_table_center = too_slow_table.get_rect(center=(300, 270))

coord_counter = 0  # Count of coordinates which are drawn to find drawing speed
start_time = 0  # Time when drawing started, used to find drawing speed
percent = None
radius_perfect_circle = None
# Main loop
while check:
    color = (red_intensity, green_intensity, 0)
    # Draw circle around which the user will draw their circle
    pygame.draw.circle(sc, 'white', center_dot, radius_dot)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # If Enter is pressed, the game will stop
                check = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # When left mouse button is pressed, determine start position, drawing check, and start time
            start_pos = event.pos
            radius_perfect_circle = distance((300, 300), start_pos)
            check_draw = True
            coord_counter = 0
            start_time = time.time()
        if event.type == pygame.MOUSEMOTION:
            if check_draw:
                # If the starting position is not in the history and the distance from the center dot is sufficient
                if start_pos not in pos_hist and distance(start_pos, center_dot) > radius_dot + min_distance:
                    pos_hist.append(start_pos)
                    coord_counter += 1
                    end_pos = event.pos
                    pygame.draw.line(sc, color, start_pos, end_pos, width_line)
                    radius_my_circle = distance((300, 300), end_pos)
                    if radius_my_circle > radius_perfect_circle:
                        percent = (radius_perfect_circle / radius_my_circle) * 100
                        percent = float('{:.1f}'.format(percent))
                    if radius_my_circle < radius_perfect_circle:
                        percent = (radius_my_circle / radius_perfect_circle) * 100
                        percent = float('{:.1f}'.format(percent))
                    if percent < 65:
                        check_draw = clearing()
                        wrong_way_table = f.render('wrong way', True, 'red')
                        wrong_way_table_center = wrong_way_table.get_rect(center=(300, 330))
                        sc.blit(wrong_way_table, wrong_way_table_center)
                    if red_intensity < 255:
                        red_intensity += (100 - percent) * 1.5
                        if red_intensity > 255:
                            red_intensity = 255
                    if red_intensity == 255:
                        green_intensity -= (100 - percent) * 1.5
                        if green_intensity < 0:
                            green_intensity = 0
                    percent_table = f.render(str(percent), True, color)
                    percent_table_center = percent_table.get_rect(center=(292.5, 293))
                    pygame.draw.rect(sc, 'black', pygame.Rect(259, 280, 68, 30))
                    sc.blit(percent_table, percent_table_center)

                    start_pos = end_pos
                else:
                    check_draw = clearing()

                # If the distance from the center dot is too small, clear the drawing and show the 'too close' message
                if distance(start_pos, center_dot) < radius_dot + min_distance:
                    check_draw = clearing()
                    sc.blit(too_close_table, too_close_table_center)

                # If the drawing speed is too slow, clear the drawing and show the 'too slow' message
                if coord_counter < 300 and (time.time() - start_time) >= 2:
                    check_draw = clearing()
                    coord_counter = 0
                    sc.blit(too_slow_table, too_slow_table_center)
                if coord_counter > 300 and (time.time() - start_time) >= 2:
                    start_time = time.time()
                    coord_counter = 0
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            check_draw = clearing()
            red_intensity = 0
            green_intensity = 255
        pygame.display.update()

pygame.quit()
