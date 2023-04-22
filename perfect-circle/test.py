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
    percent_hist.clear()
    return False



def percentage_color(value, sensitivity=2):
    if value <= 75:
        red_intensity = 255
        green_intensity = 0
    else:
        red_intensity = 255 - 255 * (((value - 75) / 25) ** sensitivity)
        green_intensity = 255
    return (red_intensity, green_intensity, 0)


def line_intersection_with_screen(center, start_pos, screen_size):
    dx, dy = start_pos[0] - center[0], start_pos[1] - center[1]

    if abs(dx) > abs(dy):
        if dx > 0:
            x = screen_size[0]
        else:
            x = 0
        y = center[1] + dy * (x - center[0]) / dx
    else:
        if dy > 0:
            y = screen_size[1]
        else:
            y = 0
        x = center[0] + dx * (y - center[1]) / dy

    return int(x), int(y)


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

def crossed_line(pos1, pos2, k, b):
    y1 = k * pos1[0] + b
    y2 = k * pos2[0] + b

    return (pos1[1] < y1 and pos2[1] > y2) or (pos1[1] > y1 and pos2[1] < y2)


pygame.init()
sc = pygame.display.set_mode((600, 600))
check = True  # Check for main while loop
check_draw = False  # Check for drawing
red_intensity = 0
green_intensity = 255
start_pos = (0, 0)
end_pos = (0, 0)
width_line = 1
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
percent_hist = []  # Store all percentage values to calculate the average
radius_perfect_circle = None
reference_line = None
check_for_valuefun = False
cnt = 0
cross_count = 0
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
            reference_line = line_intersection_with_screen(center_dot, start_pos, sc.get_size())
            k, b = linefun(center_dot, reference_line)

        if event.type == pygame.MOUSEMOTION:

            if check_draw:
                if abs(abs(start_pos[1]) - abs((start_pos[0] * k) + b)) < 1:
                    cnt += 1
                # If the starting position is not in the history and the distance from the center dot is sufficient
                if pos_hist.count(start_pos) == 0 and distance(start_pos,
                                                               center_dot) > radius_dot + min_distance and cross_count < 2:  # Modify this line

                    pos_hist.append(start_pos)
                    coord_counter += 1
                    end_pos = event.pos
                    if crossed_line(start_pos, end_pos, k, b):
                        cross_count += 1
                    pygame.draw.line(sc, color, start_pos, end_pos, width_line)
                    radius_my_circle = distance((300, 300), end_pos)
                    if radius_my_circle > radius_perfect_circle:
                        percent = (radius_perfect_circle / radius_my_circle) * 100
                        percent = float('{:.1f}'.format(percent))
                    if radius_my_circle < radius_perfect_circle:
                        percent = (radius_my_circle / radius_perfect_circle) * 100
                        percent = float('{:.1f}'.format(percent))
                    # Add the current percentage value to the list
                    percent_hist.append(percent)
                    sensitivity = 4  # You can adjust the sensitivity value to your liking
                    red_intensity = 255 - 255 * ((percent / 100) ** sensitivity)
                    green_intensity = 255 * ((percent / 100) ** sensitivity)
                    # Calculate the average percentage only if the percent_hist list is not empty
                    if len(percent_hist) > 0:
                        average_percent = sum(percent_hist) / len(percent_hist)
                        average_percent = float('{:.1f}'.format(average_percent))
                    else:
                        average_percent = 0

                    percent_color = percentage_color(average_percent)
                    percent_table = f.render(str(average_percent), True, percent_color)

                    percent_table_center = percent_table.get_rect(center=(292.5, 293))
                    pygame.draw.rect(sc, 'black', pygame.Rect(259, 280, 68, 30))
                    sc.blit(percent_table, percent_table_center)

                    start_pos = end_pos
                else:
                    check_draw = clearing()
                    cross_count = 0  # Reset cross_count when clearing
                    cnt = 0
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
            cnt = 0
            red_intensity = 0
            green_intensity = 255
        if check_draw and reference_line:
            pygame.draw.line(sc, 'black', center_dot, reference_line, width_line)
        pygame.display.update()

pygame.quit()
