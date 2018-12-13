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
    mouse_rect = mouse_button(screen)  # left, top, width, height, mouse_button->surface
    pen_rect = pen_button(screen)  # left, top, width, height, pen_button->surface
    mouse_surface = mouse_rect[4]
    pen_surface = pen_rect[4]
    button_surfaces = mouse_surface, pen_surface

    circle_number = 0
    circle_radius = 30
    arrow_start = ()
    arrow_end = ()
    arrow_tail = ''
    arrow_text = 'a'
    mouse_movement_for_circle = True
    mouse_movement_for_line = False

    button_animation = False
    change2mouse = False
    change2pen = False
    button_status = change2mouse, change2pen
    return_mark = False
    pixel = 2
    temp_button_surface = ''

    font = pygame.font.Font(r'fonts\freesansbold.ttf', 20)

    while 1:
        button_status = change2mouse, change2pen

        if button_animation is True:
            for i in range(button_status.__len__()):
                if button_status[i] is True:
                    temp_button_surface = button_surfaces[i]
            button_rect = temp_button_surface.get_rect()
            button_rect.inflate_ip((-pixel, -pixel))
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

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.__dict__['pos']  # x, y
                    if event.__dict__['button'] == 1:
                        if (pos[1] - circle_radius) < (mouse_rect[1] + mouse_rect[3]):
                            button_animation = True
                            if mouse_rect[0] <= pos[0] <= (mouse_rect[0] + mouse_rect[2]):
                                change2mouse = True
                                change2pen = False
                            if pen_rect[0] <= pos[0] <= (pen_rect[0] + pen_rect[2]):
                                change2pen = True
                                change2mouse = False
                                # TODO:补全画笔动画
                            continue

                        if change2mouse is True:
                            continue

                        for circle in circle_list:
                            distance = get_distance(pos, circle)
                            if distance < 3600:
                                arrow_start = circle[1]
                                arrow_tail = circle[0]
                                mouse_movement_for_circle = False
                                mouse_movement_for_line = True
                                # TODO:解决除数为零错误
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
                if event.type == pygame.MOUSEBUTTONUP and mouse_movement_for_line is True:
                    pos = event.__dict__['pos']
                    for circle in circle_list:
                        distance = get_distance(pos, circle)
                        if distance < circle_radius * circle_radius:
                            arrow_end = circle[1]
                            arrow_head = circle[0]
                            k = get_k(arrow_start, arrow_end)
                            if k != 0:
                                draw_arrow(screen, red, arrow_start, arrow_end, k)
                                line_list.append((arrow_text, arrow_tail, arrow_head))
                                arrow_start = ()
                                arrow_end = ()
                            break
                    mouse_movement_for_line = False
        mouse_movement_for_circle = True

        pygame.display.flip()


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


def mouse_action():
    return


def pen_action():
    return


if __name__ == '__main__':
    main()
