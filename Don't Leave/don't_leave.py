import pygame
import sys

pygame.init()
pygame.mixer.init()

# --- Window Setup ---
WIDTH, HEIGHT = 900, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Don't Leave")
clock = pygame.time.Clock()

# --- Fonts (Bassy) ---
BASSY_FONT_PATH = "Don't Leave/bassy/Bassy.ttf"
FONT_MAIN = pygame.font.Font(BASSY_FONT_PATH, 46)
FONT_WHISPER = pygame.font.Font(BASSY_FONT_PATH, 36)
FONT_SECTION = pygame.font.Font(BASSY_FONT_PATH, 20)

# --- Colors ---
BG_COLOR = (8, 8, 18)
TEXT_COLOR = (230, 240, 255)
WHISPER_COLOR = (180, 220, 240)
SLOW_FADE_COLOR = (170, 210, 235)
SECTION_COLOR = (60, 120, 140)
GLOW_COLOR = (0, 220, 255)         
DIM_COLOR_FACTOR = 0.35  

# --- SYNC ADJUSTMENT ---

SYNC_OFFSET = 0.2

SONG_START = 116.0

#  LYRICS WITH PRECISE TIMESTAMPS:
# (start_sec, end_sec, text, style) | | {style: "main", "whisper", "slow_fade", "section"}

lyrics = [
    # --- PRE-CHORUS ---
    (116.0, 119.0, "Overcompensating for the lack of all my feelings",              "main"),
    (119.0, 122.5, "I know",                                                        "slow_fade"),
    (122.7, 124.0, "Never meant to hurt you, girl",                                 "main"),
    (124.0, 127.0, "I love you but I think should go",                              "slowfade"),
    (127.0, 128.0, "(Oh-oh)",                                                       "whisper"),

    # --- BRIDGE --- 
    (128.0, 128.0, "---SECTION---",                                                 "section"),
    (128.0, 129.0, "Oh Baby, baby,",                                                "whisper"),
    (129.0, 131.0, "Just stay here",                                                "main"),
    (131.0, 132.0, "Never wanted you to",                                           "main"),
    (132.0, 134.5, "Disappear",                                                     "main"),
    (134.5, 136.0, "Can't deny the",                                                "main"),
    (135.5, 138.0, "Endless chemistry",                                             "main"),
    (137.5, 140.5, "So don't you fall in love",                                     "main"),

    # --- CHORUS --- 
    (141.0, 141.0, "---SECTION---",                                                 "section"),
    (141.0, 142.0, "(Oh baby, baby)",                                               "whisper"),
    (142.0, 143.8, "Just stay here",                                                "main"),
    (143.7, 145.0, "Never wanted you to",                                           "main"),
    (145.0, 147.5, "Disappear",                                                     "main"),
    (147.0, 150.0, "But don't you fall in love again with me",                      "main"),
    (150.0, 153.0, "Cause we could fuck it up so easily",                           "main"),
    (153.5, 155.5, "(Oh Baby, baby)",                                               "whisper"),
]

# --- DISPLAY SETTINGS ---

LINE_HEIGHT = 58          # vertical spacing between lines
START_Y = 100             # first line Y position
MAX_VISIBLE_LINES = 8     # max lines on screen before oldest fades
FADE_IN_SPEED = 500       # alpha per second for fade in
FADE_OUT_SPEED = 100      # alpha per second for old lines dimming
ACTIVE_LINE_GLOW = True

# --- Typing Settings ---
TYPING_SPEED = 17  


def get_font_and_color(style):
    if style == "whisper":
        return FONT_WHISPER, WHISPER_COLOR
    elif style in ("slow_fade", "slowfade"):
        return FONT_MAIN, SLOW_FADE_COLOR
    elif style == "section":
        return FONT_SECTION, SECTION_COLOR
    else:
        return FONT_MAIN, TEXT_COLOR


def get_song_time():
    """Get current absolute song position with sync offset."""
    pos_ms = pygame.mixer.music.get_pos()
    if pos_ms == -1:
        return -1
    return SONG_START + pos_ms / 1000.0 + SYNC_OFFSET


def draw_text_simple(text, font, color, alpha, pos):
    """Draw text centered at given Y position (no typing effect)."""
    if alpha <= 1 or not text:
        return
    clamped = max(0, min(255, int(alpha)))
    center_x = WIDTH // 2
    surf = font.render(text, True, color)
    surf.set_alpha(clamped)
    rect = surf.get_rect(center=(center_x, pos))
    screen.blit(surf, rect)


def draw_typing_text(text, visible_chars, font, color, alpha, pos):
    """Draw text with letter-by-letter typing effect, centered."""
    if alpha <= 1 or not text:
        return
    clamped = max(0, min(255, int(alpha)))
    center_x = WIDTH // 2

    # The portion of text revealed so far
    shown_text = text[:visible_chars]

    # Render the full text to get total width for centering
    full_surf = font.render(text, True, color)
    full_width = full_surf.get_width()
    full_height = full_surf.get_height()

    # Starting X so the final result is centered
    start_x = center_x - full_width // 2

    if shown_text:
        shown_surf = font.render(shown_text, True, color)
        shown_surf.set_alpha(clamped)
        shown_rect = shown_surf.get_rect(topleft=(start_x, pos - full_height // 2))
        screen.blit(shown_surf, shown_rect)

# --- DISPLAY STATE ---

class DisplayLine:
    """A line currently visible on screen with letter-by-letter typing."""
    def __init__(self, text, style, y_pos, start_time, end_time, is_active=True):
        self.text = text
        self.style = style
        self.y_pos = y_pos
        self.start_time = start_time
        self.end_time = end_time
        self.alpha = 0.0
        self.target_alpha = 255.0
        self.is_active = is_active
        self.font, self.color = get_font_and_color(style)
        self.char_count = len(text) if text else 0
        self.typing_done = False  # True once all characters are revealed

    def update(self, dt):
        """Update alpha each frame."""
        if self.is_active:
            self.alpha = min(self.target_alpha, self.alpha + FADE_IN_SPEED * dt)
        else:
            dim_target = 255 * DIM_COLOR_FACTOR
            if self.alpha > dim_target:
                self.alpha = max(dim_target, self.alpha - FADE_OUT_SPEED * dt)

    def get_visible_char_count(self, song_time):
        """How many characters should be visible at the given song time."""
        if self.char_count == 0:
            return 0
        elapsed = song_time - self.start_time
        # Fixed typing speed so short lines type out fast
        typing_duration = self.char_count / TYPING_SPEED
        # But never exceed the line's actual duration
        line_duration = self.end_time - self.start_time
        if line_duration > 0:
            typing_duration = min(typing_duration, line_duration)
        if typing_duration <= 0:
            return self.char_count
        progress = max(0.0, min(1.0, elapsed / typing_duration))
        count = int(progress * self.char_count) + (1 if progress > 0 else 0)
        count = min(count, self.char_count)
        if count >= self.char_count:
            self.typing_done = True
        return count

    def fade_out(self, dt):
        """Fully fade out (for section breaks)."""
        self.alpha = max(0, self.alpha - 400 * dt)
        return self.alpha <= 0

    def draw(self, song_time):
        if self.is_active and not self.typing_done:
            visible = self.get_visible_char_count(song_time)
            draw_typing_text(self.text, visible, self.font,
                             self.color, self.alpha, self.y_pos)
        else:
            draw_text_simple(self.text, self.font, self.color, self.alpha, self.y_pos)


# --- Load and play ---
pygame.mixer.music.load("Don't Leave/Don't Leave.mp3")
pygame.mixer.music.play(start=SONG_START)

# --- State ---
display_lines = []          
next_lyric_index = 0        
next_y = START_Y            
clearing_lines = []         

# --- Main Loop ---
running = True

while running:
    dt = clock.tick(60) / 1000.0  # delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    song_time = get_song_time()

    # End condition
    if song_time == -1 or song_time > lyrics[-1][1] + 2.0:
        running = False
        break

    # --- Trigger new lyrics ---
    while next_lyric_index < len(lyrics):
        start, end, text, style = lyrics[next_lyric_index]

        if song_time >= start:
            if style == "section" and text == "---SECTION---":
                clearing_lines.extend(display_lines)
                display_lines = []
                next_y = START_Y
                next_lyric_index += 1
                continue

            # Mark previous active lines as inactive (dim them)
            for line in display_lines:
                line.is_active = False

            # Add new line
            new_line = DisplayLine(text, style, next_y, start, end, is_active=True)
            display_lines.append(new_line)
            next_y += LINE_HEIGHT

            # If too many lines, start fading oldest
            if len(display_lines) > MAX_VISIBLE_LINES:
                oldest = display_lines.pop(0)
                clearing_lines.append(oldest)

            next_lyric_index += 1
        else:
            break

    # Update visible lines
    for line in display_lines:
        line.update(dt)

    # Update clearing lines (fade them out)
    clearing_lines = [l for l in clearing_lines if not l.fade_out(dt)]

    # --- Draw ---
    screen.fill(BG_COLOR)

    # Draw clearing (fading) lines
    for line in clearing_lines:
        line.draw(song_time)

    # Draw active display lines
    for line in display_lines:
        line.draw(song_time)

    # Draw section label
    if next_lyric_index > 0:
        # Figure out which section we're in
        section_name = ""
        for i in range(next_lyric_index - 1, -1, -1):
            s, e, t, st = lyrics[i]
            if st == "section":
                if song_time < 128:
                    section_name = "Pre-Chorus"
                elif song_time < 141:
                    section_name = "Bridge"
                else:
                    section_name = "Chorus"
                break
        # Also check if we haven't hit a section marker yet
        if not section_name and song_time < 128:
            section_name = "Pre-Chorus"

        if section_name:
            label_surf = FONT_SECTION.render(f"— {section_name} —", True, SECTION_COLOR)
            label_surf.set_alpha(120)
            label_rect = label_surf.get_rect(center=(WIDTH // 2, 30))
            screen.blit(label_surf, label_rect)

    pygame.display.flip()

# --- Final fade to black  ---
all_lines = display_lines + clearing_lines
fade_frames = 90  # 1.5 sec at 60fps

for i in range(fade_frames):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    progress = i / fade_frames  
    screen.fill(BG_COLOR)

    # Fade all lyrics uniformly
    for line in all_lines:
        line.alpha = max(0, 255 * (1.0 - progress))
        line.typing_done = True  # show full text during fade-out
        line.draw(song_time if song_time > 0 else 999)

    # Fade section label too
    if section_name:
        label_surf = FONT_SECTION.render(f"— {section_name} —", True, SECTION_COLOR)
        label_surf.set_alpha(max(0, int(120 * (1.0 - progress))))
        label_rect = label_surf.get_rect(center=(WIDTH // 2, 30))
        screen.blit(label_surf, label_rect)

    # Black overlay on top for extra smooth fade
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(int(255 * progress))
    screen.blit(overlay, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.fadeout(500)
pygame.time.wait(600)
pygame.quit()
sys.exit()
