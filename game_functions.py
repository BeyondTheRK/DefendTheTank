import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien
import sound_effects as se

def get_num_aliens_x(ai_settings, alien_width):
    """Determine num aliens that fit in row"""
    avail_space_x = ai_settings.screen_width - 2 * alien_width
    num_aliens_x = int(avail_space_x / (2 * alien_width))
    return num_aliens_x

def get_num_rows(ai_settings, ship_height, alien_height):
    """Determine num aliens that fit in row"""
    avail_space_y = (ai_settings.screen_height -
                     (3 * alien_height) - ship_height)
    num_rows = int(avail_space_y / (2 * alien_height))
    return num_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ create alien and place it in the row."""
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create full fleet of aliens """
    # Create an alien and find number of aliens in a row
    # Spacing between each alien is equal to one alien width
    alien = Alien(ai_settings, screen)
    num_aliens_x = get_num_aliens_x(ai_settings, alien.rect.width)
    num_rows = get_num_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create fleet of aliens
    for row_number in range(num_rows):
        for alien_number in range(num_aliens_x):
            # Create an alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_keydown_events(event, ai_settings, screen, stats, ship,
                         aliens, bullets):
    """Respond to keypresses and mouse events."""

    #start/keep moving ship

    if event.key == pygame.K_RIGHT:
        # Move ship to the right
        ship.moving_right = True

    # elif event.key == pygame.K_a:
        # Move ship to the left
    #   ship.moving_left = True

    # elif event.key == pygame.K_d:
        # Move ship to the right
    # ship.moving_right = True
   
    elif event.key == pygame.K_LEFT:
        # Move ship to the left
        ship.moving_left = True

    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, ship, aliens, bullets)

    elif event.key == pygame.K_q:
        pygame.quit()
        sys.exit()
        
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        """how can we use pygame.key.get_pressed() func
        to hold down space bar for endless bullets?"""


def fire_bullet(ai_settings, screen, ship, bullets):
    """ fire a bullet if limit not reached yet."""
    # Create new bullet and add to bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        se.bullet_sound.play()
        
def check_keyup_events(event, ship):
    """Respond to keypresses and mouse events."""

    # stop moving ship
            
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:            
            check_keydown_events(event, ai_settings, screen, stats, ship,
                        aliens, bullets)
            
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """Start a new game when player clicks Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        
        #Resetting game settings
        ai_settings.initialize_dynamic_settings()

        #reset scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        
        #empty lists and restart games
        start_game(ai_settings, screen, stats, ship, aliens, bullets)

def start_game(ai_settings, screen, stats, ship, aliens, bullets):
        #hide mouse cursor
        pygame.mouse.set_visible(False)
        
        #Reset game stats
        stats.reset_stats()
        stats.game_active = True

        #empty list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #background music
        se.background_sound.play()  

        #create new fleet and center ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        
            
def check_fleet_edges(ai_settings, aliens):
    """respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """drop entire fleet and change fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1




def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    """ Update images on the screen and flip to new screen."""
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)

    #Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    #Draw score info
    sb.show_score()

    #draw play button if game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # make most recently drawn screen visible
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Update position of bullets and get rid of old bullets."""
    # Update bullet positions
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """Respond to bullet alien collisions"""
    #Remove any bullets and aliens that collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            se.alien_sound.play()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # if entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()
        

        
        create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien"""
    if stats.ships_left > 0:
        #Decrement ships_left
        stats.ships_left -= 1

        # update scoreboard
        sb.prep_ships()

        #Empty list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create new flewet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #Pause
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """check if any aliens have reached the bottom of screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #treat this the same as if ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if fleet is at an edge, Update positions of all apliens in fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    #look for alien ship collisions
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
