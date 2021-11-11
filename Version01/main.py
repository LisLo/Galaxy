# from io import StringIO
import os
import sys
from pathlib import Path


from kivy.config import Config
Config.set('graphics', 'width', 900)
Config.set('graphics', 'height', 400)

from kivy.utils import platform
from kivy.app import App
from kivy.properties import NumericProperty, Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.widget import Widget
from kivy.core.window import Window


root_path: Path = os.path.split((os.path.dirname(__file__)))[0]
sys.path.append(root_path)


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    # vertical numbers of lines
    V_NB_LINES = 10
    H_NB_LINES = 15
    V_LINES_SPACING = .2  # percentage in screen width
    H_LINES_SPACING = .2
    vertical_lines = []
    horizontal_lines = []

    # for moving down
    SPEED = 4
    current_offset_y = 0

    # for moving side
    SPEED_X = 20
    current_speed_x = 0
    current_offset_x = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width) + " H: " + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard.unbind(on_key_up=self.on_keyboard_up)
        self._keyboard = None

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def on_parent(self, widget, parent):
        # print("O PARENT W: " + str(self.width) + " H: " + str(self.height))
        pass

        # will allways call on_perspective_point_x and y
    def on_size(self, *args):
        # print("On SIZE W: " + str(self.width) + " H: " + str(self.height))
        # self.perspective_point_x = self.width / 2
        # self.perspective_point_y = self.height * 0.75
        # this two function will not longer nedded, because they will updated in the update function
        # self.update_vertical_lines()
        # self.update_horizontal_lines()
        pass

    def on_perspective_point_x(self, widget, value):
        # print("PX: " + str(value))
        pass

    def on_perspective_point_y(self, widget, value):
        # print("Py: " + str(value))
        pass

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_vertical_lines(self):
        centeral_line_x = int(self.width / 2)
        spacing = self.V_LINES_SPACING * self.width
        # self.line.points = [center_x, 0, center_x, 100]
        # *.5 for shifting the lines to the right
        offset = - int(self.V_NB_LINES / 2) + .5
        for i in range(0, self.V_NB_LINES):
            line_x = centeral_line_x + offset * spacing + self.current_offset_x

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1

    def update_horizontal_lines(self):
        centeral_line_x = int(self.width / 2)
        spacing = self.V_LINES_SPACING * self.width
        # self.line.points = [center_x, 0, center_x, 100]
        # *.5 for shifting the lines to the right
        offset = - int(self.V_NB_LINES / 2) + .5

        xmin = centeral_line_x + offset * spacing + self.current_offset_x
        xmax = centeral_line_x - offset * spacing + self.current_offset_x
        spacing_y = self.H_LINES_SPACING * self.height

        for i in range(0, self.H_NB_LINES):
            line_y = int(i * spacing_y) - self.current_offset_y
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def transform(self, x, y):
        # return self.transform2D(x, y)
        return self.transform_perspective(x, y)

    def transform2D(self, x, y):
        return int(x), int(y)

    def transform_perspective(self, x, y):
        # TO DO
        lin_y = y * self.perspective_point_y / self.height
        if lin_y > self.perspective_point_y:
            lin_y = self.perspective_point_y

        diff_x = x - self.perspective_point_x
        diff_y = self.perspective_point_y - lin_y
        factor_y = diff_y / self.perspective_point_y
        factor_y = pow(factor_y, 2)

        tr_x = self.perspective_point_x + diff_x * factor_y
        tr_y = (1 - factor_y) * self.perspective_point_y
        return int(tr_x), int(tr_y)

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_speed_x = self.SPEED_X
        elif keycode[1] == 'right':
            self.current_speed_x = - self.SPEED_X
        return True

    def on_keyboard_up(self, keyboard, keycode):
        self.current_speed_x = 0
        return True

    def on_touch_down(self, touch):
        if touch.x < self.width / 2:
            # print("<-")
            self.current_speed_x = self.SPEED_X
        else:
            # print("->")
            self.current_speed_x = - self.SPEED_X

    def on_touch_up(self, touch):
        # print("up")
        self.current_speed_x = 0

    # dt = delta time
    def update(self, dt):
        # print("dt: " + str(dt * 60))
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        # time_factor for better game performance on every device
        self.current_offset_y += self.SPEED * time_factor

        spacing_y = self.H_LINES_SPACING * self.height
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y

        # movement on the right
        self.current_offset_x += self.current_speed_x * time_factor


class TheGalaxyApp(App):
    pass


TheGalaxyApp().run()
