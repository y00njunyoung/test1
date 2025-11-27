import pygame
import sys

pygame.init()
pygame.display.set_caption("게임")

# -----------------------------
# 기본 설정
# -----------------------------
BASE_WIDTH, BASE_HEIGHT = 800, 600
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)

# -----------------------------
# 이미지 로드 함수
# -----------------------------
def load_img(path):
    return pygame.image.load(path).convert_alpha()

# 원본 이미지 로드
bg_main_original = load_img("images/main_background.png")
bg_desc_original = load_img("images/description_background.png")

btn_start_original = load_img("images/btn_start.png")
btn_desc_original = load_img("images/btn_description.png")
btn_exit_original = load_img("images/btn_exit.png")
btn_music_on_original = load_img("images/btn_music_on.png")
btn_music_off_original = load_img("images/btn_music_off.png")

# -----------------------------
# 버튼 기본 좌표 (원본 기준 800×600 좌표)
# -----------------------------
button_info = {
    "start": (516.0689, 517.1278, 222.0178, 68.3005),
    "desc": (514.9524, 429.992, 223.1342, 68.5918),
    "exit": (736.7423, 34.7654, 43.8002, 43.4385),
    "music": (680.0366, 34.7654, 43.8002, 43.4385),
}

# -----------------------------
# 스케일링 함수
# -----------------------------
def scale_img(img, w_ratio, h_ratio):
    return pygame.transform.smoothscale(
        img,
        (int(img.get_width() * w_ratio), int(img.get_height() * h_ratio))
    )

def get_scaled_button_rect(key, w_ratio, h_ratio):
    x, y, w, h = button_info[key]
    return pygame.Rect(int(x * w_ratio), int(y * h_ratio), int(w * w_ratio), int(h * h_ratio))

# -----------------------------
# 상태 변수
# -----------------------------
current_screen = "main"
music_on = True  # ← 기본은 On 버튼 상태

# -----------------------------
# 메인 루프
# -----------------------------
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 창 크기 변경 시 반응형
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # 클릭 이벤트
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            w_ratio = screen.get_width() / BASE_WIDTH
            h_ratio = screen.get_height() / BASE_HEIGHT

            if current_screen == "main":
                # 게임 시작 버튼
                if get_scaled_button_rect("start", w_ratio, h_ratio).collidepoint(mx, my):
                    print("게임 시작")

                # 설명 화면으로 이동
                if get_scaled_button_rect("desc", w_ratio, h_ratio).collidepoint(mx, my):
                    current_screen = "desc"

                # 게임 종료
                if get_scaled_button_rect("exit", w_ratio, h_ratio).collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

                # -----------------------------
                # 음악 on/off 토글
                # -----------------------------
                if get_scaled_button_rect("music", w_ratio, h_ratio).collidepoint(mx, my):
                    music_on = not music_on  # ← 상태 반전
                    if music_on:
                        print("Music: ON")
                        # pygame.mixer.music.play(-1)   ← 나중에 음악 넣을 때
                    else:
                        print("Music: OFF")
                        # pygame.mixer.music.stop()

            # 설명 화면 클릭 → 메인으로 복귀
            elif current_screen == "desc":
                current_screen = "main"

    # -----------------------------
    # 화면 그리기
    # -----------------------------
    w_ratio = screen.get_width() / BASE_WIDTH
    h_ratio = screen.get_height() / BASE_HEIGHT

    if current_screen == "main":
        # 배경
        screen.blit(scale_img(bg_main_original, w_ratio, h_ratio), (0, 0))

        # 버튼들
        screen.blit(scale_img(btn_start_original, w_ratio, h_ratio),
                    get_scaled_button_rect("start", w_ratio, h_ratio))
        screen.blit(scale_img(btn_desc_original, w_ratio, h_ratio),
                    get_scaled_button_rect("desc", w_ratio, h_ratio))
        screen.blit(scale_img(btn_exit_original, w_ratio, h_ratio),
                    get_scaled_button_rect("exit", w_ratio, h_ratio))

        # --------------------------------
        # 여기서 On/Off 버튼 이미지를 선택
        # --------------------------------
        if music_on:
            music_img = btn_music_on_original
        else:
            music_img = btn_music_off_original

        screen.blit(scale_img(music_img, w_ratio, h_ratio),
                    get_scaled_button_rect("music", w_ratio, h_ratio))

    else:
        # 설명 화면
        screen.blit(scale_img(bg_desc_original, w_ratio, h_ratio), (0, 0))

    pygame.display.update()
    clock.tick(60)
