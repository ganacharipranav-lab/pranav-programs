import pygame
import random
import heapq

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 15, 15
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Maze Solver - A* Search")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Create maze
maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Random walls
for r in range(ROWS):
    for c in range(COLS):
        if random.random() < 0.25:
            maze[r][c] = 1

start = (0, 0)
goal = (ROWS - 1, COLS - 1)

maze[start[0]][start[1]] = 0
maze[goal[0]][goal[1]] = 0

visited_nodes = []
path_nodes = []

# Manhattan heuristic
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* Algorithm
def astar():
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}

    visited_nodes.clear()

    while open_set:
        current = heapq.heappop(open_set)[1]

        visited_nodes.append(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        r, c = current

        neighbors = [
            (r + 1, c),
            (r - 1, c),
            (r, c + 1),
            (r, c - 1)
        ]

        for nr, nc in neighbors:
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if maze[nr][nc] == 1:
                    continue

                tentative_g = g_score[current] + 1

                if (nr, nc) not in g_score or tentative_g < g_score[(nr, nc)]:

                    came_from[(nr, nc)] = current
                    g_score[(nr, nc)] = tentative_g

                    f = tentative_g + heuristic((nr, nc), goal)

                    heapq.heappush(open_set, (f, (nr, nc)))

    return []

# Player
player = list(start)

font = pygame.font.SysFont(None, 30)

running = True

while running:

    screen.fill(WHITE)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # AI Solve
            if event.key == pygame.K_SPACE:
                path_nodes = astar()

    keys = pygame.key.get_pressed()

    # Manual play
    if keys[pygame.K_UP]:
        nr, nc = player[0] - 1, player[1]
        if nr >= 0 and maze[nr][nc] == 0:
            player[0] = nr

    if keys[pygame.K_DOWN]:
        nr, nc = player[0] + 1, player[1]
        if nr < ROWS and maze[nr][nc] == 0:
            player[0] = nr

    if keys[pygame.K_LEFT]:
        nr, nc = player[0], player[1] - 1
        if nc >= 0 and maze[nr][nc] == 0:
            player[1] = nc

    if keys[pygame.K_RIGHT]:
        nr, nc = player[0], player[1] + 1
        if nc < COLS and maze[nr][nc] == 0:
            player[1] = nc

    # Draw maze
    for r in range(ROWS):
        for c in range(COLS):

            color = WHITE

            if maze[r][c] == 1:
                color = BLACK

            pygame.draw.rect(
                screen,
                color,
                (c * CELL_SIZE, r * CELL_SIZE,
                 CELL_SIZE, CELL_SIZE)
            )

            pygame.draw.rect(
                screen,
                (200, 200, 200),
                (c * CELL_SIZE, r * CELL_SIZE,
                 CELL_SIZE, CELL_SIZE),
                1
            )

    # Draw visited nodes
    for node in visited_nodes:
        r, c = node
        pygame.draw.rect(
            screen,
            YELLOW,
            (c * CELL_SIZE, r * CELL_SIZE,
             CELL_SIZE, CELL_SIZE)
        )

    # Draw final path
    for node in path_nodes:
        r, c = node
        pygame.draw.rect(
            screen,
            BLUE,
            (c * CELL_SIZE, r * CELL_SIZE,
             CELL_SIZE, CELL_SIZE)
        )

    # Goal
    pygame.draw.rect(
        screen,
        RED,
        (goal[1] * CELL_SIZE,
         goal[0] * CELL_SIZE,
         CELL_SIZE,
         CELL_SIZE)
    )

    # Player
    pygame.draw.rect(
        screen,
        GREEN,
        (player[1] * CELL_SIZE,
         player[0] * CELL_SIZE,
         CELL_SIZE,
         CELL_SIZE)
    )

    text = font.render(
        "Arrow Keys: Play  |  SPACE: AI Solve",
        True,
        BLACK
    )

    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
