import math
import random

import pygame


WIDTH = 800
HEIGHT = 600

FPS = 60 

MAX_ALPHA = 255


class Particle:
    def __init__(self, pos: tuple, vel: list, lifetime: float, color: str, scale_type: str = 'shrink'):
        self.pos = pygame.Vector2(pos)
        self.vel = vel
        self.lifetime = lifetime
        self.life_left = lifetime
        self.alpha = MAX_ALPHA
        self.color = pygame.Color(color)
        self.scaling = -1 if scale_type == 'shrink' else 1

    def update(self, gravity: float = 0, dt: int = 1):
        self.pos.x += self.vel[0] * dt
        self.pos.y += self.vel[1] * dt
        self.vel[1] += gravity * dt
        self.life_left -= 1 * dt
        self.alpha = self.life_left/self.lifetime*255

    def draw(self, surface: pygame.Surface):
        particle_surface = pygame.Surface((self.lifetime, self.lifetime))
        particle_surface.set_alpha(self.alpha)
        pygame.draw.circle(particle_surface, self.color, (self.life_left/2, self.life_left/2), self.life_left // 2)
        surface.blit(particle_surface, (self.pos[0] - self.lifetime/2, self.pos[1] - self.lifetime/2))

    def is_dead(self):
        return self.life_left <= 0

    def copy(self):
        return Particle(self.pos, self.vel, self.lifetime, self.color, 'shrink' if self.scaling < 0 else 'expand')
    

class ParticleType:
    def __init__(self, vel_range: tuple, lifetime_range: tuple, colors: tuple, gravity: float = 0, scale_type: str = 'shrink'):
        self.particles = []
        self.vel_range = vel_range
        self.lifetime_range = lifetime_range
        self.gravity = gravity
        self.colors = colors
        self.scale_type = scale_type

    def get_new_particle(self, spawn_range=((0, 0), (0, 0)), offset=0, colors=None):
        # spawn_range = (min_pos, max_pos) | ((min_x, min_y), (max_x, max_y))
        if isinstance(spawn_range[0], tuple) and isinstance(spawn_range[1], tuple):
            pos = (random.randint(spawn_range[0][0] - offset, spawn_range[1][0] + offset), random.randint(spawn_range[0][1] - offset, spawn_range[1][1] + offset))
        elif isinstance(spawn_range[0], int) and isinstance(spawn_range[1], int):
            pos = spawn_range[0] + random.randint(-offset, offset), spawn_range[1] + random.randint(-offset, offset)
        vel = [random.randint(self.vel_range[0][0], self.vel_range[1][0]), random.randint(self.vel_range[0][1], self.vel_range[1][1]), random.randint(self.vel_range[0][1], self.vel_range[1][1])]
        lifetime = random.randint(min(self.lifetime_range), max(self.lifetime_range))
        color = random.choice(self.colors)
        particle = Particle(pos, vel, lifetime, color, self.scale_type)
        return particle

    def add_particles(self, spawn_range=((0, 0), (0, 0)), offset=0, amount=1):
        for i in range(amount):
            particle = self.get_new_particle(spawn_range)
            self.particles.append(particle)

    def update_particles(self, pos_range, dt=1):
        if not self.particles:
            return
        for particle in self.particles[:]:
            particle.update(self.gravity, dt)
            if particle.is_dead():
                self.particles.remove(particle)
                continue
            if particle.pos.x + particle.lifetime/2 < pos_range[0][0] or particle.pos.x - particle.lifetime/2 > pos_range[1][0] or \
                particle.pos.y + particle.lifetime/2 < pos_range[0][1] or particle.pos.y - particle.lifetime/2 > pos_range[1][1]:
                self.particles.remove(particle)
    
    def draw_particles(self, surface):
        if not self.particles:
            return
        for particle in self.particles:
            particle.draw(surface)


def get_dt(ms):
    return ms/1000*60


def main():
    print(pygame.colordict.THECOLORS)
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    full_screen = False
    particle_colors = (
        'white',
        'whitesmoke',
        'ghostwhite',
        'gray90'
    )
    mouse_particles = ParticleType(((-2, -2), (2, 2)), (4, 24), ('red', ), 0.2)
    click_particles = ParticleType(((-4, -4), (4, 4)), (24, 48), particle_colors, 0)
    particle_types = (mouse_particles, click_particles)
    pygame.mouse.set_visible(False)
    font = pygame.font.Font(None, 32)

    while True:
        ms = clock.tick(FPS)
        dt = get_dt(ms)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    full_screen = not full_screen
                if event.key == pygame.K_ESCAPE:
                    full_screen = False
                if full_screen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_particles.add_particles(event.pos, 5, 20)
                
        mouse_pos = pygame.mouse.get_pos()
        mouse_particles.add_particles(mouse_pos, 10, 5)

        for particle_type in particle_types:
            particle_type.update_particles(((0, 0), (WIDTH, HEIGHT)), dt=dt)

        screen.fill('black')
        for particle_type in particle_types:
            particle_type.draw_particles(screen)

        fps_text = font.render(f'{round(clock.get_fps())}', True, 'gold')
        screen.blit(fps_text, (8, 8))

        pygame.display.update()


if __name__ == '__main__':
    pygame.display.set_caption('particle test')
    main()

pygame.quit()