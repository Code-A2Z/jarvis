"""
Car Racing Game (Streamlit-compatible)
Refactored for brevity and maintainability.
"""
import pygame, random, math, json, os, sys
from enum import Enum
from dataclasses import dataclass
try:
    import streamlit as st
    from st_pygame import st_pygame
except ImportError:
    st = None
    st_pygame = None

SCREEN_WIDTH, SCREEN_HEIGHT, FPS = 800, 600, 60
COLORS = {
    'WHITE': (255,255,255), 'BLACK': (0,0,0), 'GRAY': (128,128,128), 'DARK_GRAY': (64,64,64),
    'LIGHT_GRAY': (192,192,192), 'YELLOW': (255,255,0), 'RED': (220,20,20), 'BLUE': (30,144,255),
    'GREEN': (34,139,34), 'ORANGE': (255,165,0), 'PURPLE': (138,43,226), 'ROAD_GRAY': (96,96,96),
    'GRASS_GREEN': (107,142,35), 'SKY_BLUE': (135,206,235), 'SHADOW': (0,0,0,100)
}
CAR_WIDTH, CAR_HEIGHT, ROAD_WIDTH, LANE_COUNT = 60, 120, 400, 3
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

class GameState(Enum):
    MENU, PLAYING, PAUSED, GAME_OVER, SETTINGS = range(5)
class CarType(Enum):
    SPORTS, SEDAN, TRUCK, POLICE = range(4)
@dataclass
class CarSpec:
    name: str; color: tuple; secondary_color: tuple; speed_multiplier: float; size_multiplier: float
CAR_SPECS = {
    CarType.SPORTS: CarSpec("Sports Car", COLORS['RED'], COLORS['BLACK'], 1.2, 0.9),
    CarType.SEDAN: CarSpec("Sedan", COLORS['BLUE'], COLORS['LIGHT_GRAY'], 1.0, 1.0),
    CarType.TRUCK: CarSpec("Truck", COLORS['ORANGE'], COLORS['DARK_GRAY'], 0.8, 1.3),
    CarType.POLICE: CarSpec("Police Car", COLORS['WHITE'], COLORS['BLUE'], 1.1, 1.0),
}
class Particle:
    def __init__(self, x, y, vx, vy, color, life, size=3):
        self.x, self.y, self.vx, self.vy, self.color, self.life, self.max_life, self.size = x, y, vx, vy, color, life, life, size
    def update(self):
        self.x += self.vx; self.y += self.vy; self.life -= 1; self.vy += 0.1; return self.life > 0
    def draw(self, screen):
        if self.life <= 0: return
        alpha = int(255 * (self.life / self.max_life))
        surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (self.size, self.size), self.size)
        screen.blit(surf, (self.x-self.size, self.y-self.size))
class ParticleSystem:
    def __init__(self): self.particles = []
    def add_explosion(self, x, y, intensity=20):
        for _ in range(intensity):
            a, s = random.uniform(0,2*math.pi), random.uniform(2,8)
            c = random.choice([COLORS['RED'], COLORS['ORANGE'], COLORS['YELLOW'], COLORS['WHITE']])
            self.particles.append(Particle(x, y, math.cos(a)*s, math.sin(a)*s, c, random.randint(30,60), random.randint(2,5)))
    def add_smoke(self, x, y, count=5):
        for _ in range(count):
            g = random.randint(100,150)
            self.particles.append(Particle(x, y, random.uniform(-1,1), random.uniform(-3,-1), (g,g,g), random.randint(40,80), random.randint(3,6)))
    def update(self): self.particles = [p for p in self.particles if p.update()]
    def draw(self, screen):
        for p in self.particles: p.draw(screen)
class Car:
    def __init__(self, x, y, car_type, is_player=False):
        self.x, self.y, self.car_type, self.spec, self.is_player = x, y, car_type, CAR_SPECS[car_type], is_player
        self.width = int(CAR_WIDTH * self.spec.size_multiplier)
        self.height = int(CAR_HEIGHT * self.spec.size_multiplier)
        self.velocity_x = 0; self.velocity_y = 0
        self.max_speed = 8 * self.spec.speed_multiplier
        self.acceleration = 0.3; self.friction = 0.85
        self.angle = 0; self.shadow_offset = 3
        self.ai_target_lane = 0; self.ai_change_timer = 0
    def draw_realistic_car(self, screen):
        shadow_surface = pygame.Surface((self.width+6, self.height+6), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, COLORS['SHADOW'], (0,0,self.width+6,self.height+6))
        screen.blit(shadow_surface, (self.x-3, self.y+self.shadow_offset))
        car_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.is_player:
            pygame.draw.rect(screen, (0,255,80), car_rect, border_radius=8)
        else:
            pygame.draw.rect(screen, self.spec.color, car_rect, border_radius=8)
        roof_height = self.height//3; roof_y = self.y+self.height//4
        roof_rect = pygame.Rect(self.x+8, roof_y, self.width-16, roof_height)
        pygame.draw.rect(screen, self.spec.secondary_color, roof_rect, border_radius=6)
        windshield_rect = pygame.Rect(self.x+6, self.y+5, self.width-12, 15)
        pygame.draw.rect(screen, COLORS['LIGHT_GRAY'], windshield_rect, border_radius=3)
        rear_window_rect = pygame.Rect(self.x+6, self.y+self.height-20, self.width-12, 15)
        pygame.draw.rect(screen, COLORS['LIGHT_GRAY'], rear_window_rect, border_radius=3)
        left_window = pygame.Rect(self.x+2, roof_y+3, 8, roof_height-6)
        right_window = pygame.Rect(self.x+self.width-10, roof_y+3, 8, roof_height-6)
        pygame.draw.rect(screen, COLORS['LIGHT_GRAY'], left_window, border_radius=2)
        pygame.draw.rect(screen, COLORS['LIGHT_GRAY'], right_window, border_radius=2)
        if not self.is_player:
            pygame.draw.rect(screen, COLORS['WHITE'], pygame.Rect(self.x+8, self.y+2, 8, 6), border_radius=2)
            pygame.draw.rect(screen, COLORS['WHITE'], pygame.Rect(self.x+self.width-16, self.y+2, 8, 6), border_radius=2)
        else:
            pygame.draw.rect(screen, COLORS['RED'], pygame.Rect(self.x+8, self.y+self.height-8, 8, 6), border_radius=2)
            pygame.draw.rect(screen, COLORS['RED'], pygame.Rect(self.x+self.width-16, self.y+self.height-8, 8, 6), border_radius=2)
        wheel_color = COLORS['BLACK']; wheel_size = 8
        pygame.draw.circle(screen, wheel_color, (self.x+12, self.y+15), wheel_size)
        pygame.draw.circle(screen, wheel_color, (self.x+self.width-12, self.y+15), wheel_size)
        pygame.draw.circle(screen, wheel_color, (self.x+12, self.y+self.height-15), wheel_size)
        pygame.draw.circle(screen, wheel_color, (self.x+self.width-12, self.y+self.height-15), wheel_size)
        rim_color = COLORS['LIGHT_GRAY']; rim_size = 4
        for pos in [(self.x+12, self.y+15), (self.x+self.width-12, self.y+15), (self.x+12, self.y+self.height-15), (self.x+self.width-12, self.y+self.height-15)]:
            pygame.draw.circle(screen, rim_color, pos, rim_size)
        if self.car_type == CarType.POLICE:
            pygame.draw.rect(screen, COLORS['BLUE'], pygame.Rect(self.x+4, self.y+self.height//2-3, self.width-8, 6))
        elif self.car_type == CarType.SPORTS:
            stripe_width = 4; stripe_x = self.x+self.width//2-stripe_width//2
            pygame.draw.rect(screen, COLORS['WHITE'], pygame.Rect(stripe_x, self.y+10, stripe_width, self.height-20))
    def update_physics(self):
        friction_x = 0.96 if self.is_player else self.friction
        friction_y = 0.97 if self.is_player else self.friction
        self.velocity_x *= friction_x; self.velocity_y *= friction_y
        if self.is_player:
            if abs(self.velocity_x)<0.08: self.velocity_x=0
            if abs(self.velocity_y)<0.08: self.velocity_y=0
            steer_ease=0.22; self.angle+=steer_ease*self.velocity_x; self.angle*=0.80
        self.x+=self.velocity_x; self.y+=self.velocity_y
        if self.is_player:
            road_left=SCREEN_WIDTH//2-ROAD_WIDTH//2; road_right=SCREEN_WIDTH//2+ROAD_WIDTH//2
            if self.x<road_left: self.x=road_left; self.velocity_x=0
            elif self.x+self.width>road_right: self.x=road_right-self.width; self.velocity_x=0
    def update_ai(self, game_speed):
        if self.is_player: return
        self.y+=game_speed*self.spec.speed_multiplier
        self.ai_change_timer+=1
        if self.ai_change_timer>random.randint(120,300):
            self.ai_change_timer=0
            road_left=SCREEN_WIDTH//2-ROAD_WIDTH//2
            lanes=[road_left+LANE_WIDTH*0.5-self.width//2, road_left+LANE_WIDTH*1.5-self.width//2, road_left+LANE_WIDTH*2.5-self.width//2]
            self.ai_target_lane=random.choice(lanes)
        if hasattr(self,'ai_target_lane'):
            lane_diff=self.ai_target_lane-self.x
            if abs(lane_diff)>2: self.velocity_x+=0.1*(1 if lane_diff>0 else -1)
    def get_rect(self): return pygame.Rect(self.x, self.y, self.width, self.height)
class Game:
    def __init__(self):
        self.screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("Car Racing Game")
        self.clock=pygame.time.Clock()
        self.background_image=pygame.image.load("background_demo.png").convert()
        self.background_image=pygame.transform.scale(self.background_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
        self.state=GameState.MENU; self.running=True
        self.particle_system=ParticleSystem()
        self.score=0; self.high_score=self.load_high_score(); self.level=1; self.cars_passed=0
        self.player=Car(SCREEN_WIDTH//2-CAR_WIDTH//2,SCREEN_HEIGHT-150,CarType.SPORTS,True)
        self.enemies=[]; self.enemy_spawn_timer=0; self.enemy_spawn_delay=90
        self.game_speed=4.0; self.speed_increase_timer=0; self.road_offset=0
        self.screen_shake=0; self.collision_flash=0
        self.font_large=pygame.font.Font(None,48); self.font_medium=pygame.font.Font(None,36); self.font_small=pygame.font.Font(None,24)
        self.keys_pressed=set()
    def load_high_score(self):
        try:
            if os.path.exists('high_score.json'):
                with open('high_score.json','r') as f:
                    data=json.load(f); return data.get('high_score',0)
        except: pass
        return 0
    def save_high_score(self):
        try:
            with open('high_score.json','w') as f:
                json.dump({'high_score':self.high_score},f)
        except: pass
    def spawn_enemy_car(self):
        car_types=list(CarType) if self.level>=5 else ([CarType.SEDAN,CarType.SPORTS,CarType.POLICE] if self.level>=3 else [CarType.SEDAN,CarType.SPORTS])
        car_type=random.choice(car_types)
        road_left=SCREEN_WIDTH//2-ROAD_WIDTH//2
        lanes=[road_left+LANE_WIDTH*0.5-CAR_WIDTH//2,road_left+LANE_WIDTH*1.5-CAR_WIDTH//2,road_left+LANE_WIDTH*2.5-CAR_WIDTH//2]
        available_lanes=[lane_x for lane_x in lanes if not any(abs(enemy.x-lane_x)<CAR_WIDTH and enemy.y>-CAR_HEIGHT*2 for enemy in self.enemies)]
        if not available_lanes: available_lanes=lanes
        x=random.choice(available_lanes)
        self.enemies.append(Car(x,-CAR_HEIGHT,car_type))
    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: self.running=False
            elif event.type==pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                if self.state==GameState.MENU:
                    if event.key==pygame.K_SPACE: self.start_game()
                    elif event.key==pygame.K_ESCAPE: self.running=False
                elif self.state==GameState.PLAYING:
                    if event.key==pygame.K_ESCAPE: self.state=GameState.PAUSED
                elif self.state==GameState.PAUSED:
                    if event.key==pygame.K_ESCAPE: self.state=GameState.PLAYING
                    elif event.key==pygame.K_r: self.start_game()
                elif self.state==GameState.GAME_OVER:
                    if event.key==pygame.K_r: self.start_game()
                    elif event.key==pygame.K_ESCAPE: self.state=GameState.MENU
            elif event.type==pygame.KEYUP: self.keys_pressed.discard(event.key)
    def handle_input(self):
        if self.state!=GameState.PLAYING: return
        steer_accel=self.player.acceleration*1.2; speed_accel=self.player.acceleration*1.0; brake_accel=self.player.acceleration*1.8
        if pygame.K_LEFT in self.keys_pressed or pygame.K_a in self.keys_pressed:
            if self.player.velocity_x>0: self.player.velocity_x-=steer_accel*1.5
            self.player.velocity_x-=steer_accel
        if pygame.K_RIGHT in self.keys_pressed or pygame.K_d in self.keys_pressed:
            if self.player.velocity_x<0: self.player.velocity_x+=steer_accel*1.5
            self.player.velocity_x+=steer_accel
        if pygame.K_UP in self.keys_pressed or pygame.K_w in self.keys_pressed:
            if self.player.velocity_y>-self.player.max_speed*0.4: self.player.velocity_y-=speed_accel
        if pygame.K_DOWN in self.keys_pressed or pygame.K_s in self.keys_pressed:
            if self.player.velocity_y<self.player.max_speed*0.4: self.player.velocity_y+=brake_accel
        max_vel=self.player.max_speed*1.0
        self.player.velocity_x=max(-max_vel,min(max_vel,self.player.velocity_x))
        self.player.velocity_y=max(-max_vel*0.7,min(max_vel*0.7,self.player.velocity_y))
    def update_game(self):
        if self.state!=GameState.PLAYING: return
        self.player.update_physics()
        for enemy in self.enemies[:]:
            enemy.update_ai(self.game_speed)
            if enemy.y>SCREEN_HEIGHT+50:
                self.enemies.remove(enemy); self.cars_passed+=1; self.score+=10
                if self.score>self.high_score: self.high_score=self.score
        self.enemy_spawn_timer+=1
        if self.enemy_spawn_timer>=self.enemy_spawn_delay:
            self.spawn_enemy_car(); self.enemy_spawn_timer=0
        player_rect=self.player.get_rect()
        for enemy in self.enemies:
            if player_rect.colliderect(enemy.get_rect()):
                self.handle_collision(enemy); break
        self.update_difficulty(); self.update_effects(); self.particle_system.update()
        self.road_offset+=self.game_speed
        if self.road_offset>=60: self.road_offset=0
    def handle_collision(self, enemy_car):
        self.particle_system.add_explosion((self.player.x+enemy_car.x)//2+CAR_WIDTH//2,(self.player.y+enemy_car.y)//2+CAR_HEIGHT//2,30)
        self.screen_shake=20; self.collision_flash=30; self.state=GameState.GAME_OVER; self.save_high_score()
    def update_difficulty(self):
        self.speed_increase_timer+=1
        if self.speed_increase_timer>=600:
            self.game_speed+=0.2; self.speed_increase_timer=0
            if self.enemy_spawn_delay>30: self.enemy_spawn_delay=max(30,self.enemy_spawn_delay-2)
        new_level=(self.cars_passed//10)+1
        if new_level>self.level: self.level=new_level
    def update_effects(self):
        if self.screen_shake>0: self.screen_shake-=1
        if self.collision_flash>0: self.collision_flash-=1
        if random.randint(1,60)==1:
            smoke_x=self.player.x+self.player.width//2; smoke_y=self.player.y+self.player.height
            self.particle_system.add_smoke(smoke_x,smoke_y,2)
    def start_game(self):
        self.state=GameState.PLAYING; self.score=0; self.level=1; self.cars_passed=0; self.game_speed=4.0; self.enemy_spawn_delay=90; self.speed_increase_timer=0
        self.player=Car(SCREEN_WIDTH//2-CAR_WIDTH//2,SCREEN_HEIGHT-150,CarType.SPORTS,True)
        self.enemies.clear(); self.screen_shake=0; self.collision_flash=0; self.particle_system.particles.clear()
    def draw_background(self): self.screen.blit(self.background_image,(0,0))
    def draw_road(self):
        road_left=SCREEN_WIDTH//2-ROAD_WIDTH//2; road_right=SCREEN_WIDTH//2+ROAD_WIDTH//2
        pygame.draw.rect(self.screen,COLORS['ROAD_GRAY'],pygame.Rect(road_left,0,ROAD_WIDTH,SCREEN_HEIGHT))
        pygame.draw.rect(self.screen,COLORS['WHITE'],(road_left-8,0,8,SCREEN_HEIGHT))
        pygame.draw.rect(self.screen,COLORS['WHITE'],(road_right,0,8,SCREEN_HEIGHT))
        lane1_x=road_left+LANE_WIDTH-2; lane2_x=road_left+2*LANE_WIDTH-2
        dash_length=30; dash_gap=30
        for y in range(-dash_length,SCREEN_HEIGHT+dash_length,dash_length+dash_gap):
            dash_y=y+self.road_offset
            if -dash_length<=dash_y<=SCREEN_HEIGHT:
                pygame.draw.rect(self.screen,COLORS['WHITE'],(lane1_x,dash_y,4,dash_length))
                pygame.draw.rect(self.screen,COLORS['WHITE'],(lane2_x,dash_y,4,dash_length))
    def draw_ui(self):
        ui_bg=pygame.Surface((300,120),pygame.SRCALPHA); ui_bg.fill((0,0,0,128)); self.screen.blit(ui_bg,(10,10))
        score_text=self.font_medium.render(f"Score: {self.score:,}",True,COLORS['WHITE'])
        high_score_text=self.font_small.render(f"High Score: {self.high_score:,}",True,COLORS['YELLOW'])
        level_text=self.font_small.render(f"Level: {self.level}",True,COLORS['GREEN'])
        speed_text=self.font_small.render(f"Speed: {self.game_speed:.1f}",True,COLORS['BLUE'])
        cars_text=self.font_small.render(f"Cars Passed: {self.cars_passed}",True,COLORS['WHITE'])
        self.screen.blit(score_text,(20,20)); self.screen.blit(high_score_text,(20,50)); self.screen.blit(level_text,(20,75)); self.screen.blit(speed_text,(150,75)); self.screen.blit(cars_text,(20,100))
        if self.score<50:
            controls_bg=pygame.Surface((250,60),pygame.SRCALPHA); controls_bg.fill((0,0,0,128)); self.screen.blit(controls_bg,(SCREEN_WIDTH-260,SCREEN_HEIGHT-70))
            controls_text=["WASD/Arrows: Move","Space: Horn","ESC: Pause"]
            for i,text in enumerate(controls_text):
                rendered=self.font_small.render(text,True,COLORS['WHITE'])
                self.screen.blit(rendered,(SCREEN_WIDTH-250,SCREEN_HEIGHT-60+i*20))
    def draw_menu(self):
        title_text=self.font_large.render("CAR RACING GAME",True,COLORS['WHITE'])
        title_rect=title_text.get_rect(center=(SCREEN_WIDTH//2,150))
        title_shadow=self.font_large.render("CAR RACING GAME",True,COLORS['BLACK'])
        shadow_rect=title_shadow.get_rect(center=(SCREEN_WIDTH//2+3,153))
        self.screen.blit(title_shadow,shadow_rect); self.screen.blit(title_text,title_rect)
        subtitle_text=self.font_medium.render("Professional Edition",True,COLORS['YELLOW'])
        subtitle_rect=subtitle_text.get_rect(center=(SCREEN_WIDTH//2,200)); self.screen.blit(subtitle_text,subtitle_rect)
        instructions=["Press SPACE to Start","Use WASD or Arrow Keys to move","Avoid other cars and survive as long as possible!","Press ESC to quit"]
        for i,instruction in enumerate(instructions):
            text=self.font_small.render(instruction,True,COLORS['WHITE'])
            text_rect=text.get_rect(center=(SCREEN_WIDTH//2,300+i*30))
            self.screen.blit(text,text_rect)
        if self.high_score>0:
            high_score_text=self.font_medium.render(f"High Score: {self.high_score:,}",True,COLORS['GREEN'])
            high_score_rect=high_score_text.get_rect(center=(SCREEN_WIDTH//2,450))
            self.screen.blit(high_score_text,high_score_rect)
    def draw_game_over(self):
        overlay=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA); overlay.fill((0,0,0,180)); self.screen.blit(overlay,(0,0))
        game_over_text=self.font_large.render("GAME OVER",True,COLORS['RED'])
        game_over_rect=game_over_text.get_rect(center=(SCREEN_WIDTH//2,200)); self.screen.blit(game_over_text,game_over_rect)
        stats=[f"Final Score: {self.score:,}",f"Level Reached: {self.level}",f"Cars Passed: {self.cars_passed}",f"High Score: {self.high_score:,}"]
        for i,stat in enumerate(stats):
            color=COLORS['YELLOW'] if "High Score" in stat else COLORS['WHITE']
            text=self.font_medium.render(stat,True,color)
            text_rect=text.get_rect(center=(SCREEN_WIDTH//2,280+i*40))
            self.screen.blit(text,text_rect)
        if self.score==self.high_score and self.score>0:
            new_high_text=self.font_medium.render("NEW HIGH SCORE!",True,COLORS['YELLOW'])
            new_high_rect=new_high_text.get_rect(center=(SCREEN_WIDTH//2,450))
            if (pygame.time.get_ticks()//500)%2: self.screen.blit(new_high_text,new_high_rect)
        restart_text=self.font_small.render("Press R to Restart or ESC for Menu",True,COLORS['WHITE'])
        restart_rect=restart_text.get_rect(center=(SCREEN_WIDTH//2,500)); self.screen.blit(restart_text,restart_rect)
    def draw_paused(self):
        overlay=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA); overlay.fill((0,0,0,128)); self.screen.blit(overlay,(0,0))
        paused_text=self.font_large.render("PAUSED",True,COLORS['WHITE'])
        paused_rect=paused_text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)); self.screen.blit(paused_text,paused_rect)
        resume_text=self.font_small.render("Press ESC to Resume or R to Restart",True,COLORS['WHITE'])
        resume_rect=resume_text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2+50)); self.screen.blit(resume_text,resume_rect)
    def draw(self):
        shake_x=shake_y=0
        if self.screen_shake>0: shake_x=random.randint(-self.screen_shake,self.screen_shake); shake_y=random.randint(-self.screen_shake,self.screen_shake)
        self.draw_background()
        if self.state in [GameState.PLAYING,GameState.PAUSED,GameState.GAME_OVER]:
            self.draw_road()
            temp_surface=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
            self.player.draw_realistic_car(temp_surface)
            for enemy in self.enemies: enemy.draw_realistic_car(temp_surface)
            self.particle_system.draw(temp_surface)
            self.screen.blit(temp_surface,(shake_x,shake_y))
            self.draw_ui()
            if self.collision_flash>0:
                flash_surface=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
                alpha=int(255*(self.collision_flash/30))
                flash_surface.fill((255,255,255,alpha))
                self.screen.blit(flash_surface,(0,0))
        if self.state==GameState.MENU: self.draw_menu()
        elif self.state==GameState.PAUSED: self.draw_paused()
        elif self.state==GameState.GAME_OVER: self.draw_game_over()
        pygame.display.flip()
    def run(self):
        while self.running:
            self.handle_events(); self.handle_input(); self.update_game(); self.draw(); self.clock.tick(FPS)
        pygame.quit()

def carRacingGame():
    pygame.init()
    game = Game()
    st.title("Car Racing Game")
    start = st.button("Start Game")
    if start:
        running = True
        while running:
            game.handle_events(); game.handle_input(); game.update_game(); game.draw()
            st_pygame(game.screen)
            if st.button("Quit"): running = False
        pygame.quit()

if __name__ == "__main__":
    if st is not None and st_pygame is not None:
        carRacingGame()
    else:
        pygame.init(); Game().run()
