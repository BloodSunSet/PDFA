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

    arrow_start = ()
    arrow_end = ()
    arrow_tail = ''
    circle_number = 0
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
                pos = event.__dict__['pos']
                if event.__dict__['button'] == 1:
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
                        pygame.draw.circle(screen, red, pos, 30, 1)
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
                    distance = (pos[0] - circle[1][0]) * (pos[0] - circle[1][0]) + \
                               (pos[1] - circle[1][1]) * (pos[1] - circle[1][1])
                    if distance < 900:
                        arrow_end = circle[1]
                        arrow_head = circle[0]
                        k = ((arrow_start[0] - arrow_end[0]) * (arrow_start[0] - arrow_end[0]) +
                             (arrow_start[1] - arrow_end[1]) * (arrow_start[1] - arrow_end[1])) / 900
                        k_arrow_head = ((900 * k) / 49) ** 0.5
                        k = k ** 0.5
                        print(k_arrow_head, '\n', k)
                        if k != 0:
                            arrow_start_ = (arrow_end[0] - arrow_start[0]) / k + arrow_start[0], \
                                           (arrow_end[1] - arrow_start[1]) / k + arrow_start[1]
                            arrow_end_ = arrow_end[0] - (arrow_end[0] - arrow_start[0]) / k, \
                                         arrow_end[1] - (arrow_end[1] - arrow_start[1]) / k
                            anchor_point = arrow_end_[0] - (arrow_end_[0] - arrow_start_[0]) / k_arrow_head, \
                                           arrow_end_[1] - (arrow_end_[1] - arrow_start_[1]) / k_arrow_head
                            upper_point = anchor_point[0] + (anchor_point[1] - arrow_end_[1]), \
                                          anchor_point[1] + (arrow_end_[0] - anchor_point[0])
                            downer_point = anchor_point[0] - (anchor_point[1] - arrow_end_[1]), \
                                           anchor_point[1] - (arrow_end_[0] - anchor_point[0])
                            pygame.draw.line(screen, red, upper_point, arrow_end_)
                            pygame.draw.line(screen, red, downer_point, arrow_end_)
                            pygame.draw.line(screen, red, arrow_start_, arrow_end_)
                            print(arrow_start, arrow_start_, '\n', arrow_end, arrow_end_)
                            line_list.append((arrow_text, arrow_tail, arrow_head))
                            arrow_start = ()
                            arrow_end = ()
                        break
                mouse_movement_for_line = False
        mouse_movement_for_circle = True

        pygame.display.update()


if __name__ == '__main__':
    main()
