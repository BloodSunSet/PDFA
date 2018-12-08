import pygame
import sys


def main():
    pygame.init()
    
    size = width, height = 320, 240
    white = 255, 255, 255
    red = 255, 0, 0
    circle_list = []  # circle_text, circle_center 
    line_list = []  # arrow_tail, arrow_head
    
    screen = pygame.display.set_mode(size)
    screen.fill(white)
    while 1:
        arrow_start = ()
        arrow_end = ()
        arrow_tail = ''
        circle_text = 'Q0'
        arrow_text = 'a'
        mouse_movement_for_circle = True
        mouse_movement_for_line = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.__dict__['pos']
                if event.__dict__['button'] == 1:
                    for circle in circle_list:
                        distance = (pos[0] - circle[1][0]) * (pos[0] - circle[1][0]) + \
                                   (pos[1] - circle[1][1]) * (pos[1] - circle[1][1])
                        if distance < 400:
                            arrow_start = circle[1]
                            arrow_tail = circle[0]
                            # mouse_movement_for_circle is False
                            # TODO:解决重复位置画圆的问题，解决无法划线的问题
                            break
                    if mouse_movement_for_circle is True:
                        pygame.draw.circle(screen, red, pos, 20, 1)
                        circle_list.append((circle_text, pos))
                        mouse_movement_for_line = True
                if event.__dict__['button'] == 3:
                    # TODO:右键菜单
                    break
            if event.type == pygame.MOUSEBUTTONUP:
                for circle in circle_list:
                    distance = (pos[0] - circle[1][0]) * (pos[0] - circle[1][0]) + \
                               (pos[1] - circle[1][1]) * (pos[1] - circle[1][1])
                    print('up distance=', distance)
                    if distance < 400 and mouse_movement_for_line is True:
                        arrow_end = circle[1]
                        arrow_head = circle[0]
                        pygame.draw.line(screen, red, arrow_start, arrow_end)
                        line_list.append((arrow_text, arrow_tail, arrow_end))
                        mouse_movement_for_line = False
                        break
                
        pygame.display.update()


if __name__ == '__main__':
    main()
