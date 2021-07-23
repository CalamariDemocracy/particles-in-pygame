import pygame

from particle import ParticleType


WIDTH = 800
HEIGHT = 600

FPS = 60 


def get_dt(ms):
    return ms/1000*60


def main():
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

    left_click = False

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
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_click = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left_click = False
                            
        mouse_pos = pygame.mouse.get_pos()
        mouse_particles.add_particles(mouse_pos, 5, 10)

        if left_click:
            click_particles.add_particles(mouse_pos, 20, 5)
        
        for particle_type in particle_types:
            particle_type.update_particles(((0, 0), (screen.get_width(), screen.get_height())), dt=dt)

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