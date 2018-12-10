import pygame
import sys


def main():
    pygame.init()
    
    size = width, height = 1000, 800
    white = 255, 255, 255
    red = 255, 0, 0
    circle_list = []  # circle_text, circle_center 
    line_list = []  # arrow_tail, arrow_head
    
    screen = pygame.display.set_mode(size)
    screen.fill(white)
    mouse_rect = mouse_button(screen)  # left, top, width, height
    pen_rect = pen_button(screen)
    print(mouse_rect, pen_rect)

    circle_number = 0
    circle_radius = 30
    arrow_start = ()
    arrow_end = ()
    arrow_tail = ''
    arrow_text = 'a'
    mouse_movement_for_circle = True
    mouse_movement_for_line = False
    font = pygame.font.Font(None, 20)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(line_list)
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.__dict__['pos']  # x, y
                if event.__dict__['button'] == 1:
                    print(pos[1] + circle_radius)
                    if (pos[1] - circle_radius) < (mouse_rect[1] + mouse_rect[3]):
                        if mouse_rect[0] <= pos[0] <= (mouse_rect[0] + mouse_rect[2]):
                            mouse_action()
                        if pen_rect[0] <= pos[0] <= (pen_rect[0] + pen_rect[2]):
                            pen_action()
                        continue
                    for circle in circle_list:
                        distance = (pos[0] - circle[1][0]) * (pos[0] - circle[1][0]) + \
                                   (pos[1] - circle[1][1]) * (pos[1] - circle[1][1])
                        if distance < 3600:
                            arrow_start = circle[1]
                            arrow_tail = circle[0]
                            mouse_movement_for_circle = False
                            mouse_movement_for_line = True
                            print(mouse_movement_for_circle)
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

        pygame.display.update()


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

    return mouse_button_rect.left, mouse_button_rect.top, mouse_button_rect.width, mouse_button_rect.height


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

    return pen_button_rect.left, pen_button_rect.top, pen_button_rect.width, pen_button_rect.height


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
         (arrow_start[1] - arrow_end[1]) * (arrow_start[1] - arrow_end[1])) / 30 * 30
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
    print(arrow_start, arrow_start_, '\n', arrow_end, arrow_end_)
    pygame.draw.line(surface, color, arrow_start_, arrow_end_)
    k_arrow_head = ((30 * 30 * k * k) / (volume * volume)) ** 0.5
    anchor_point = arrow_end_[0] - (arrow_end_[0] - arrow_start_[0]) / k_arrow_head, \
                   arrow_end_[1] - (arrow_end_[1] - arrow_start_[1]) / k_arrow_head
    upper_point = anchor_point[0] + (anchor_point[1] - arrow_end_[1]), \
                  anchor_point[1] + (arrow_end_[0] - anchor_point[0])
    downer_point = anchor_point[0] - (anchor_point[1] - arrow_end_[1]), \
                   anchor_point[1] - (arrow_end_[0] - anchor_point[0])
    pygame.draw.line(surface, color, upper_point, arrow_end_)
    pygame.draw.line(surface, color, downer_point, arrow_end_)
    return None


def mouse_action():
    return


def pen_action():
    return


if __name__ == '__main__':
    main()
