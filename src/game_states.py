"""
game_states.py - Estados del juego Julia's Run

Este archivo gestiona los diferentes estados o pantallas del juego:
- Menú principal
- Jugando
- Game Over
- Pausa (TODO)

Conceptos de programación cubiertos:
- Máquina de estados
- Gestión de eventos
- Renderizado condicional
- Flujo de control del programa

Referencias útiles:
- pygame.font: https://www.pygame.org/docs/ref/font.html
- pygame.event: https://www.pygame.org/docs/ref/event.html
"""

import pygame
from settings import *
import cv2
import os
from settings import GAME_OVER_VIDEO
from settings import VIDEO_MENU_IZQUIERDA
from settings import IMG_MENU_DERECHO
from settings import LOGO_MENU
from settings import LOGO_GAME_OVER
from settings import MUSIC_MENU

class GameStateManager:
    """
    Gestiona los diferentes estados del juego (menú, jugando, pausa, etc.)
    y llama a los métodos on_enter y on_exit de cada estado.
    """

    def __init__(self, states_dict):
        """
        Args:
            states_dict: Diccionario con los estados del juego:
                {
                    STATE_MENU: MenuState(),
                    STATE_PLAYING: PlayingState(),
                    STATE_PAUSED: PausedState(),
                    STATE_GAME_OVER: GameOverState(),
                }
        """
        self.states = states_dict
        self.current_state = None
        self.next_state = STATE_MENU  # arrancar en menú

        # Inicializar fuentes
        pygame.font.init()
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

    def change_state(self, new_state):
        self.next_state = new_state

    def update_state(self):
        """Si hay un cambio pendiente, ejecuta on_exit y on_enter."""
        if self.next_state is None:
            return
        
        new_state = self.next_state
        self.next_state = None

        # 1. Salida del estado anterior
        if self.current_state:
            state_obj = self.states[self.current_state]
            if hasattr(state_obj, "on_exit"):
                state_obj.on_exit()

        # 2. Entrar en el nuevo estado
        self.current_state = new_state
        state_obj = self.states[self.current_state]
        if hasattr(state_obj, "on_enter"):
            state_obj.on_enter()

    def get_current_state(self):
        return self.current_state



class MenuState:
    """
    Estado del menú principal.
    
    Muestra el título del juego, instrucciones básicas y
    espera a que el jugador presione una tecla para empezar.
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de menú."""

        self.state_manager = state_manager

        # ======================
        # CARGAR VIDEO
        # ======================
        base_path = os.path.dirname(os.path.dirname(__file__))  
        # Sube desde /estados/ hasta el directorio raíz

        video_path = os.path.join(base_path, VIDEO_MENU_IZQUIERDA)
        video_path = os.path.abspath(video_path)
                
        self.video = cv2.VideoCapture(video_path)
        if not self.video.isOpened():
            print("Error al cargar el video")

        # ======================
        # CARGAR IMAGEN DEL MENÚ
        # ======================
        image_base_path = os.path.dirname(os.path.dirname(__file__))

        image_path = os.path.join(image_base_path, IMG_MENU_DERECHO)
        image_path = os.path.abspath(image_path)

        try:
            # Cargar imagen original sin escalar (escalaremos después)
            self.original_menu_image = pygame.image.load(image_path)
            self.menu_image = self.original_menu_image  # Copia inicial
        except pygame.error as e:
            print(f"Error al cargar la imagen del menú: {e}")

        # Imagen fallback si no se pudo cargar
            self.original_menu_image = pygame.Surface((300, WINDOW_HEIGHT))
            self.original_menu_image.fill(PURPLE)
            self.menu_image = self.original_menu_image

        # Estas variables se inicializan luego en draw_background_animation()
        self.last_frame_time = 0
        self.current_frame_surface = None
        self.video_width = WINDOW_WIDTH // 2  # tamaño inicial de seguridad

        # ======================
        # CARGAR IMAGEN DEL TÍTULO
        # ======================
        title_image_base_path = os.path.dirname(os.path.dirname(__file__))

        title_image_path = os.path.join(title_image_base_path, LOGO_MENU) 
        title_image_path = os.path.abspath(title_image_path)

        try:
            self.title_image = pygame.image.load(title_image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error al cargar la imagen del título: {e}")
            self.title_image = None

        self.title_image = pygame.image.load(title_image_path).convert_alpha()
       
        self.title_image = pygame.transform.scale(self.title_image, (210, 220))

        # ======================
        # IMAGEN DEBAJO DE LAS INSTRUCCIONES
        # ======================
        bottom_image_path = os.path.join(image_base_path, IMG_PULPO_MENU)
        bottom_image_path = os.path.abspath(bottom_image_path)

        try:
            self.bottom_image_original = pygame.image.load(bottom_image_path).convert_alpha()
        except:
            print("Error al cargar la imagen inferior del menú")
            self.bottom_image_original = pygame.Surface((200, 200))
            self.bottom_image_original.fill((255, 0, 255))  # color placeholder


    def on_enter(self):
        music_base_path = os.path.dirname(os.path.dirname(__file__))
        music_path = os.path.join(music_base_path, MUSIC_MENU)
        music_path = os.path.abspath(music_path)

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Error al reproducir música de menú:", e)

           
    def handle_events(self, events):
        """
        Maneja los eventos del menú.
        
        Args:
            events: Lista de eventos de pygame
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_SPACE or event.key == KEY_ENTER:
                    pygame.mixer.music.stop()               
                    self.state_manager.change_state(STATE_PLAYING)
                elif event.key == KEY_ESCAPE:
                    return False  # Señal para salir del juego
        
        return True  # Continuar ejecutando
    
    def update(self):
        """Actualiza la lógica del menú (no hay mucho que hacer aquí)."""
        pass
    
    def draw_background_animation(self, screen):
        """Dibuja el video de fondo y la imagen a la derecha."""

        # Inicialización
        if not hasattr(self, "last_frame_time"):
            self.last_frame_time = 0
            self.current_frame_surface = pygame.Surface((WINDOW_WIDTH // 2, WINDOW_HEIGHT))
            self.current_frame_surface.fill(BLACK)
            self.video_width = WINDOW_WIDTH // 2  # Valor por defecto

        frame_delay = 120  # ms por frame (~8 FPS)
        current_time = pygame.time.get_ticks()

        # ¿Es hora de actualizar frame?
        if current_time - self.last_frame_time >= frame_delay:
            self.last_frame_time = current_time

            ret, frame = self.video.read()

            # Reiniciar si terminó
            if not ret or frame is None:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.video.read()

            if ret and frame is not None:
                try:
                    # BGR → RGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Redimensionar manteniendo proporción
                    h, w, _ = frame.shape
                    target_height = WINDOW_HEIGHT
                    aspect_ratio = w / h
                    target_width = int(target_height * aspect_ratio)

                    frame = cv2.resize(frame, (target_width, target_height))

                    # Convertir a Surface de pygame
                    self.current_frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                    self.video_width = target_width

                except Exception as e:
                    print("Error procesando frame:", e)
                    self.current_frame_surface.fill(BLUE)
                    self.video_width = WINDOW_WIDTH // 2

        # Dibujar video (izquierda)
        screen.blit(self.current_frame_surface, (0, 0))

        # --- REDIMENSIONAR LA IMAGEN CORRECTAMENTE ---
        right_panel_width = max(1, WINDOW_WIDTH - self.video_width)

        # Usar SIEMPRE la imagen original
        menu_img_scaled = pygame.transform.scale(
            self.original_menu_image,
            (right_panel_width, WINDOW_HEIGHT)
        )

        # Dibujar imagen a la derecha del video
        screen.blit(menu_img_scaled, (self.video_width, 0))

        

    def draw(self, screen):
        """
        Dibuja el menú principal.
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        self.draw_background_animation(screen)

        OFFSET_X = 300
        
        
        # Título del juego
        if self.title_image:
            title_rect = self.title_image.get_rect(center=(WINDOW_WIDTH//2 + OFFSET_X, 150))
            screen.blit(self.title_image, title_rect)
        else:
        # fallback por si la imagen falla
            title_text = self.state_manager.font_large.render("The Little Mermaid Yulia's Run", True, WHITE)
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2 + OFFSET_X, 150))
            screen.blit(title_text, title_rect)

        # # Subtítulo
        # subtitle_text = self.state_manager.font_medium.render("🧜‍♀️🐚 Aventura Épica", True, RED)
        # subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH//2 + OFFSET_X, 200))
        # screen.blit(subtitle_text, subtitle_rect)
        
        # Instrucciones
        instructions = [
            "Controles:",
            "Flechas → Mover",
            "Espacio → Lanzar estrella-shuriken",
            "Esquiva obstáculos rojos",
            "Recoge power-ups de colores",
            "",
            "Presiona ESPACIO para comenzar",
            "ESC para salir",
            "",
            "(Vocal performance by",
            "the game's developer)"
        ]
        
        start_y = 280
        for i, instruction in enumerate(instructions):
            color = WHITE if instruction != "" else BLACK
            text = self.state_manager.font_medium.render(instruction, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2 + OFFSET_X, start_y + i * 25))
            screen.blit(text, text_rect)
            
        # ======================
        # DIBUJAR LA IMAGEN DEBAJO DEL TEXTO
        # ======================
       
        TARGET_WIDTH = 180
        TARGET_HEIGHT = 180

        # Escalar la imagen
        bottom_image_scaled = pygame.transform.scale(
            self.bottom_image_original,
            (TARGET_WIDTH, TARGET_HEIGHT)
        )

        # Posición debajo del texto
        img_x = WINDOW_WIDTH//2 + OFFSET_X
        img_y = start_y + len(instructions) * 25 + 100  # un poco más abajo

        # Centrar la imagen en X
        img_rect = bottom_image_scaled.get_rect(center=(img_x, img_y))

        # Dibujarla en pantalla
        screen.blit(bottom_image_scaled, img_rect)

        
        # TODO 9: Añadir demo visual o animación de fondo
        # self.draw_background_animation(screen)


class PlayingState:
    """
    Estado principal del juego.
    
    Este es el estado donde ocurre toda la acción:
    - El jugador se mueve y lanza cuchillos
    - Aparecen obstáculos y power-ups
    - Se detectan colisiones
    - Se actualiza la puntuación
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de juego."""
        self.state_manager = state_manager 

        self.music_started = False
  
        
        #Sonidos
        self.snd_powerup = pygame.mixer.Sound(SOUND_POWERUP)
        self.snd_escudo = pygame.mixer.Sound(SOUND_ESCUDO)
        self.snd_throw = pygame.mixer.Sound(SOUND_THROW)

        self.snd_powerup.set_volume(1.0)
        self.snd_escudo.set_volume(1.0)
        self.snd_throw.set_volume(1.0)

        # --- Fondo del juego ---
        base_path = os.path.dirname(os.path.dirname(__file__))
        bg_path = os.path.join(base_path, IMG_MAIN)  
        bg_path = os.path.abspath(bg_path)

        self.background_image = pygame.image.load(bg_path).convert()
        # self.background_image = pygame.image.load(bg_path).convert_alpha()
        self.background_image = pygame.transform.scale(
            self.background_image,
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        self.bg_y = 0   # posición vertical del fondo
        self.bg_speed = 2  # píxeles por frame (ajusta a tu gusto)
        
    def on_enter(self):
        base_path = os.path.dirname(os.path.dirname(__file__))
        music_path = os.path.join(base_path, MUSIC_MAIN)
        music_path = os.path.abspath(music_path)

        if not self.music_started:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            self.music_started = True
        else:
            pygame.mixer.music.unpause()

          
            
    def handle_events(self, events, player, knife_cooldown):
        """
        Maneja los eventos durante el juego.
        
        Args:
            events: Lista de eventos de pygame
            player: Instancia del jugador
            knife_cooldown: Timer de cooldown para cuchillos
            
        Returns:
            list: Lista de nuevos cuchillos creados (si se lanzó alguno)
        """
        
        new_knives = []
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_SPACE:
                    # Lanzar cuchillo si no hay cooldown
                    if knife_cooldown.is_ready():
                        from entities import Knife  # Import local para evitar circular
                        new_knife = Knife(player.rect)
                        new_knives.append(new_knife)
                        knife_cooldown.start_cooldown()
                        
                        # TODO 4: Añadir sonido de lanzamiento
                        # pygame.mixer.Sound(SOUND_THROW).play()
                
                elif event.key == KEY_P:
                    # ✅ IMPLEMENTADO: Implementar pausa
                    pygame.mixer.music.pause() 
                    self.state_manager.change_state(STATE_PAUSED)
                    print("Juego pausado")  # Debug
                
                elif event.key == KEY_ESCAPE:
                    return new_knives, False  # Salir del juego
        
        return new_knives, True  # Continuar jugando
    
    def update(self, player, obstacles, knives, powerups, effects, knife_cooldown):
        """
        Actualiza toda la lógica del juego.
        
        Args:
            player: Instancia del jugador
            obstacles: Lista de obstáculos
            knives: Lista de cuchillos
            powerups: Lista de power-ups
            effects: Sistema de efectos de power-ups
            knife_cooldown: Timer de cooldown
            
        Returns:
            bool: True si el jugador sigue vivo, False si Game Over
        """
        
        # Actualizar timers
        knife_cooldown.update()
        effects.update(player)
        
        # Mover jugador según teclas presionadas
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        # Actualizar obstáculos
        for obstacle in obstacles[:]:  # [:] crea una copia para iterar seguro
            if not obstacle.update():
                # Obstáculo salió de pantalla - dar puntos por esquivar
                obstacles.remove(obstacle)
                player.score += POINTS_PER_OBSTACLE_AVOIDED
        
        # Actualizar cuchillos
        for knife in knives[:]:
            if not knife.update():
                knives.remove(knife)
        
        # Actualizar power-ups
        for powerup in powerups[:]:
            if not powerup.update():
                powerups.remove(powerup)
        
        # Detectar colisiones jugador-obstáculos
        for obstacle in obstacles[:]:
            if player.rect.colliderect(obstacle.rect):
                obstacles.remove(obstacle)
                if not player.take_damage():
                    # Game Over
                    return False
                
                # TODO 4: Añadir sonido de daño
                # pygame.mixer.Sound(SOUND_HIT).play()
        
        # Detectar colisiones cuchillo-obstáculos
        for knife in knives[:]:
            for obstacle in obstacles[:]:
                if knife.rect.colliderect(obstacle.rect):
                    # Destruir ambos y dar puntos
                    knives.remove(knife)
                    obstacles.remove(obstacle)
                    player.score += POINTS_PER_OBSTACLE_DESTROYED
                    
                    # TODO 7: Crear efecto de explosión
                    # explosion = Explosion(obstacle.rect.center)
                    break
        
        # Detectar colisiones jugador-power-ups
        for powerup in powerups[:]:
            if player.rect.colliderect(powerup.rect):
                powerups.remove(powerup)
                player.score += POINTS_PER_POWERUP
                
                # Activar efecto según el tipo
                if powerup.type == 'vodka':
                    effects.activate_vodka_boost(player)
                elif powerup.type == 'tea':
                    effects.activate_tea_shield(player)
        
        return True  # Jugador sigue vivo
    
    def draw(self, screen, player, obstacles, knives, powerups, effects, knife_cooldown):
        """
        Dibuja todo el estado del juego.
        
        Args:
            screen: Superficie donde dibujar
            player: Instancia del jugador
            obstacles: Lista de obstáculos
            knives: Lista de cuchillos
            powerups: Lista de power-ups
            effects: Sistema de efectos
            knife_cooldown: Timer de cooldown
        """
        
        # --- Fondo con scroll infinito ---
        self.bg_y += self.bg_speed
        if self.bg_y >= WINDOW_HEIGHT:
            self.bg_y = 0

        screen.blit(self.background_image, (0, self.bg_y))
        screen.blit(self.background_image, (0, self.bg_y - WINDOW_HEIGHT))

        
        # Dibujar todas las entidades
        player.draw(screen)
        
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        for knife in knives:
            knife.draw(screen)
        
        for powerup in powerups:
            powerup.draw(screen)
        
        # Dibujar HUD (Heads-Up Display)
        self.draw_hud(screen, player, effects, knife_cooldown)
    
    def draw_hud(self, screen, player, effects, knife_cooldown):
        """
        Dibuja la interfaz de usuario (puntuación, vidas, etc.).
        
        Args:
            screen: Superficie donde dibujar
            player: Instancia del jugador
            effects: Sistema de efectos
            knife_cooldown: Timer de cooldown
        """
        
        # Puntuación
        score_text = self.state_manager.font_medium.render(f"Puntuación: {player.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Vidas
        lives_text = self.state_manager.font_medium.render(f"Vidas: {player.lives}", True, WHITE)
        screen.blit(lives_text, (10, 40))
        
        # Estado del escudo
        if player.has_shield:
            shield_text = self.state_manager.font_small.render("🛡️ ESCUDO ACTIVO", True, TEA_COLOR)
            screen.blit(shield_text, (10, 70))
        
        # ✅ IMPLEMENTADO: Barra de cooldown visual
        knife_cooldown.draw_cooldown_bar(screen)
        
        # ✅ IMPLEMENTADO: Efectos activos
        effects.draw_active_effects(screen, self.state_manager.font_small)
        


class GameOverState:
    """
    Estado de Game Over.
    
    Muestra la puntuación final, el récord y permite
    reiniciar el juego o volver al menú.
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de Game Over."""
        base_path = os.path.dirname(os.path.dirname(__file__))  
        
        video_path = os.path.join(base_path, GAME_OVER_VIDEO)
        video_path = os.path.abspath(video_path)

        self.video = cv2.VideoCapture(video_path)
        if not self.video.isOpened():
            print("Error al cargar el video de Game Over")

        # Variables internas para controlar el video
        self.last_frame_time = 0
        self.current_frame_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.current_frame_surface.fill(BLACK)

        self.state_manager = state_manager
        self.final_score = 0
        self.best_score = 0
        self.is_new_record = False

        # --- Imagen logo ---
        logo_path = os.path.join(base_path, LOGO_GAME_OVER)
        logo_path = os.path.abspath(logo_path)
      
        self.logo_image = pygame.image.load(logo_path).convert_alpha()
        
        self.logo_image = pygame.transform.scale(self.logo_image, (300, 300))

        self.state_manager = state_manager

        # --- Sonido de Game Over ---
        sound_path = os.path.join(base_path, SOUND_GAME_OVER)
        sound_path = os.path.abspath(sound_path)
        self.game_over_sound = pygame.mixer.Sound(sound_path)
        self.game_over_sound.set_volume(0.8)  # opcional
        self.sound_played = False

    
    def set_scores(self, final_score, best_score):
        """
        Establece las puntuaciones para mostrar.
        
        Args:
            final_score: Puntuación de la partida actual
            best_score: Mejor puntuación histórica
        """
        self.final_score = final_score
        self.best_score = best_score
        self.is_new_record = final_score > best_score

        # Reproducir sonido solo una vez
        if not self.sound_played:
            self.game_over_sound.play()
            self.sound_played = True
    
    def handle_events(self, events):
        """
        Maneja los eventos en la pantalla de Game Over.
        
        Args:
            events: Lista de eventos de pygame
        """
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_ENTER:
                    self.sound_played = False   # <-- reset
                    self.state_manager.change_state(STATE_PLAYING)
                elif event.key == KEY_ESCAPE:
                    self.sound_played = False   # <-- reset
                    return False  # Salir del juego
        
        return True
    
    def update(self):
        """Actualiza la lógica del Game Over."""
        pass

    def draw_background_animation(self, screen):
        """Dibuja el video de fondo en loop."""

        frame_delay = 100  # ms por frame (~10 FPS, ajustable)
        current_time = pygame.time.get_ticks()

        if current_time - self.last_frame_time >= frame_delay:
            self.last_frame_time = current_time

            ret, frame = self.video.read()

            # Reiniciar si el video terminó
            if not ret or frame is None:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.video.read()

            if ret and frame is not None:
                try:
                    # BGR → RGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Escalar al tamaño completo de la ventana
                    frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))

                    # Convertir a Surface
                    self.current_frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

                except Exception as e:
                    print("Error procesando frame del video Game Over:", e)
                    self.current_frame_surface.fill(BLACK)

        # Dibujar video
        screen.blit(self.current_frame_surface, (0, 0))

    
    def draw(self, screen):
        """
        Dibuja la pantalla de Game Over.
        
        Args:
            screen: Superficie donde dibujar
        """
                
        # Primero dibujar video animado
        self.draw_background_animation(screen)

        offset_x = 320   
        offset_y = 100 
        
        # Título
        logo_rect = self.logo_image.get_rect(center=(WINDOW_WIDTH // 2 + offset_x, 150 + offset_y))
        screen.blit(self.logo_image, logo_rect)
        
        # Puntuación final
        score_text = self.state_manager.font_large.render(f"Tu puntuación: {self.final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2 + offset_x, 320 + offset_y))
        screen.blit(score_text, score_rect)
        
        # Récord
        if self.is_new_record:
            record_text = self.state_manager.font_large.render("¡NUEVO RÉCORD!", True, YELLOW)
        else:
            record_text = self.state_manager.font_large.render(f"Récord: {self.best_score}", True, YELLOW)
        
        record_rect = record_text.get_rect(center=(WINDOW_WIDTH//2 + offset_x, 360 + offset_y))
        screen.blit(record_text, record_rect)
        
        # Instrucciones
        restart_text = self.state_manager.font_medium.render("Presiona ENTER para jugar de nuevo", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2 + offset_x, 450 + offset_y))
        screen.blit(restart_text, restart_rect)
        
        exit_text = self.state_manager.font_medium.render("ESC para salir", True, WHITE)
        exit_rect = exit_text.get_rect(center=(WINDOW_WIDTH//2 + offset_x, 480 + offset_y))
        screen.blit(exit_text, exit_rect)


# ✅ IMPLEMENTADO: Estado de pausa
class PausedState:
    """
    Estado cuando el juego está pausado.
    
    En este estado el juego se detiene pero se mantiene visible
    en el fondo con una indicación de pausa superpuesta.
    """
    
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.pulse_timer = 0

        # --- VIDEO DE FONDO ---
        base_path = os.path.dirname(os.path.dirname(__file__))
        video_path = os.path.join(base_path, PAUSE_VIDEO)
        video_path = os.path.abspath(video_path)

        self.video = cv2.VideoCapture(video_path)

        if not self.video.isOpened():
            print("ERROR: No se pudo cargar el video de pausa")

        self.last_frame_time = 0
        self.current_frame_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.current_frame_surface.fill((0, 0, 0))

    
    def handle_events(self, events):
        """
        Maneja eventos en estado de pausa.
        
        Args:
            events: Lista de eventos de pygame
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_P:
                    # Reanudar el juego
                    pygame.mixer.music.unpause()
                    self.state_manager.change_state(STATE_PLAYING)
                    print("Juego reanudado")  # Debug
                elif event.key == KEY_ESCAPE:
                    # Volver al menú principal
                    self.state_manager.change_state(STATE_MENU)
                    print("Volviendo al menú desde pausa")  # Debug
        return True
    
    def update(self):
        """Actualizar efectos visuales de la pausa."""
        self.pulse_timer += 1

    def draw_background_video(self, screen):
        frame_delay = 100  # 10 FPS
        current_time = pygame.time.get_ticks()

        if current_time - self.last_frame_time >= frame_delay:
            self.last_frame_time = current_time

            ret, frame = self.video.read()

            if not ret or frame is None:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.video.read()

            if ret and frame is not None:
                try:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
                    self.current_frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                except:
                    self.current_frame_surface.fill((0, 0, 0))

        screen.blit(self.current_frame_surface, (0, 0))

    
    def draw(self, screen, game_surface=None):
        """
        Dibuja la pantalla de pausa.
        
        Args:
            screen: Superficie donde dibujar
            game_surface: Superficie del juego de fondo (opcional)
        """
        self.draw_background_video(screen)

        # Aplicar oscurecimiento para que el texto sea legible
        # overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        # overlay.fill((0, 0, 0))
        # overlay.set_alpha(120)
        # screen.blit(overlay, (0, 0))

              
        self.pulse_timer += 1
        pulse_factor = abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 3).x)
        pulse_size = int(FONT_SIZE_LARGE + pulse_factor * 10)
        
        try:
            pulse_font = pygame.font.Font(None, pulse_size)
        except:
            pulse_font = self.state_manager.font_large
        
        paused_text = pulse_font.render("PAUSED", True, YELLOW)
        paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 200))
        
        # Sombra del texto para mejor legibilidad
        shadow_text = pulse_font.render("PAUSED", True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(paused_rect.centerx + 3, paused_rect.centery + 3))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(paused_text, paused_rect)
        
        # Instrucciones
        instructions = [
            "Presiona P para continuar",
            "ESC para volver al menú"
        ]
        
        y_offset = WINDOW_HEIGHT//2 + 300
        for instruction in instructions:
            text = self.state_manager.font_medium.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y_offset))
            
            # Fondo semi-transparente para las instrucciones
            bg_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5,
                                text_rect.width + 20, text_rect.height + 10)
            pygame.draw.rect(screen, BLACK, bg_rect)
            pygame.draw.rect(screen, WHITE, bg_rect, 1)
            
            screen.blit(text, text_rect)
            y_offset += 40



# === NOTAS EDUCATIVAS ===
"""
Conceptos importantes sobre máquinas de estados:

1. SEPARACIÓN DE RESPONSABILIDADES:
   Cada estado maneja solo su propia lógica, lo que hace
   el código más organizado y fácil de mantener.

2. TRANSICIONES DE ESTADO:
   Los estados pueden cambiar a otros estados según eventos
   (teclas presionadas, condiciones del juego, etc.).

3. GESTIÓN DE EVENTOS:
   Cada estado decide cómo responder a eventos de teclado
   y ratón de manera apropiada para su contexto.

4. RENDERIZADO CONDICIONAL:
   Solo se dibuja lo que es relevante para el estado actual,
   mejorando el rendimiento y la claridad visual.

5. FLUJO DEL PROGRAMA:
   La máquina de estados define cómo el usuario navega
   por las diferentes pantallas del juego.

Ejercicio para estudiantes:
- Implementar el estado de pausa (TODO 1)
- Añadir un estado de opciones o configuración
- Crear transiciones animadas entre estados
"""