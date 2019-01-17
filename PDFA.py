import pygame
import tkinter as tk
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import *
import os

root = tk.Tk()
root.title("自动机的状态转换图表示")
embed = tk.Frame(root, width=500, height=500)  # creates embed frame for pygame window
embed.grid(columnspan=600, rowspan=500)  # Adds grid
embed.pack(side=LEFT)  # packs window to the left
# buttonwin = tk.Frame(root, width=75, height=500)
# buttonwin.pack(side=LEFT)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'


def menu_bar(surface):
    """
    创建含有多个按钮的菜单栏
    :param surface: 菜单栏所在平面
    :return: 每个按钮的rect
    """

    mouse_rect = mouse_button(surface)
    pen_rect = pen_button(surface)
    run_rect = run_button(surface)
    load_rect = load_button(surface)
    save_rect = save_button(surface)
    return mouse_rect, pen_rect, run_rect, load_rect, save_rect


def menu_bar_clicked(surface):
    """
    加载按下按钮时的切换图片
    :param surface: 按钮所在平面
    :return: 光标， 铅笔， 运行的surface
    """

    run_button_clicked = pygame.image.load('images/运行_clicked.png')
    mouse_button_clicked = pygame.image.load('images/光标_clicked.png')
    pen_button_clicked = pygame.image.load('images/铅笔_clicked.png')
    load_button_clicked = pygame.image.load('images/加载_clicked.png')
    save_button_clicked = pygame.image.load('images/保存_clicked.png')
    return mouse_button_clicked, pen_button_clicked, run_button_clicked, load_button_clicked, save_button_clicked


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


def load_button(surface):
    """
    创建一个加载本地保存文件的按钮
    :param surface: 按钮所在平面
    :return: 按钮的左， 上， 宽， 高
    """

    load_button = pygame.image.load('images/加载.png')
    load_button_rect = load_button.get_rect()
    load_button_rect.move_ip(99, 0)
    surface.blit(load_button, load_button_rect)

    return load_button_rect.left, load_button_rect.top, load_button_rect.width, load_button_rect.height, load_button


def save_button(surface):
    """
    创建一个加载本地保存文件的按钮
    :param surface: 按钮所在平面
    :return: 按钮的左， 上， 宽， 高
    """

    save_button = pygame.image.load('images/保存.png')
    save_button_rect = save_button.get_rect()
    save_button_rect.move_ip(132, 0)
    surface.blit(save_button, save_button_rect)

    return save_button_rect.left, save_button_rect.top, save_button_rect.width, save_button_rect.height, save_button


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


def draw_origin_arrow(surface, arrow_end):
    """
    画一个标记初态的空心箭头
    :param surface: 箭头所在平面
    :param arrow_end: 箭头指向状态圆接触点
    :return: None
    """

    length = 50
    right_part_length = 20
    left_part_height = 20
    right_part_height = 40

    blue = (0, 0, 255)

    left_x = arrow_end[0] - length
    left_top_y = arrow_end[1] - left_part_height / 2
    left_bottom_y = arrow_end[1] + left_part_height / 2
    right_x = arrow_end[0] - right_part_length
    right_top_y = arrow_end[1] - left_part_height / 2
    right_bottom_y = arrow_end[1] + left_part_height / 2
    triangle_x = right_x
    triangle_top_y = arrow_end[1] - right_part_height / 2
    triangle_bottom_y = arrow_end[1] + right_part_height / 2

    point_list = [(left_x, left_top_y), (left_x, left_bottom_y), (right_x, right_bottom_y),
                  (triangle_x, triangle_bottom_y), arrow_end, (triangle_x, triangle_top_y),
                  (right_x, right_top_y)]

    pygame.draw.aalines(surface, blue, 1, point_list)
    return None


def flush(screen, circle_list, circle_color, circle_radius, line_list, font, change2mouse, button_rects,
          has_origin, origin_circle, final_circles):
    """
    刷新当前界面
    :param screen: 当前界面
    :param circle_list: 状态表
    :param circle_color: 状态圆颜色
    :param circle_radius: 状态圆半径
    :param line_list: 箭头颜色
    :param font: 状态圆字体
    :param change2mouse: 是否为编辑模式
    :param button_rects: 功能按键栏
    :param has_origin: 是否有初态
    :param origin_circle: 初态圆id
    :param final_circles: 终态圆集
    :return: None
    """

    screen.fill((255, 255, 255))

    # left, top, width, height, mouse_button->surface
    mouse_surface = button_rects[0][4]
    pen_surface = button_rects[1][4]
    run_surface = button_rects[2][4]
    load_surface = button_rects[3][4]
    save_surface = button_rects[4][4]
    button_clicked_surfaces = menu_bar_clicked(screen)
    mouse_button_clicked = button_clicked_surfaces[0]
    pen_button_clicked = button_clicked_surfaces[1]
    run_button_clicked = button_clicked_surfaces[2]
    load_button_clicked = button_clicked_surfaces[3]
    save_button_clicked = button_clicked_surfaces[4]
    button_mouse_rect = mouse_surface.get_rect()
    button_mouse_rect.move_ip(0, 0)
    button_pen_rect = pen_surface.get_rect()
    button_pen_rect.move_ip(33, 0)
    button_run_rect = run_surface.get_rect()
    button_run_rect.move_ip(66, 0)
    button_load_rect = load_surface.get_rect()
    button_load_rect.move_ip(99, 0)
    button_save_rect = save_surface.get_rect()
    button_save_rect.move_ip(132, 0)
    if change2mouse is True:
        screen.blit(mouse_button_clicked, button_mouse_rect)
        screen.blit(pen_surface, button_pen_rect)
    else:
        screen.blit(mouse_surface, button_mouse_rect)
        screen.blit(pen_button_clicked, button_pen_rect)
    screen.blit(run_surface, button_run_rect)
    screen.blit(load_surface, button_load_rect)
    screen.blit(save_surface, button_save_rect)

    for circle in circle_list:
        pygame.draw.circle(screen, circle_color, circle[1], circle_radius, 1)
        text = font.render(circle[0], 0, circle_color)
        screen.blit(text, (circle[1][0] - 10, circle[1][1] - 5))
        if has_origin is True and origin_circle == circle[2]:
            draw_origin_arrow(screen, (circle[1][0] - 30, circle[1][1]))
        if final_circles.__len__() > 0:
            if circle[2] in final_circles:
                pygame.draw.circle(screen, circle_color, circle[1], circle_radius - 3, 1)
    for line in line_list:
        arrow_tail_index = arrow_head_index = 0
        for i, circle in enumerate(circle_list):
            if line[3] == circle[2]:
                arrow_tail_index = i
            if line[4] == circle[2]:
                arrow_head_index = i
        draw_arrow(screen, circle_color, circle_list[line[3]][1], circle_list[line[4]][1],
                   get_k(circle_list[arrow_tail_index][1], circle_list[arrow_head_index][1]))

    root.update()

    return


def right_click_menu(surface, pos, origin_color, final_color):
    """
    创建一个右键菜单
    :param surface: 菜单所在平面
    :param pos: 菜单左上角所在位置
    :param origin_color: 初态状态颜色
    :param final_color: 终态状态颜色
    :return: 菜单位置和菜单大小
    """

    width = 100
    height = 150
    grey = (225, 225, 225)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    font = pygame.font.Font(r'fonts\freesansbold.ttf', 15)
    pygame.draw.rect(surface, blue, (pos[0], pos[1], width, height), 3)
    pygame.draw.rect(surface, grey, (pos[0], pos[1], width, height))
    set_origin_text = font.render(u'origin', 1, origin_color)
    set_final_text = font.render(u'final', 1, final_color)
    set_change_text = font.render(u'change', 1, black)
    surface.blit(set_origin_text, (pos[0] + 20, pos[1] + 10))
    surface.blit(set_final_text, (pos[0] + 20, pos[1] + 30))
    surface.blit(set_change_text, (pos[0] + 20, pos[1] + 50))
    return pos, width, height


def load_file():
    filename = tk.filedialog.askopenfilename(initialdir="G:/python/PDFA/PDFA/saves")
    content = []
    if filename:
        with open(filename, 'r') as f:
            temp_content = f.readlines()
            for line in temp_content:
                line = line.strip()
                content.append(line)

            circle_list = []
            line_list = []
            final_circles = []

            origin_index = content.index('###origin_circle###')
            final_index = content.index('###final_circles###')
            line_index = content.index('###line_list###')
            circle_index = content.index('###circle_list###')
            origin_circle = content[origin_index + 1: final_index]
            final_temp_circles = content[final_index + 1: circle_index]
            circles = content[circle_index + 1: line_index]
            lines = content[line_index + 1:]

            for final_circle in final_temp_circles:
                final_circles.append(int(final_circle))
            for circle in circles:
                temp_circle_list = circle.split(',')
                circle_list.append((temp_circle_list[0], (int(temp_circle_list[1]), int(temp_circle_list[2])),
                                    int(temp_circle_list[3])))
            for line in lines:
                temp_line_list = line.split(',')
                line_list.append((temp_line_list[0], temp_line_list[1], temp_line_list[2],
                                  int(temp_line_list[3]), int(temp_line_list[4])))

            return origin_circle, final_circles, circle_list, line_list
    else:
        return ''


def save_file():
    file_name = tk.filedialog.asksaveasfilename(initialdir="G:/python/PDFA/PDFA/saves")
    if file_name:
        with open(file_name, 'w') as f:
            f.write('###origin_circle###\n')
            f.write(str(origin_circle))
            f.write('\n')
            f.write('###final_circles###\n')
            for final_circle in final_circles:
                f.write(str(final_circle))
                f.write('\n')
            f.write('###circle_list###\n')
            for circle in circle_list:
                f.write(circle[0])
                f.write(',')
                f.write(str(circle[1][0]))
                f.write(',')
                f.write(str(circle[1][1]))
                f.write(',')
                f.write(str(circle[2]))
                f.write('\n')
            f.write('###line_list###\n')
            for line in line_list:
                f.write(line[0])
                f.write(',')
                f.write(line[1])
                f.write(',')
                f.write(line[2])
                f.write(',')
                f.write(str(line[3]))
                f.write(',')
                f.write(str(line[4]))
                f.write('\n')


def create_status_table():
    top = Toplevel()
    top.title(u'状态转换表')
    tree = ttk.Treeview(top)  # 表格
    tree["columns"] = ("a", "final")
    tree.column("a", width=70)  # 表示列,不显示
    tree.column("final", width=70)

    tree.heading("a", text="a")  # 显示表头
    tree.heading("final", text=u"终态")

    tree_data = []
    for circle in circle_list:
        tree_data.append([circle[0], '', circle[2]])
    for line in line_list:
        for row in tree_data:
            if line[1] == row[0]:
                row[1] += line[2]
    for i, row in enumerate(tree_data):
        text = row[0] if row[2] != origin_circle else row[0] + '->'
        values = (row[1], "0") if row[2] not in final_circles else (row[1], "1")
        tree.insert("", i, text=text, values=values)

    tree.pack()


screen = pygame.display.set_mode((500, 500))
screen.fill(pygame.Color(255, 255, 255))
pygame.init()
white = 255, 255, 255
red = 255, 0, 0
black = 0, 0, 0
circle_list = []  # circle_text, circle_center, circle_number
line_list = []  # arrow_text, arrow_tail, arrow_head, arrow_tail_i, arrow_head_i

screen.fill(white)
button_rects = menu_bar(screen)  # mouse, pen, run, load, save

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
mouse_movement_for_draw_circle = True
mouse_movement_for_line = False

change2mouse = False
run = False

has_circle_motion = False
right_click = False
right_menu_info = []
has_origin = False
origin_circle = -1
final_circles = []
origin_color = black
final_color = black
selected_circle = -1
mouse_position = ()

font = pygame.font.Font(r'fonts\freesansbold.ttf', 20)
pygame.display.update()


def on_closing():
    root.destroy()


root.update()
root.protocol("WM_DELETE_WINDOW", on_closing)

while True:
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
    flush(screen, circle_list, red, circle_radius, line_list, font, change2mouse, button_rects, has_origin,
          origin_circle, final_circles)
    if right_click is True:
        origin_color = red if circle_list[selected_circle][2] == origin_circle else black
        final_color = red if circle_list[selected_circle][2] in final_circles else black
        right_menu_info = right_click_menu(screen, mouse_position, origin_color, final_color)

    for event in pygame.event.get():
        # if event.type == pygame.QUIT:
        #     sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.__dict__['pos']  # x, y
            if event.__dict__['button'] == 1:
                if right_click is True:
                    if right_menu_info[0][0] < pos[0] < right_menu_info[0][0] + right_menu_info[1]:
                        if right_menu_info[0][1] < pos[1] < right_menu_info[0][1] + right_menu_info[2]:
                            if right_menu_info[0][1] + 10 < pos[1] < right_menu_info[0][1] + 30:  # 点击了origin
                                if has_origin is False:
                                    origin_circle = circle_list[selected_circle][2]
                                    has_origin = True
                                elif has_origin is True:
                                    if selected_circle == origin_circle:
                                        has_origin = False
                                        origin_circle = -1
                                    else:
                                        # TODO:警告不可添加多个初态，应先取消之前的初态
                                        break
                            if right_menu_info[0][1] + 30 < pos[1] < right_menu_info[0][1] + 50:  # 点击了final
                                if circle_list[selected_circle][2] in final_circles:
                                    final_circles.remove(circle_list[selected_circle][2])
                                else:
                                    final_circles.append(circle_list[selected_circle][2])
                            if right_menu_info[0][1] + 50 < pos[1] < right_menu_info[0][1] + 70:  # 点击了change
                                # TODO:change响应
                                break
                            right_click = False
                            # TODO:写菜单响应函数
                            break
                    else:
                        right_click = False

                if (pos[1] - circle_radius) < 32:  # 菜单栏
                    if button_rects[0][0] <= pos[0] <= (button_rects[0][0] + button_rects[0][2]):
                        change2mouse = True
                    if button_rects[1][0] <= pos[0] <= (button_rects[1][0] + button_rects[1][2]):
                        change2mouse = False
                    if button_rects[2][0] <= pos[0] <= (button_rects[2][0] + button_rects[2][2]):
                        run = True
                        create_status_table()
                    if button_rects[3][0] <= pos[0] <= (button_rects[3][0] + button_rects[3][2]):
                        new_lists = load_file()
                        if new_lists != '':
                            if new_lists[0][0] != '':
                                origin_circle = int(new_lists[0][0])
                                has_origin = True
                            final_circles = new_lists[1]
                            circle_list = new_lists[2]
                            line_list = new_lists[3]
                    if button_rects[4][0] <= pos[0] <= (button_rects[4][0] + button_rects[4][2]):
                        save_file()
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
                        mouse_movement_for_draw_circle = False
                        if distance < 900:
                            arrow_start = circle[1]
                            arrow_tail = circle[0]
                            arrow_tail_i = circle_list[i][2]
                            mouse_movement_for_line = True
                        break
                if mouse_movement_for_draw_circle is True:
                    pygame.draw.circle(screen, red, pos, circle_radius, 1)
                    if circle_list.__len__() == 0:
                        circle_number = 0
                    else:
                        circle_number = circle_list[circle_list.__len__() - 1][2] + 1
                    circle_text = '%s%d' % ('Q', circle_number)
                    text = font.render(circle_text, 0, red)
                    screen.blit(text, (pos[0] - 10, pos[1] - 5))
                    circle_list.append((circle_text, pos, circle_number))
            if event.__dict__['button'] == 3:
                if change2mouse is True:
                    for i, circle in enumerate(circle_list):
                        distance = get_distance(pos, circle)
                        if distance < 900:
                            right_click = True
                            mouse_position = pos
                            selected_circle = i
                break
        if event.type == pygame.MOUSEBUTTONUP:
            if mouse_movement_for_line is True:
                pos = event.__dict__['pos']
                for i, circle in enumerate(circle_list):
                    distance = get_distance(pos, circle)
                    if distance < circle_radius * circle_radius:
                        arrow_end = circle[1]
                        arrow_head = circle[0]
                        arrow_head_i = circle_list[i][2]
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
                circle_list[circle_for_move_i] = (circle_list[circle_for_move_i][0], new_mouse_position,
                                                  circle_list[circle_for_move_i][2])
                flush(screen, circle_list, red, circle_radius, line_list, font, change2mouse, button_rects,
                      has_origin, origin_circle, final_circles)

    mouse_movement_for_draw_circle = True

    pygame.display.flip()
