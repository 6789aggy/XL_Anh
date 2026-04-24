import pygame
import cv2
import random
import os
import math
import mediapipe as mp
from src.hand_tracking import HandTracker
from src.utils import load_questions, open_add_question_ui, save_score, get_top_history

# --- KHỞI TẠO ---
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bird Shooting Game - Professional Layout")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Arial", 26, bold=True)
font_msg = pygame.font.SysFont("Arial", 50, bold=True)
font_rank = pygame.font.SysFont("Consolas", 18, bold=True)

# --- ÂM THANH ---
music_on, sfx_on = True, True
snd_shoot = snd_correct = snd_reload = snd_winner = snd_gameover = None
def load_game_sounds():
    global snd_shoot, snd_correct, snd_reload, snd_winner, snd_gameover
    try:
        if os.path.exists("assets/sounds/bg_music.mp3"):
            pygame.mixer.music.load("assets/sounds/bg_music.mp3")
            pygame.mixer.music.set_volume(0.3)
        if os.path.exists("assets/sounds/shoot.wav"): snd_shoot = pygame.mixer.Sound("assets/sounds/shoot.wav")
        if os.path.exists("assets/sounds/correct.wav"): snd_correct = pygame.mixer.Sound("assets/sounds/correct.wav")
        if os.path.exists("assets/sounds/reload.wav"): snd_reload = pygame.mixer.Sound("assets/sounds/reload.wav")
        if os.path.exists("assets/sounds/winner.wav"): snd_winner = pygame.mixer.Sound("assets/sounds/winner.wav")
        if os.path.exists("assets/sounds/gameover.wav"): snd_gameover = pygame.mixer.Sound("assets/sounds/gameover.wav")
    except: pass
load_game_sounds()

# Biến Game
ai_assist, ready_to_shoot = False, True 
max_ammo, ammo, lives = 5, 5, 3
player_name = ""; active_input = False

# Hình ảnh
try:
    bg_img = pygame.image.load("assets/images/background.png").convert()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    bird_orig = pygame.image.load("assets/images/bird_sprite.png").convert_alpha()
    bird_img_r = pygame.transform.scale(bird_orig, (100, 80))
    bird_img_l = pygame.transform.flip(bird_img_r, True, False)
except:
    bg_img = pygame.Surface((WIDTH, HEIGHT)); bg_img.fill((100, 200, 255))
    bird_img_r = bird_img_l = pygame.Surface((100, 80))

cap = cv2.VideoCapture(1)
tracker = HandTracker(); mp_draw = mp.solutions.drawing_utils
MENU, PLAYING, PAUSED, RESULT, GAMEOVER = 0, 1, 2, 3, 4
game_state = MENU

class Bird:
    def __init__(self, pool):
        self.pool = pool
        self.side = random.choice(["left", "right"])
        self.current_correct_ans = None
        self.reset_pos()
    
    def reset_pos(self, current_correct=None):
        if current_correct: self.current_correct_ans = current_correct
        self.text = self.current_correct_ans if (self.current_correct_ans and random.random() < 0.6) else random.choice(self.pool)
        self.x = -200 if self.side == "left" else WIDTH + 200
        self.speed_x = random.randint(5, 9) if self.side == "left" else random.randint(-9, -5)
        self.y = random.randint(150, HEIGHT - 150)
        self.speed_y = random.uniform(-1, 1)
        self.rect = bird_img_r.get_rect(center=(self.x, self.y))
    
    def move(self):
        self.x += self.speed_x; self.y += self.speed_y
        if self.y < 150 or self.y > HEIGHT - 100: self.speed_y *= -1
        self.rect.center = (self.x, self.y)
        if self.x > WIDTH + 400 or self.x < -400: self.reset_pos()

    def draw(self, surface, is_target=False):
        if ai_assist and is_target: pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), 65, 5)
        surface.blit(bird_img_r if self.speed_x > 0 else bird_img_l, self.rect)
        ans_txt = font_small.render(str(self.text), True, (0, 0, 0))
        box = pygame.Rect(0, 0, ans_txt.get_width() + 14, ans_txt.get_height() + 6)
        box.center = (self.x, self.y + 45)
        pygame.draw.rect(surface, (255, 255, 255), box, border_radius=8)
        surface.blit(ans_txt, ans_txt.get_rect(center=box.center))

def draw_button(text, x, y, w, h, color):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, border_radius=15)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=15)
    txt = font_small.render(text, True, (255, 255, 255))
    screen.blit(txt, (x + (w - txt.get_width())//2, y + (h - txt.get_height())//2))
    return rect

def draw_history_table():
    """Vẽ bảng Ranking ngoài Menu với cột ACC ngoài cùng bên phải"""
    table_rect = pygame.Rect(WIDTH - 450, 50, 420, 380)
    pygame.draw.rect(screen, (255, 255, 255, 220), table_rect, border_radius=20)
    pygame.draw.rect(screen, (44, 62, 80), table_rect, 3, border_radius=20)
    title = font_small.render("TOP RANKING", True, (44, 62, 80))
    screen.blit(title, (table_rect.centerx - title.get_width()//2, table_rect.y + 15))
    
    # Header
    h_y = table_rect.y + 60
    screen.blit(font_rank.render("NAME", True, (127, 140, 141)), (table_rect.x + 20, h_y))
    screen.blit(font_rank.render("SCORE", True, (127, 140, 141)), (table_rect.x + 210, h_y))
    screen.blit(font_rank.render("ACC", True, (127, 140, 141)), (table_rect.x + 325, h_y)) # Cột ngoài cùng

    top = get_top_history(6)
    for i, p in enumerate(top):
        y = table_rect.y + 100 + (i * 45)
        clr = (241, 196, 15) if i == 0 else (44, 62, 80)
        screen.blit(font_rank.render(f"{i+1}.{str(p['name'])[:10]}", True, clr), (table_rect.x + 15, y))
        screen.blit(font_rank.render(str(p['score']), True, (39, 174, 96)), (table_rect.x + 210, y))
        screen.blit(font_rank.render(p.get('accuracy','0/0'), True, (52, 152, 219)), (table_rect.x + 325, y))

def main():
    global game_state, music_on, sfx_on, ai_assist, ready_to_shoot, ammo, lives, player_name, active_input
    all_q, birds, score, q_idx, correct_shots = [], [], 0, 0, 0
    running = True
    btn_start = btn_add = btn_pause = btn_res = btn_mus = btn_sfx = btn_exit = btn_retry = name_rect = btn_help = pygame.Rect(0,0,0,0)

    while running:
        success, frame = cap.read()
        cursor_pos, is_firing, is_rock = None, False, False
        cam_surf = None
        if success:
            res = tracker.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if res.multi_hand_landmarks:
                for hand_lms in res.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_lms, mp.solutions.hands.HAND_CONNECTIONS)
                    thumb, idx, mid, ring, pinky = [hand_lms.landmark[i] for i in [4, 8, 12, 16, 20]]
                    cursor_pos = (int((1 - idx.x) * WIDTH), int(idx.y * HEIGHT))
                    if idx.y < hand_lms.landmark[6].y and pinky.y < hand_lms.landmark[18].y and mid.y > hand_lms.landmark[10].y and ring.y > hand_lms.landmark[14].y: is_rock = True
                    elif math.hypot(idx.x - thumb.x, idx.y - thumb.y) < 0.04: is_firing = True
            small_f = cv2.resize(cv2.flip(frame, 1), (240, 180))
            cam_surf = pygame.image.frombuffer(small_f.tobytes(), small_f.shape[1::-1], "BGR")

        if is_rock and game_state == PLAYING and ammo < max_ammo:
            ammo = max_ammo
            if sfx_on and snd_reload: snd_reload.play()

        shoot_now = (is_firing and ready_to_shoot)
        ready_to_shoot = not is_firing

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if game_state == MENU and event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_BACKSPACE: player_name = player_name[:-1]
                elif len(player_name) < 15: player_name += event.unicode
            if event.type == pygame.KEYDOWN and event.key == pygame.K_h: ai_assist = not ai_assist
            if event.type == pygame.MOUSEBUTTONDOWN:
                m = pygame.mouse.get_pos()
                if game_state == MENU:
                    active_input = name_rect.collidepoint(m)
                    if btn_start.collidepoint(m):
                        all_q = load_questions()
                        if all_q:
                            player_name = player_name.strip() if player_name.strip() else "Player 1"
                            random.shuffle(all_q); score, q_idx, ammo, lives, correct_shots = 0, 0, 5, 3, 0
                            birds = [Bird([opt for q in all_q for opt in q['options']]) for _ in range(8)]
                            for b in birds: b.current_correct_ans = all_q[0]['correct']
                            game_state = PLAYING
                            if music_on: pygame.mixer.music.play(-1)
                    elif btn_add.collidepoint(m): open_add_question_ui()
                elif game_state == PLAYING:
                    if btn_pause.collidepoint(m): game_state = PAUSED
                    elif btn_help.collidepoint(m): ai_assist = not ai_assist
                elif game_state == PAUSED:
                    if btn_res.collidepoint(m): game_state = PLAYING
                    elif btn_mus.collidepoint(m): 
                        music_on = not music_on
                        if music_on: pygame.mixer.music.play(-1)
                        else: pygame.mixer.music.stop()
                    elif btn_sfx.collidepoint(m): sfx_on = not sfx_on
                    elif btn_exit.collidepoint(m): game_state = MENU
                elif game_state in [RESULT, GAMEOVER] and btn_retry.collidepoint(m): game_state = MENU

        if shoot_now and game_state == PLAYING and cursor_pos:
            if ammo > 0:
                ammo -= 1; curr_q = all_q[q_idx]
                if sfx_on and snd_shoot: snd_shoot.play()
                hit = next((b for b in birds if b.rect.collidepoint(cursor_pos)), None)
                if hit:
                    if str(hit.text) == str(curr_q['correct']):
                        if sfx_on and snd_correct: snd_correct.play()
                        score += 10; correct_shots += 1; q_idx += 1
                        if q_idx >= len(all_q):
                            pygame.mixer.music.stop()
                            if sfx_on and snd_winner: snd_winner.play()
                            save_score(player_name, score, correct_shots, len(all_q))
                            game_state = RESULT
                        else:
                            for b in birds: b.current_correct_ans = all_q[q_idx]['correct']
                    else: lives -= 1
                    hit.reset_pos()
                else: lives -= 1
                if lives <= 0:
                    pygame.mixer.music.stop()
                    if sfx_on and snd_gameover: snd_gameover.play()
                    save_score(player_name, score, correct_shots, len(all_q))
                    game_state = GAMEOVER

        screen.blit(bg_img, (0, 0))
        if cam_surf: screen.blit(cam_surf, (WIDTH - 250, HEIGHT - 190))
        if game_state == MENU:
            pygame.draw.rect(screen, (255,255,255, 180), (100, 50, 450, 550), border_radius=25)
            screen.blit(font_small.render("ENTER NAME:", True, (44, 62, 80)), (150, 100))
            name_rect = pygame.Rect(150, 140, 350, 45)
            pygame.draw.rect(screen, (255,255,255), name_rect, border_radius=5)
            pygame.draw.rect(screen, (46,204,113) if active_input else (127,140,141), name_rect, 2, border_radius=5)
            screen.blit(font_small.render(player_name, True, (0,0,0)), (160, 145))
            btn_start = draw_button("START GAME", 150, 220, 350, 75, (46, 204, 113))
            btn_add = draw_button("SETTINGS / HISTORY", 150, 320, 350, 75, (52, 152, 219))
            draw_history_table()
        elif game_state == PLAYING:
            screen.blit(font_small.render(f"AMMO: {ammo}/5", True, (255,255,255)), (50, 60))
            for i in range(lives): pygame.draw.circle(screen, (255,0,0), (60 + i*35, 120), 12)
            curr_q = all_q[q_idx]
            q_str = f"SHOOT: {curr_q['question']}"
            if ai_assist: q_str += f" {curr_q['correct']}"
            pygame.draw.rect(screen, (255,255,255), (WIDTH//4, 20, WIDTH//2, 80), border_radius=15)
            q_txt = font_small.render(q_str, True, (0,0,0))
            screen.blit(q_txt, (WIDTH//2-q_txt.get_width()//2, 40))
            for b in birds: b.move(); b.draw(screen, (str(b.text)==str(curr_q['correct'])))
            btn_help = draw_button(f"Help: {'ON' if ai_assist else 'OFF'}", 20, HEIGHT - 70, 150, 50, (46, 204, 113) if ai_assist else (100,100,100))
            btn_pause = draw_button("|| STOP", WIDTH-160, 20, 140, 50, (231, 76, 60))
        elif game_state == PAUSED:
            pygame.draw.rect(screen, (255,255,255), (WIDTH//3, 100, WIDTH//3, 520), border_radius=20)
            btn_res = draw_button("RESUME", WIDTH//2-100, 150, 200, 60, (46, 204, 113))
            btn_mus = draw_button(f"MUSIC: {'ON' if music_on else 'OFF'}", WIDTH//2-100, 250, 200, 60, (52, 152, 219))
            btn_sfx = draw_button(f"SFX: {'ON' if sfx_on else 'OFF'}", WIDTH//2-100, 350, 200, 60, (52, 152, 219))
            btn_exit = draw_button("EXIT", WIDTH//2-100, 480, 200, 60, (231, 76, 60))
        elif game_state in [RESULT, GAMEOVER]:
            pygame.draw.rect(screen, (255,255,255), (WIDTH//4, 150, WIDTH//2, 400), border_radius=25)
            res_txt = font_msg.render("VICTORY!" if game_state == RESULT else "GAME OVER", True, (39,174,96) if game_state == RESULT else (231,76,60))
            screen.blit(res_txt, (WIDTH//2-res_txt.get_width()//2, 220))
            btn_retry = draw_button("BACK TO MENU", WIDTH//2-130, 420, 260, 60, (243, 156, 18))

        if cursor_pos and game_state == PLAYING:
            c = (46,204,113) if ammo>0 else (231,76,60)
            pygame.draw.circle(screen, c, cursor_pos, 22, 2)
            pygame.draw.line(screen, c, (cursor_pos[0]-30, cursor_pos[1]), (cursor_pos[0]+30, cursor_pos[1]), 2)
            pygame.draw.line(screen, c, (cursor_pos[0], cursor_pos[1]-30), (cursor_pos[0], cursor_pos[1]+30), 2)
        pygame.display.flip(); clock.tick(30)
    cap.release(); pygame.quit()

if __name__ == "__main__": main()