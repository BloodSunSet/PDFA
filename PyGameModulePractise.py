import pygame
import sys
import time


def main():
    pygame.init()
    
    size = width, height = 1000, 800
    white = 255, 255, 255
    red = 255, 0, 0
    circle_list = []  # circle_text, circle_center
    line_list = []  # arrow_tail, arrow_head
    
    screen = pygame.display.set_mode(size)
    screen.fill(white)
    button_rects = menu_bar(screen)  # mouse, pen, run

    circle_number = 0
    circle_radius = 30
    circle_for_move_i = 0
    arrow_start = ()
    arrow_end = ()
    arrow_tail = ''
    arrow_head = ''
    arrow_tail_i = 0
    arrow_head_i = 0
    arrow_text = 'a'
    mouse_movement_for_circle = True
    mouse_movement_for_line = False

    change2mouse = False
    run = False

    has_circle_motion = False

    font = pygame.font.Font(r'fonts\freesansbold.ttf', 20)

    while 1:
        # 旧的动画方案
        """
        旧的动画方案：
        if button_animation is True:
            for i in range(button_status.__len__()):
                if button_status[i] is True:
                    temp_button_surface = button_surfaces[i]
                    temp_button_position = i * 32
            button_rect = temp_button_surface.get_rect()
            # button_rect.inflate_ip((-pixel, -pixel))
            button_rect.move_ip(temp_button_position, 0)
            screen.blit(temp_button_surface, button_rect)
            if return_mark is False:
                pixel += 1
                if pixel == 5:
                    return_mark = True
            if return_mark is True:
                pixel -= 1
                if pixel == 2:
                    return_mark = False
                    button_animation = False
            time.sleep(0.1)
 
        """
        flush(screen, circle_list, red, circle_radius, line_list, font, change2mouse, button_rects)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.__dict__['pos']  # x, y
                    if event.__dict__['button'] == 1:
                        if (pos[1] - circle_radius) < 32:
                            if button_rects[0][0] <= pos[0] <= (button_rects[0][0] + button_rects[0][2]):
                                change2mouse = True
                            if button_rects[1][0] <= pos[0] <= (button_rects[1][0] + button_rects[1][2]):
                                change2mouse = False
                            if button_rects[2][0] <= pos[0] <= (button_rects[2][0] + button_rects[2][2]):
                                run = True
                                # TODO:写状态转换表的生成
                            continue

                        if change2mouse is True:
                            for i, circle in enumerate(circle_list):
                                distance = get_distance(pos, circle)
                                if distance < 900:
                                    circle_for_move_i = i
                                    has_circle_motion = True
                                    break
                            continue

                        for i, circle in enumerate(circle_list):
                            distance = get_distance(pos, circle)
                            if distance < 3600:
                                mouse_movement_for_circle = False
                                if distance < 900:
                                    arrow_start = circle[1]
                                    arrow_tail = circle[0]
                                    arrow_tail_i = i
                                    mouse_movement_for_line = True
                                break
                        if mouse_movement_for_circle is True:
                            pygame.draw.circle(screen, red, pos, circle_radius, 1)
                            circle_text = '%s%d' % ('Q', circle_number)
                            circle_number += 1
                            text = font.render(circle_text, 0, red)
                            screen.blit(text, (pos[0] - 10, pos[1] - 5))
                            circle_list.append((circle_text, pos))
                    if event.__dict__['button'] == 3:
                        # TODO:右键菜单
                        break
                if event.type == pygame.MOUSEBUTTONUP:
                    if mouse_movement_for_line is True:
                        pos = event.__dict__['pos']
                        for i, circle in enumerate(circle_list):
                            distance = get_distance(pos, circle)
                            if distance < circle_radius * circle_radius:
                                arrow_end = circle[1]
                                arrow_head = circle[0]
                                arrow_head_i = i
                                k = get_k(arrow_start, arrow_end)
                                if k != 0:
                                    draw_arrow(screen, red, arrow_start, arrow_end, k)
                                    line_list.append((arrow_text, arrow_tail, arrow_head, arrow_tail_i, arrow_head_i))
                                    arrow_start = ()
                                    arrow_end = ()
                                break
                        mouse_movement_for_line = False
                    if has_circle_motion is True:
                        has_circle_motion = False
                if event.type == pygame.MOUSEMOTION:
                    if has_circle_motion is True:
                        new_mouse_position = pygame.mouse.get_pos()
                        circle_list[circle_for_move_i] = (circle_list[circle_for_move_i][0], new_mouse_position)
                        flush(screen, circle_list, red, circle_radius, line_list, font, change2mouse, button_rects)

        mouse_movement_for_circle = True

        pygame.display.flip()


def menu_bar(surface):
    """
    创建含有多个按钮的菜单栏
    :param surface: 菜单栏所在平面
    :return: 每个按钮的rect
    """

    mouse_rect = mouse_button(surface)
    pen_rect = pen_button(surface)
    run_rect = run_button(surface)
    return mouse_rect, pen_rect, run_rect


def menu_bar_clicked(surface):
    """
    加载按下按钮时的切换图片
    :param surface: 按钮所在平面
    :return: 光标， 铅笔， 运行的surface
    """

    run_button_clicked = pygame.image.load('images/运行_clicked.png')
    mouse_button_clicked = pygame.image.load('images/光标_clicked.png')
    pen_button_clicked = pygame.image.load('images/铅笔_clicked.png')
    return mouse_button_clicked, pen_button_clicked, run_button_clicked


def mouse_button(surface):
    """
    创建一个切换为鼠标动作的按钮
    :param surface: 按钮所在平面
    :return: 按钮的左， 上， 宽， 高
    """

    mouse_button = pygame.image.load('images/光标.png')
    mouse_button_rect = mouse_button.get_rect()
    mouse_button_rect.move_ip(0, 0)
    surface.blit(mouse_button, mouse_button_rect)

    return mouse_button_rect.left, mouse_button_rect.top, mouse_button_rect.width, mouse_button_rect.height, mouse_button


def pen_button(surface):
    """
    创建一个切换为画笔动作的按钮
    :param surface: 按钮所在平面
    :return: 按钮的左， 上， 宽， 高
    """

    pen_button = pygame.image.load('images/铅笔.png')
    pen_button_rect = pen_button.get_rect()
    pen_button_rect.move_ip(33, 0)
    surface.blit(pen_button, pen_button_rect)

    return pen_button_rect.left, pen_button_rect.top, pen_button_rect.width, pen_button_rect.height, pen_button


def run_button(surface):
    """
    创建一个运行自动机的按钮
    :param surface: 按钮所在平面
    :return: 按钮的左， 上， 宽， 高
    """

    run_button = pygame.image.load('images/运行.png')
    run_button_rect = run_button.get_rect()
    run_button_rect.move_ip(66, 0)
    surface.blit(run_button, run_button_rect)

    return run_button_rect.left, run_button_rect.top, run_button_rect.width, run_button_rect.height, run_button


def get_distance(pos, circle):
    """
    得到鼠标位置和任一圆的位置关系
    :param pos: 鼠标位置
    :param circle: 状态圆
    :return: distance
    """

    distance = (pos[0] - circle[1][0]) * (pos[0] - circle[1][0]) + \
               (pos[1] - circle[1][1]) * (pos[1] - circle[1][1])
    return distance


def get_k(arrow_start, arrow_end):
    """
    获得辅助计算箭头的比例值k
    :param arrow_start: 箭头开始位置
    :param arrow_end: 箭头结束位置
    :return: k
    """

    k = ((arrow_start[0] - arrow_end[0]) * (arrow_start[0] - arrow_end[0]) +
         (arrow_start[1] - arrow_end[1]) * (arrow_start[1] - arrow_end[1])) / (30 * 30)
    k = k ** 0.5
    return k


def draw_arrow(surface, color, arrow_start, arrow_end, k, volume=7):
    """
    画一个箭头
    :param surface: 箭头所在平面
    :param color: 箭头颜色
    :param arrow_start: 箭头开始的位置
    :param arrow_end: 箭头结束的位置
    :param k: 箭头的比例
    :param volume: 箭头的大小
    :return: None
    """

    arrow_start_ = (arrow_end[0] - arrow_start[0]) / k + arrow_start[0], \
                   (arrow_end[1] - arrow_start[1]) / k + arrow_start[1]
    arrow_end_ = arrow_end[0] - (arrow_end[0] - arrow_start[0]) / k, \
                 arrow_end[1] - (arrow_end[1] - arrow_start[1]) / k
    k_arrow_head = ((30 * 30 * k * k) / (volume * volume)) ** 0.5
    anchor_point = arrow_end_[0] - (arrow_end_[0] - arrow_start_[0]) / k_arrow_head, \
                   arrow_end_[1] - (arrow_end_[1] - arrow_start_[1]) / k_arrow_head
    upper_point = anchor_point[0] + (anchor_point[1] - arrow_end_[1]), \
                  anchor_point[1] + (arrow_end_[0] - anchor_point[0])
    downer_point = anchor_point[0] - (anchor_point[1] - arrow_end_[1]), \
                   anchor_point[1] - (arrow_end_[0] - anchor_point[0])
    pygame.draw.line(surface, color, arrow_start_, arrow_end_)
    pygame.draw.line(surface, color, upper_point, arrow_end_)
    pygame.draw.line(surface, color, downer_point, arrow_end_)
    return None


def flush(screen, circle_list, circle_color, circle_radius, line_list, font, change2mouse, button_rects):
    """
    刷新当前界面
    :param screen: 当前界面
    :param circle_list: 状态表
    :param circle_color: 状态圆颜色
    :param circle_radius: 状态圆半径
    :param line_list: 箭头颜色
    :param font: 状态圆字体
    :return: None
    """

    screen.fill((255, 255, 255))

    # left, top, width, height, mouse_button->surface
    mouse_surface = button_rects[0][4]
    pen_surface = button_rects[1][4]
    run_surface = button_rects[2][4]
    button_clicked_surfaces = menu_bar_clicked(screen)
    mouse_button_clicked = button_clicked_surfaces[0]
    pen_button_clicked = button_clicked_surfaces[1]
    run_button_clicked = button_clicked_surfaces[2]
    button_mouse_rect = mouse_surface.get_rect()
    button_mouse_rect.move_ip(0, 0)
    button_pen_rect = pen_surface.get_rect()
    button_pen_rect.move_ip(33, 0)
    button_run_rect = run_surface.get_rect()
    button_run_rect.move_ip(66, 0)
    if change2mouse is True:
        screen.blit(mouse_button_clicked, button_mouse_rect)
        screen.blit(pen_surface, button_pen_rect)
    else:
        screen.blit(mouse_surface, button_mouse_rect)
        screen.blit(pen_button_clicked, button_pen_rect)
    screen.blit(run_surface, button_run_rect)

    for circle in circle_list:
        pygame.draw.circle(screen, circle_color, circle[1], circle_radius, 1)
        text = font.render(circle[0], 0, circle_color)
        screen.blit(text, (circle[1][0] - 10, circle[1][1] - 5))
    for line in line_list:
        draw_arrow(screen, circle_color, circle_list[line[3]][1], circle_list[line[4]][1],
                   get_k(circle_list[line[3]][1], circle_list[line[4]][1]))
    return


def mouse_action():
    return


def pen_action():
    return


if __name__ == '__main__':
    main()
