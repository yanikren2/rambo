import pygame
import random
import os
import sys
from pygame.locals import *

# Pygame başlat
pygame.init()
pygame.mixer.init()  # Ses için

# Ekran ayarları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gelişmiş Yılan Oyunu")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

# Font ayarları
font_large = pygame.font.SysFont("comicsansms", 48)
font_medium = pygame.font.SysFont("comicsansms", 36)
font_small = pygame.font.SysFont("comicsansms", 24)

# Oyun sabitler
FPS = 12
BLOCK_SIZE = 20

# Görsellerin yükleneceği klasör
IMAGES_FOLDER = "images"

# Görseller için bir sözlük oluşturalım - bunları açıklamalar içinde tanımlıyoruz, siz kendi klasörünüze ekleyeceksiniz
images = {
    "snake_head": None,  # "snake_head.png" dosyasını ekleyeceksiniz
    "snake_body": None,  # "snake_body.png" dosyasını ekleyeceksiniz
    "normal_food": None,  # "food.png" dosyasını ekleyeceksiniz
    "big_food": None,  # "big_food.png" dosyasını ekleyeceksiniz
    "background": None,  # "background.png" dosyasını ekleyeceksiniz
    "menu_bg": None  # "menu_bg.png" dosyasını ekleyeceksiniz
}

# Sesler
sounds = {
    "eat": None,  # "eat.wav" dosyasını ekleyeceksiniz
    "game_over": None,  # "game_over.wav" dosyasını ekleyeceksiniz
    "big_eat": None  # "big_eat.wav" dosyasını ekleyeceksiniz
}


def load_images():
    """Görselleri yükle"""
    global images

    # Görsel klasörünün var olup olmadığını kontrol et
    if not os.path.exists(IMAGES_FOLDER):
        os.makedirs(IMAGES_FOLDER)
        print(f"'{IMAGES_FOLDER}' klasörü oluşturuldu. Lütfen oyun görsellerini buraya ekleyin.")

    # Görselleri yüklemeyi dene
    try:
        for key in images.keys():
            file_path = os.path.join(IMAGES_FOLDER, f"{key}.png")
            if os.path.exists(file_path):
                # Görseli yükle ve doğru boyuta getir
                if key == "background" or key == "menu_bg":
                    images[key] = pygame.image.load(file_path).convert()
                    images[key] = pygame.transform.scale(images[key], (WIDTH, HEIGHT))
                elif key == "big_food":
                    images[key] = pygame.image.load(file_path).convert_alpha()
                    images[key] = pygame.transform.scale(images[key], (BLOCK_SIZE * 2, BLOCK_SIZE * 2))
                else:
                    images[key] = pygame.image.load(file_path).convert_alpha()
                    images[key] = pygame.transform.scale(images[key], (BLOCK_SIZE, BLOCK_SIZE))
            else:
                print(f"{file_path} bulunamadı. Varsayılan şekiller kullanılacak.")
    except Exception as e:
        print(f"Görselleri yüklerken hata oluştu: {e}")


def load_sounds():
    """Sesleri yükle"""
    global sounds

    # Ses klasörünün var olup olmadığını kontrol et
    sounds_folder = "sounds"
    if not os.path.exists(sounds_folder):
        os.makedirs(sounds_folder)
        print(f"'{sounds_folder}' klasörü oluşturuldu. Lütfen oyun seslerini buraya ekleyin.")

    # Sesleri yüklemeyi dene
    try:
        for key in sounds.keys():
            file_path = os.path.join(sounds_folder, f"{key}.wav")
            if os.path.exists(file_path):
                sounds[key] = pygame.mixer.Sound(file_path)
            else:
                print(f"{file_path} bulunamadı.")
    except Exception as e:
        print(f"Sesleri yüklerken hata oluştu: {e}")


class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (BLOCK_SIZE, 0)  # Başlangıçta sağa doğru hareket
        self.grow_pending = 0
        self.score = 0
        self.speed = FPS

    def move(self):
        """Yılanı hareket ettir"""
        head_x, head_y = self.body[0]
        dx, dy = self.direction

        # Yeni baş pozisyonu (ekran kenarlarından geçiş yapabilmesi için)
        new_head = ((head_x + dx) % WIDTH, (head_y + dy) % HEIGHT)

        # Yeni başı ekle
        self.body.insert(0, new_head)

        # Eğer büyüme beklemedeyse, kuyruğu silme
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        """Yılanı büyüt"""
        self.grow_pending += amount

    def check_collision(self):
        """Yılanın kendisiyle çarpışıp çarpışmadığını kontrol et"""
        return self.body[0] in self.body[1:]

    def draw(self, surface):
        """Yılanı çiz"""
        # Baş
        if images["snake_head"]:
            # Yönüne göre başın açısını hesapla
            angle = 0
            if self.direction == (BLOCK_SIZE, 0):  # Sağ
                angle = 0
            elif self.direction == (-BLOCK_SIZE, 0):  # Sol
                angle = 180
            elif self.direction == (0, -BLOCK_SIZE):  # Yukarı
                angle = 90
            elif self.direction == (0, BLOCK_SIZE):  # Aşağı
                angle = 270

            # Dönmüş görüntüyü oluştur
            rotated_head = pygame.transform.rotate(images["snake_head"], angle)
            surface.blit(rotated_head, self.body[0])
        else:
            # Görseller yoksa basit çizim kullan
            pygame.draw.rect(surface, GREEN, pygame.Rect(self.body[0], (BLOCK_SIZE, BLOCK_SIZE)))

        # Gövde
        for segment in self.body[1:]:
            if images["snake_body"]:
                surface.blit(images["snake_body"], segment)
            else:
                pygame.draw.rect(surface, GREEN, pygame.Rect(segment, (BLOCK_SIZE, BLOCK_SIZE)))


class Food:
    def __init__(self, is_big=False):
        self.position = self.generate_position()
        self.is_big = is_big
        self.lifetime = 300 if is_big else -1  # Büyük yemler sınırlı süre kalır (-1: sonsuz)

    def generate_position(self):
        """Rastgele bir konumda yem oluştur"""
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        return (x, y)

    def draw(self, surface):
        """Yemi çiz"""
        if self.is_big:
            if images["big_food"]:
                surface.blit(images["big_food"], self.position)
            else:
                pygame.draw.rect(surface, GOLD, pygame.Rect(self.position, (BLOCK_SIZE * 2, BLOCK_SIZE * 2)))
        else:
            if images["normal_food"]:
                surface.blit(images["normal_food"], self.position)
            else:
                pygame.draw.rect(surface, RED, pygame.Rect(self.position, (BLOCK_SIZE, BLOCK_SIZE)))

    def update(self):
        """Yaşam süresini güncelle"""
        if self.is_big and self.lifetime > 0:
            self.lifetime -= 1
            return self.lifetime > 0
        return True


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.reset()
        self.state = "menu"  # "menu", "game", "gameover", "help"
        self.high_score = self.load_high_score()

    def reset(self):
        """Oyunu sıfırla"""
        self.snake = Snake()
        self.foods = [Food()]  # Normal yemle başla
        self.big_food_timer = random.randint(500, 1000)  # Büyük yem için zamanlayıcı
        self.paused = False

    def load_high_score(self):
        """Yüksek skoru yükle"""
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        """Yüksek skoru kaydet"""
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def check_food_collision(self):
        """Yem çarpışmalarını kontrol et"""
        head_rect = pygame.Rect(self.snake.body[0], (BLOCK_SIZE, BLOCK_SIZE))

        for i, food in enumerate(self.foods[:]):
            food_size = (BLOCK_SIZE * 2, BLOCK_SIZE * 2) if food.is_big else (BLOCK_SIZE, BLOCK_SIZE)
            food_rect = pygame.Rect(food.position, food_size)

            if head_rect.colliderect(food_rect):
                # Yem yeme
                if food.is_big:
                    # Büyük yem: +5 puan, +3 büyüme
                    self.snake.score += 5
                    self.snake.grow(3)
                    if sounds["big_eat"]:
                        sounds["big_eat"].play()
                else:
                    # Normal yem: +1 puan, +1 büyüme
                    self.snake.score += 1
                    self.snake.grow(1)
                    if sounds["eat"]:
                        sounds["eat"].play()

                # Yemi kaldır ve yeni yem ekle
                self.foods.pop(i)
                self.foods.append(Food())

                # Skora göre hızı artır (maksimum 20 FPS'ye kadar)
                self.snake.speed = min(FPS + self.snake.score // 10, 20)

                # Yüksek skoru güncelle
                if self.snake.score > self.high_score:
                    self.high_score = self.snake.score
                    self.save_high_score()

                return True

        return False

    def update(self):
        """Oyunu güncelle"""
        if self.state == "game" and not self.paused:
            # Yılanı hareket ettir
            self.snake.move()

            # Kendisiyle çarpışma kontrolü
            if self.snake.check_collision():
                self.state = "gameover"
                if sounds["game_over"]:
                    sounds["game_over"].play()
                return

            # Yem çarpışma kontrolü
            self.check_food_collision()

            # Yemleri güncelle
            for i, food in enumerate(self.foods[:]):
                if not food.update():
                    self.foods.pop(i)

            # Büyük yem oluşturma zamanlayıcısını güncelle
            if self.big_food_timer > 0:
                self.big_food_timer -= 1
                if self.big_food_timer == 0:
                    # Eğer zaten büyük yem yoksa ekle
                    if not any(food.is_big for food in self.foods):
                        self.foods.append(Food(is_big=True))
                    self.big_food_timer = random.randint(500, 1000)  # Zamanlayıcıyı sıfırla

    def draw(self):
        """Oyunu ekrana çiz"""
        # Arkaplan
        if self.state in ["menu", "help"] and images["menu_bg"]:
            screen.blit(images["menu_bg"], (0, 0))
        elif images["background"]:
            screen.blit(images["background"], (0, 0))
        else:
            screen.fill(BLACK)

        if self.state == "menu":
            self.draw_menu()
        elif self.state == "help":
            self.draw_help()
        elif self.state == "game":
            # Yemleri çiz
            for food in self.foods:
                food.draw(screen)

            # Yılanı çiz
            self.snake.draw(screen)

            # Skoru çiz
            score_text = font_small.render(f"Skor: {self.snake.score} | Rekor: {self.high_score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            # Duraklatma bildirimi
            if self.paused:
                pause_text = font_medium.render("DURAKLADI - Devam etmek için P'ye basın", True, WHITE)
                text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(pause_text, text_rect)
        elif self.state == "gameover":
            self.draw_game_over()

    def draw_menu(self):
        """Ana menüyü çiz"""
        title = font_large.render("YILAN OYUNU", True, WHITE)
        start = font_medium.render("1. Oyuna Başla", True, WHITE)
        help_text = font_medium.render("2. Nasıl Oynanır", True, WHITE)
        quit_text = font_medium.render("3. Çıkış", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(start, (WIDTH // 2 - start.get_width() // 2, 250))
        screen.blit(help_text, (WIDTH // 2 - help_text.get_width() // 2, 300))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 350))

    def draw_help(self):
        """Yardım ekranını çiz"""
        title = font_medium.render("NASIL OYNANIR", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        help_lines = [
            "- Yılanı yön tuşlarıyla hareket ettir",
            "- Normal yemler 1 puan ve 1 büyüme sağlar",
            "- Altın büyük yemler 5 puan ve 3 büyüme sağlar",
            "- Büyük yemler sınırlı süre boyunca ekranda kalır",
            "- Kendine veya duvarlara çarpma - oyun biter",
            "- P tuşu ile oyunu duraklatabilirsin",
            "",
            "ESC tuşuna basarak menüye dönebilirsin"
        ]

        for i, line in enumerate(help_lines):
            line_text = font_small.render(line, True, WHITE)
            screen.blit(line_text, (100, 150 + i * 40))

    def draw_game_over(self):
        """Oyun bitti ekranını çiz"""
        gameover_text = font_large.render("OYUN BİTTİ", True, RED)
        score_text = font_medium.render(f"Skorun: {self.snake.score}", True, WHITE)
        restart_text = font_medium.render("Yeniden başlamak için BOŞLUK'a bas", True, WHITE)
        menu_text = font_medium.render("Menüye dönmek için ESC'ye bas", True, WHITE)

        screen.blit(gameover_text, (WIDTH // 2 - gameover_text.get_width() // 2, 150))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 250))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 350))
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, 400))

    def handle_events(self):
        """Olayları işle"""
        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            elif event.type == KEYDOWN:
                if self.state == "menu":
                    if event.key == K_1:
                        self.reset()
                        self.state = "game"
                    elif event.key == K_2:
                        self.state = "help"
                    elif event.key == K_3 or event.key == K_ESCAPE:
                        return False

                elif self.state == "help":
                    if event.key == K_ESCAPE:
                        self.state = "menu"

                elif self.state == "game":
                    if event.key == K_p:
                        self.paused = not self.paused
                    elif event.key == K_ESCAPE:
                        self.state = "menu"

                    # Yön tuşları
                    if not self.paused:
                        if event.key == K_UP and self.snake.direction != (0, BLOCK_SIZE):
                            self.snake.direction = (0, -BLOCK_SIZE)
                        elif event.key == K_DOWN and self.snake.direction != (0, -BLOCK_SIZE):
                            self.snake.direction = (0, BLOCK_SIZE)
                        elif event.key == K_LEFT and self.snake.direction != (BLOCK_SIZE, 0):
                            self.snake.direction = (-BLOCK_SIZE, 0)
                        elif event.key == K_RIGHT and self.snake.direction != (-BLOCK_SIZE, 0):
                            self.snake.direction = (BLOCK_SIZE, 0)

                elif self.state == "gameover":
                    if event.key == K_SPACE:
                        self.reset()
                        self.state = "game"
                    elif event.key == K_ESCAPE:
                        self.state = "menu"

        return True

    def run(self):
        """Ana oyun döngüsü"""
        running = True
        while running:
            running = self.handle_events()

            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(self.snake.speed if self.state == "game" else FPS)


# Ana çalıştırma kodu
if __name__ == "__main__":
    # Görselleri ve sesleri yükle
    load_images()
    load_sounds()

    # Oyunu başlat
    game = Game()
    game.run()

    # Pygame'i kapat
    pygame.quit()
    sys.exit()