import pygame


all_objects = []


class Object:
    def __init__(self, x, y, w, h, color=(0, 0, 0)):
        global all_objects
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h))
        self.color = color
        self.id = 'to_object'
        self.tags = []
        self.alive = True
        all_objects.append(self)

    def __repr__(self):
        return f'{self.id} {(self.rect.x, self.rect.y)}'

    def update(self, *args):
        global all_objects
        pass

    def draw(self, surface, *args):
        self.image.fill(self.color)
        surface.blit(self.image, self.rect)


class Bullet(Object):
    def __init__(self, x, y, d, player_color):
        super().__init__(x, y, 5, 5, (55, 55, 55))
        self.dir = d
        self.player_color = player_color
        self.id = 'to_bullet'
        self.tags += ['bullet']

    def update(self, *args):
        global all_objects
        if self.alive:
            self.rect.move_ip(*self.dir)
            for object in all_objects:
                if 'tank' in object.tags:
                    if self.player_color != object.color and self.rect.colliderect(object.rect):
                        self.alive = False
                        object.alive = False
                elif 'wall' in object.tags:
                    if self.rect.colliderect(object.rect):
                        self.alive = False


class DefaultTank(Object):
    def __init__(self, x, y, d, color):
        super().__init__(x, y, 55, 55, color)
        self.dir = d
        self.up = None
        self.down = None
        self.right = None
        self.left = None
        self.shoot = None
        self.shoot_cd = 30
        self.prev_shoot = self.shoot_cd
        self.id = 'to_deftank'
        self.tags += ['tank']
        self.alive = True

    def set_controls(self, up, down, right, left, shoot):
        self.up = up
        self.down = down
        self.right = right
        self.left = left
        self.shoot = shoot

    def shot(self):
        global all_objects
        if not self.prev_shoot:
            self.prev_shoot = self.shoot_cd
            bullet = Bullet(self.rect.x + 25, self.rect.y + 25, (self.dir[0] * 2, self.dir[1] * 2), self.color)
            all_objects.append(bullet)

    def update(self, *args):
        global all_objects
        self.prev_shoot = max(0, self.prev_shoot - 1)

        if self.alive:
            can_move_up = can_move_down = can_move_left = can_move_right = True
            upper_rect = pygame.rect.Rect((self.rect.x, self.rect.y - 1, self.rect.h, self.rect.w))
            lower_rect = pygame.rect.Rect((self.rect.x, self.rect.y + 1, self.rect.h, self.rect.w))
            righter_rect = pygame.rect.Rect((self.rect.x + 1, self.rect.y, self.rect.h, self.rect.w))
            lefter_rect = pygame.rect.Rect((self.rect.x - 1, self.rect.y, self.rect.h, self.rect.w))

            for object in all_objects:
                if ('tank' in object.tags or 'wall' in object.tags) and object != self:
                    can_move_up = can_move_up and not upper_rect.colliderect(object.rect)
                    can_move_down = can_move_down and not lower_rect.colliderect(object.rect)
                    can_move_right = can_move_right and not righter_rect.colliderect(object.rect)
                    can_move_left = can_move_left and not lefter_rect.colliderect(object.rect)

            keys = args[0]
            if all([self.up, self.down, self.right, self.left, self.shoot]):
                if keys[self.up]:
                    if can_move_up:
                        self.rect.move_ip(0, -1)
                    self.dir = (0, -1)
                elif keys[self.down]:
                    if can_move_down:
                        self.rect.move_ip(0, 1)
                    self.dir = (0, 1)
                elif keys[self.left]:
                    if can_move_left:
                        self.rect.move_ip(-1, 0)
                    self.dir = (-1, 0)
                elif keys[self.right]:
                    if can_move_right:
                        self.rect.move_ip(1, 0)
                    self.dir = (1, 0)

                if keys[self.shoot]:
                    self.shot()
            else:
                raise Exception(f'Не установлено управление для {(self.rect.x, self.rect.y)}')

    def draw(self, surface, *args):
        self.image.fill(self.color)
        surface.blit(self.image, self.rect)
        if self.dir == (0, -1):
            pygame.draw.rect(surface,
                             (abs(self.color[0] - 50), abs(self.color[0] - 50), abs(self.color[0] - 50)),
                             (self.rect.x + 20, self.rect.y + 10, 15, 25))
        elif self.dir == (0, 1):
            pygame.draw.rect(surface,
                             (abs(self.color[0] - 50), abs(self.color[0] - 50), abs(self.color[0] - 50)),
                             (self.rect.x + 20, self.rect.y + 20, 15, 25))
        elif self.dir == (-1, 0):
            pygame.draw.rect(surface,
                             (abs(self.color[0] - 50), abs(self.color[0] - 50), abs(self.color[0] - 50)),
                             (self.rect.x + 10, self.rect.y + 20, 25, 15))
        elif self.dir == (1, 0):
            pygame.draw.rect(surface,
                             (abs(self.color[0] - 50), abs(self.color[0] - 50), abs(self.color[0] - 50)),
                             (self.rect.x + 20, self.rect.y + 20, 25, 15))


class DefaultWall(Object):
    def __init__(self, x, y, w, h, color=(0, 0, 0)):
        super().__init__(x, y, w, h, color)
        self.id = 'to_defwall'
        self.tags += ['wall']
