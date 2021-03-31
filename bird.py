from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty,NumericProperty
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.window import Window
from pipe import Pipe
class Background(Widget):
    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.floor_texture = Image(source='floor.png').texture
        self.floor_texture.wrap = 'repeat'
        self.floor_texture.uvsize = (Window.width/self.floor_texture.width,-1)
        self.cloud_texture = Image(source='cloud.png').texture
        self.cloud_texture.wrap = 'repeat'
        self.cloud_texture.uvsize = (Window.width/self.cloud_texture.width,-1)
    def update(self,passed_time):
        # update the uvpos the texture
        self.cloud_texture.uvpos = ((self.cloud_texture.uvpos[0]+ passed_time) % Window.width ,\
            self.cloud_texture.uvpos[1])
        self.floor_texture.uvpos = ((self.floor_texture.uvpos[0]+ passed_time) % Window.width ,\
            self.floor_texture.uvpos[1])
         #redrwa the texture
        texture = self.property('cloud_texture')
        texture.dispatch(self)
        texture = self.property('floor_texture')
        texture.dispatch(self)

class Char(Image):
    velocity = NumericProperty(0)
    def on_touch_down(self,touch):
        self.source = 'bird1.png'
        self.velocity =150
        super().on_touch_down(touch)
    def on_touch_up(self,touch):
        self.source = 'bird2.png'
        super().on_touch_up(touch)


from random import randint
class Bird(App):
    GRAVITY = 300
    pipes = []

    def char_move(self,passed_time):
        char = self.root.ids.char
        char.y  += char.velocity * passed_time
        char.velocity = char.velocity - self.GRAVITY * passed_time
        self.check_collision()
    
    def check_collision(self):
        char = self.root.ids.char
        self.is_colliding = False
        for pipe in self.pipes:
            if pipe.collide_widget(char):
                self.is_colliding = True
                if char.y < pipe.pipe_center - pipe.gap_size /2:
                    self.gameover()
                elif char.y > pipe.pipe_center + pipe.gap_size /2:
                    self.gameover()
                
        if char.y < 100 or char.top > self.root.height:
            self.gameover()
        if self.was_collding and not self.is_colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text)+1)
        self.was_collding = self.is_colliding
        
    def gameover(self):
        
        for pipe in self.pipes:
            self.root.remove_widget(pipe)
        self.frame.cancel()
        self.root.ids.char.pos = (20,(self.root.height-100)/2)
        self.root.ids.button.disabled = False
        self.root.ids.button.opacity = 1

    def next_frame(self,passed_time):
        self.char_move(passed_time)
        self.move_pipes(passed_time)
        self.root.ids.background.update(passed_time)

        
        

    def start(self):
        self.pipes=[]
        self.was_collding = False
        self.root.ids.score.text = '0'
        self.frame = Clock.schedule_interval(self.next_frame,1/60)
        # create the pipes
        num_pipes = 50
        dis_pipes = Window.width / (5- 1)
        for i in range (num_pipes):
            pipe = Pipe()
            pipe.pipe_center = randint(100 + 100 ,self.root.height-100 )
            pipe.size_hint = (None,None)
            pipe.pos =(Window.width + i * dis_pipes, 100)
            pipe.size = (64, self.root.height - 100)

            self.pipes.append(pipe)
            self.root.add_widget(pipe)
        
    #move the pipes
    def move_pipes(self, passed_time):
        for pipe in self.pipes:
            pipe.x -= passed_time * 100

        # repostion the pipes
       


    
if __name__ == '__main__':
    Bird().run()