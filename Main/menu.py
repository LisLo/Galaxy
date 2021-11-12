from kivy.uix.relativelayout import RelativeLayout


class MenuWidget(RelativeLayout):
    # for not activating the Button of the menu
    def on_touch_down(self, touch):
        if self.on_opacity == 0:
            return False
        # for manage the button on Menu Screen
        return super(RelativeLayout, self).on_touch_down(touch)
