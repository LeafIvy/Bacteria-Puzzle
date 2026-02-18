import pygame as pg

pg.init()
swidth = 800
sheight = 600
screen = pg.display.set_mode((swidth, sheight))
running = True


def draw_grid():
    for x in range(25, swidth, 50):
        pg.draw.line(screen, 'white', (x, 25), (x, sheight-25))
    for y in range(25, sheight, 50):
        pg.draw.line(screen, 'white', (25, y), (swidth-25, y))

    for x in range(25, 176, 50):
        pg.draw.line(screen, 'yellow', (x, sheight-150-25), (x, sheight - 25))
    for y in range(sheight-3*50-25, sheight-24, 50):
        pg.draw.line(screen, 'yellow', (25, y), (176, y))

class Germ:
    def __init__(self, screen, size, coords):
        self.screen = screen
        self.color = 'green'
        self.rect = pg.Rect(coords, size)
        self.reproduce = 1

    def draw(self):
        if self.reproduce: self.color = 'green'
        else: self.color = 'red'
        pg.draw.circle(screen, self.color, self.rect.center, self.rect.width//2)


germie = Germ(screen, (50, 50), (0, sheight-50))
germs = {(0, sheight-50): germie}
moves = 0


def reproduce():
    global moves
    mouse = pg.mouse.get_just_pressed()
    mpos = pg.mouse.get_pos()
    for k, germ in germs.copy().items():
        if (mouse[0] and germ.rect.collidepoint(mpos)) and germ.reproduce:
            coords1 = (germ.rect.x, germ.rect.top - germ.rect.height)
            coords2 = (germ.rect.right, germ.rect.y)
            germs[coords1] = Germ(screen, (50, 50), coords1)
            germs[coords2] = Germ(screen, (50, 50), coords2)
            germs.pop(k)
            moves += 1


def update(germ):
        if (germ.rect.right, germ.rect.y) not in germs and (germ.rect.x, germ.rect.top - germ.rect.height) not in germs:
            germ.reproduce = 1
        else: germ.reproduce = 0


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
            pg.quit()
            running = False

    screen.fill('black')
    draw_grid()
    for germ in germs.values():
        germ.draw()
        update(germ)
    reproduce()

    m = pg.font.Font(None, 40)
    text = m.render(f'moves: {moves}', True, 'gold', 'red')
    screen.blit(text, (swidth - 150, 10))
    pg.display.update()
