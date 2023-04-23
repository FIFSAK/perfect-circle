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


def line_intersection(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:
        return False

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

    if 0 <= t <= 1 and 0 <= u <= 1:
        return True

    return False


def percentage_color(value, sensitivity=2):
    if value <= 75:
        red_intensity = 255
        green_intensity = 0
    else:
        red_intensity = 255 - 255 * (((value - 75) / 25) ** sensitivity)
        green_intensity = 255
    return (red_intensity, green_intensity, 0)

def extend_line_to_edge(point1, point2, screen_size):
    x1, y1 = point1
    x2, y2 = point2
    screen_width, screen_height = screen_size

    if x1 == x2:
        return (x1, 0), (x1, screen_height)

    slope = (y2 - y1) / (x2 - x1)
    y_intercept = y1 - slope * x1

    line_points = []

    if slope != 0:
        y_at_left_edge = y_intercept
        y_at_right_edge = slope * screen_width + y_intercept
        x_at_top_edge = -y_intercept / slope
        x_at_bottom_edge = (screen_height - y_intercept) / slope

        if 0 <= y_at_left_edge <= screen_height:
            line_points.append((0, y_at_left_edge))

        if 0 <= y_at_right_edge <= screen_height:
            line_points.append((screen_width, y_at_right_edge))

        if 0 <= x_at_top_edge <= screen_width:
            line_points.append((x_at_top_edge, 0))

        if 0 <= x_at_bottom_edge <= screen_width:
            line_points.append((x_at_bottom_edge, screen_height))

    if len(line_points) == 2:
        return line_points[0], line_points[1]

    return None

def angle_between_points(center, start, current):
    a = distance(center, start)
    b = distance(center, current)
    c = distance(start, current)

    cos_angle = (a**2 + b**2 - c**2) / (2 * a * b)
    angle = math.degrees(math.acos(cos_angle))

    return angle





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
percent_hist = []  # Store all percentage values to calculate the average
radius_perfect_circle = None
full_circle_check = False
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
            check_draw = clearing()
            # When left mouse button is pressed, determine start position, drawing check, and start time
            start_pos = event.pos
            radius_perfect_circle = distance((300, 300), start_pos)
            check_draw = True
            full_circle_check = False
            coord_counter = 0
            close_dot_check = True
            draw_fast_check = True
            intersection_check = True
            start_time = time.time()
        if event.type == pygame.MOUSEMOTION:
            if check_draw:
                # If the starting position is not in the history and the distance from the center dot is sufficient
                if distance(start_pos, center_dot) > radius_dot + min_distance:
                    pos_hist.append(start_pos)
                    coord_counter += 1
                    end_pos = event.pos
                    pygame.draw.line(sc, color, start_pos, end_pos, width_line)
                    radius_my_circle = distance((300, 300), end_pos)
                    invisible_line = extend_line_to_edge(center_dot, end_pos, (600, 600))
                    intersection_count = 0
                    if invisible_line is not None:
                        for i in range(len(pos_hist) - 1):
                            old_line = (pos_hist[i], pos_hist[i + 1])
                            if line_intersection(invisible_line, old_line):
                                intersection_count += 1
                    angle = angle_between_points(center_dot, pos_hist[0], end_pos)

                    if angle > 180:
                        check_draw = False
                        full_circle_check = True
                        wrong_way_table = f.render('wrong way', True, 'red')
                        wrong_way_table_center = wrong_way_table.get_rect(center=(300, 330))
                        sc.blit(wrong_way_table, wrong_way_table_center)

                    if intersection_count == 2:
                        wrong_way_table = f.render('wrong way', True, 'red')
                        wrong_way_table_center = wrong_way_table.get_rect(center=(300, 330))
                        sc.blit(wrong_way_table, wrong_way_table_center)
                        check_draw = False
                        intersection_check = False

                    if len(pos_hist) > 1:
                        new_line = (pos_hist[-1], end_pos)
                        for i in range(len(pos_hist) - 2):
                            old_line = (pos_hist[i], pos_hist[i + 1])
                            if line_intersection(new_line, old_line):
                                check_draw = False
                                full_circle_check = True
                                break
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

                # If the distance from the center dot is too small, clear the drawing and show the 'too close' message
                if distance(start_pos, center_dot) < radius_dot + min_distance:
                    close_dot_check = False
                    check_draw = clearing()
                    pygame.mixer.music.load(r"sounds\error-126627_TC403uZU.mp3")
                    pygame.mixer.music.play()
                    sc.blit(too_close_table, too_close_table_center)

                # If the drawing speed is too slow, clear the drawing and show the 'too slow' message
                elif coord_counter < 500 and (time.time() - start_time) >= 2:
                    pygame.mixer.music.load(r"sounds\error-126627_TC403uZU.mp3")
                    pygame.mixer.music.play()
                    check_draw = clearing()
                    coord_counter = 0
                    sc.blit(too_slow_table, too_slow_table_center)
                    draw_fast_check = False
                elif coord_counter > 300 and (time.time() - start_time) >= 2:
                    start_time = time.time()
                    coord_counter = 0
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            check_draw = False
            if not full_circle_check and close_dot_check and draw_fast_check and intersection_check:
                pygame.mixer.music.load(r"sounds\error-126627_TC403uZU.mp3")
                pygame.mixer.music.play()
                draw_full_circle = f.render('draw full circle', True, 'red')
                sc.blit(draw_full_circle, draw_full_circle.get_rect(center=(300, 230)))
            red_intensity = 0
            green_intensity = 255
        pygame.display.update()

pygame.quit()
