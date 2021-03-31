from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty,ObjectProperty,ListProperty
from kivy.clock import Clock
class Pipe(Widget):
    gap_size = NumericProperty(100)
    cap_size = NumericProperty(10)
    pipe_center = NumericProperty(0)
    btm_body_pos = NumericProperty(0)
    btm_cap_pos = NumericProperty(0)
    top_cap_pos = NumericProperty(0)
    top_body_pos = NumericProperty(0)

    #texture
    lower_body_texture = ObjectProperty(None)
    top_body_texture = ObjectProperty(None)

    low_tex_coords= ListProperty((0,0, 1,0, 1,1, 0,1)) 
    top_tex_coords= ListProperty((0,0, 1,0, 1,1, 0,1)) 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lower_body_texture = Image(source='body.png').texture
        self.lower_body_texture.wrap = 'repeat'
        self.top_body_texture = Image(source='body.png').texture
        self.top_body_texture.wrap = 'repeat'


    def on_size(self,*args):
        lower_body_size = self.btm_cap_pos-self.btm_body_pos
        top_body_size = self.top - self.top_body_pos
        self.low_tex_coords[5] = lower_body_size / 13
        self.low_tex_coords[7] = lower_body_size/13
        self.top_tex_coords[5] = top_body_size/13
        self.top_tex_coords[7] = top_body_size/13
    
    def on_pipe_center(self, *args):
        Clock.schedule_once(self.on_size,0)

        

