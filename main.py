import pygame
import sys

pygame.init()

X = 640
Y = 360

# Colors and setup
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
clicker = (255, 255, 255)

# Set up the screen
DISPLAY = pygame.display.set_mode([X, Y])
pygame.display.set_caption('Pygame clicker')

paused = False
running = True

font = pygame.font.Font(None, 24)
shop_font = pygame.font.Font(None, 14)

mouse_clicks = 0
clicks = 0
clicker_size = 100
#this is used for a wobble effect
size_tension = 0
deltaTime = 0
click_multiplier = 1
clicker_click_modifier = 0

class Upgrade:
    upgrades = []

    def __init__(self, base_cost, cost_multiplier, gives_on_tick_or_click, name, modifier):
        self.base_cost = base_cost
        self.cost_multiplier = cost_multiplier
        self.owned = 0
        self.cost = 0
        self.gives_on_tick_or_click = gives_on_tick_or_click
        self.name = name
        self.modifier = modifier
        self.tick = 0
        Upgrade.upgrades.append(self)

    def calculate_cost(self):
        self.cost = round(self.base_cost * pow(self.cost_multiplier, self.owned))

    @staticmethod
    def update_all_costs():
        for upgrade in Upgrade.upgrades:
            upgrade.calculate_cost()

# Define upgrades
extra_mouse = Upgrade(15, 1.15, 1, "Extra mouse", 0)
steel_click = Upgrade(50, 1.15, 2, "Steel clicker", 1)
autoclick = Upgrade(100, 1.15, 1, "Autoclicker", 0)
shiny_click = Upgrade(100, 1.15, 2, "Shiny clicks", 5)
prestige = Upgrade(10000, 1.5, 0, "Prestige", 1)
while running:
    DISPLAY.fill((0, 0, 0))
    #set modifier
    clicker_click_modifier = 1
    for upgrade in Upgrade.upgrades:
        if upgrade.gives_on_tick_or_click == 2:
            clicker_click_modifier += upgrade.modifier * upgrade.owned
    (mouse_x, mouse_y) = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicks += 1
            if mouse_x > (X / 2) - clicker_size and mouse_x < (X / 2) + clicker_size and mouse_y > (Y / 2) - clicker_size and mouse_y < (Y / 2) + clicker_size:
                clicks += clicker_click_modifier * click_multiplier
            for upgrade in Upgrade.upgrades:
                if (
                    mouse_x > 10
                    and mouse_x < (X / 4) - 10
                    and mouse_y > 5 + (Upgrade.upgrades.index(upgrade) * (Y / 6))
                    and mouse_y < ((Upgrade.upgrades.index(upgrade) + 1) * (Y / 6)) - 10
                ):
                    if clicks >= upgrade.cost:
                        clicks -= upgrade.cost
                        upgrade.owned += 1
                        Upgrade.update_all_costs()
            if (
                mouse_x > 10
                and mouse_x < (X / 4) - 10
                and mouse_y > 5 + (len(Upgrade.upgrades) * (Y / 6))
                and mouse_y < ((len(Upgrade.upgrades) + 1) * (Y / 6)) - 10
            ):
                if clicks >= prestige.cost:
                    clicks = 0
                    prestige.owned += 1
                    Upgrade.update_all_costs()
                    for upgrade in Upgrade.upgrades:
                        upgrade.owned = 0

    if mouse_x > (X / 2) - clicker_size and mouse_x < (X / 2) + clicker_size and mouse_y > (Y / 2) - clicker_size and mouse_y < (Y / 2) + clicker_size:
        if event.type == pygame.MOUSEBUTTONDOWN:
            size_tension += (50 - clicker_size) * 0.5
            size_tension = (size_tension) * 0.8
            clicker_size += size_tension
        else:
            size_tension += (55 - clicker_size) * 0.5
            size_tension = (size_tension) * 0.8
            clicker_size += size_tension
    else:
        size_tension += (50 - clicker_size) * 0.5
        size_tension = (size_tension) * 0.8
        clicker_size += size_tension

    # Shop button setup
    pygame.draw.rect(DISPLAY, (82, 148, 255), (0, 0, X / 4, Y))
    for upgrade in Upgrade.upgrades:
        pygame.draw.rect(
            DISPLAY,
            (82, 180, 255),
            (
                5,
                5 + (Upgrade.upgrades.index(upgrade) * (Y / 6)),
                (X / 4) - 10,
                (Y / 6) - 10,
            ),
            5,
            15,
        )

    # Draw upgrades
    for upgrade in Upgrade.upgrades:
        upgrade.calculate_cost()
        text = pygame.font.Font(None, int((X / 25) - len(str(upgrade.owned)) - 1)).render(
            upgrade.name + ": " + str(upgrade.owned), True, white
        )
        DISPLAY.blit(text, [20, (Upgrade.upgrades.index(upgrade) * (Y / 6)) + 10])
        text = pygame.font.Font(None, int((X / 20) - len(str(upgrade.cost)) - 1)).render(
            "Cost: " + str(upgrade.cost), True, white
        )
        DISPLAY.blit(text, [20, (Upgrade.upgrades.index(upgrade) * (Y / 6)) + 30])

    # Update upgrade costs
    Upgrade.update_all_costs()

    # Run global tick event
    for upgrade in Upgrade.upgrades:
        if upgrade.gives_on_tick_or_click == 1 and upgrade.owned > 0 and upgrade.tick >= 120 / upgrade.owned:
            upgrade.tick = 0
            clicks += 1 * click_multiplier
        elif upgrade.gives_on_tick_or_click == 1 and upgrade.owned > 0 and upgrade.tick < 120 / upgrade.owned:
            upgrade.tick += 1

    # Draw multiplier
    click_multiplier = prestige.owned + prestige.modifier
    text = pygame.font.Font(None, 32 - len(str(click_multiplier)) - 1).render(
        "Multiplier: x" + str(click_multiplier), True, white
    )
    DISPLAY.blit(text, [X - len("Multiplier: x" + str(click_multiplier)) * 10, 20])

    # Draw clicks count
    text_offset = -(40) - len(str(clicks)) * 5
    text = font.render("clicks: " + str(clicks), True, white)
    DISPLAY.blit(text, [(X / 2) + text_offset, 20])

    # Draw clicker
    pygame.draw.circle(DISPLAY, clicker, (X / 2, Y / 2), clicker_size)

    clock.tick(30)
    pygame.display.flip()
