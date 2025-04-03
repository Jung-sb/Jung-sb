import pygame
import random

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game")

# 색상 정의
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# 폰트 설정
font = pygame.font.Font(None, 36)

# 뱀 초기 설정
snake = [(100, 100), (90, 100), (80, 100)]  # 뱀의 몸통 좌표 리스트
direction = (CELL_SIZE, 0)  # 초기 이동 방향 (오른쪽)
score = 0  # 점수

# 먹이 생성 함수
def generate_food():
    return (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

food = generate_food()

# 게임 루프 설정
clock = pygame.time.Clock()
running = True
game_over = False  # 게임 오버 상태

# 게임 루프
while running:
    screen.fill(BLACK)  # 배경색 설정

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:  # 키보드 입력 처리
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

    if not game_over:
        # 뱀 이동
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        # 먹이 먹기
        if new_head == food:
            food = generate_food()  # 새로운 먹이 생성
            score += 10  # 점수 증가
        else:
            snake.pop()  # 꼬리 제거

        # 충돌 판정 (벽이나 자기 몸에 부딪히면 게임 오버)
        if (new_head[0] < 0 or new_head[0] >= WIDTH or 
            new_head[1] < 0 or new_head[1] >= HEIGHT or 
            new_head in snake[1:]):
            game_over = True

    # 뱀 & 먹이 그리기
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

    # 점수 표시
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # 게임 오버 화면
    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, BLUE)
        screen.blit(game_over_text, (WIDTH // 6, HEIGHT // 2))

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(10)  # 게임 속도 조절 (숫자를 높이면 속도 증가)

    # R 키를 누르면 게임 재시작
    keys = pygame.key.get_pressed()
    if game_over and keys[pygame.K_r]:
        snake = [(100, 100), (90, 100), (80, 100)]  # 뱀 초기화
        direction = (CELL_SIZE, 0)  # 이동 방향 초기화
        food = generate_food()  # 새로운 먹이 생성
        score = 0  # 점수 초기화
        game_over = False  # 게임 오버 해제

pygame.quit()
