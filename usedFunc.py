from settings import *
import sys
import pygame as pg


def quit():
    pg.quit()
    sys.exit()


def wait():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    quit()
            if event.type == pg.MOUSEBUTTONUP:
                return
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    return


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_hit_rect2(one, two):
    return one.hit_rect.colliderect(two.hit_rect)


def cross_fade(surf, img, clock, col=BLACK):
    fill_surface = pg.Surface((WIDTH, HEIGHT))
    fill_surface.fill(col)

    done = False
    alpha = 220
    mult = -1
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.event.clear()
        fill_surface.set_alpha(alpha)
        surf.blit(img, (0, 0))
        surf.blit(fill_surface, (0, 0))
        pg.display.flip()
        if alpha <= 0:
            mult = 1
        if mult == -1:
            alpha = alpha + mult * 2
        else:
            alpha = alpha + mult * 3
            if alpha >= 250:
                done = True
        clock.tick(FPS)


def word_wrap():
    pass
