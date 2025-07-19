import pygame
import random

# Inisialisasi pygame
pygame.init()

# Ukuran layar
screen_width = 1000  # Lebih lebar untuk 20 keping
screen_height = 600  # Sesuaikan tinggi layar
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Puzzle Game')

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Muat gambar
image = pygame.image.load('image.jpg')  # Pastikan nama gambar benar
piece_width = image.get_width() // 5  # Membagi lebar menjadi 5 bagian
piece_height = image.get_height() // 4  # Membagi tinggi menjadi 4 bagian

# Potong gambar menjadi 20 bagian (5x4 grid)
pieces = []
for i in range(4):  # 4 baris
    for j in range(5):  # 5 kolom
        piece = image.subsurface(j * piece_width, i * piece_height, piece_width, piece_height)
        pieces.append(piece)

# Mengacak posisi potongan gambar
random.shuffle(pieces)

# Posisi awal setiap potongan puzzle (menggunakan posisi 5x4 grid)
positions = []
for i in range(4):
    for j in range(5):
        x = j * piece_width
        y = i * piece_height
        positions.append([x, y])  # Gunakan list agar bisa diubah

# Kecepatan pergerakan
move_speed = 10
zoom_factor = 1  # Faktor untuk memperbesar ukuran puzzle
max_zoom = 2  # Batas maksimum pembesaran
min_zoom = 1  # Batas minimum pembesaran

# Font untuk menambahkan nomor atau simbol
font = pygame.font.SysFont('Arial', 30)

# Variabel untuk drag-and-drop
dragging = False
dragged_piece_index = None
offset_x = 0
offset_y = 0

# Fungsi untuk memeriksa apakah puzzle sudah selesai
def check_solution():
    for idx, pos in enumerate(positions):
        correct_x = (idx % 5) * piece_width
        correct_y = (idx // 5) * piece_height
        if pos != [correct_x, correct_y]:
            return False
    return True

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Memeriksa apakah mouse mengklik potongan puzzle
            mouse_x, mouse_y = event.pos
            for idx, pos in enumerate(positions):
                x, y = pos
                # Jika mouse mengklik potongan puzzle
                if x <= mouse_x <= x + piece_width and y <= mouse_y <= y + piece_height:
                    dragging = True
                    dragged_piece_index = idx
                    offset_x = mouse_x - x
                    offset_y = mouse_y - y
                    break
        
        elif event.type == pygame.MOUSEBUTTONUP:
            # Lepaskan potongan puzzle yang sedang di-drag
            dragging = False
            dragged_piece_index = None

        elif event.type == pygame.MOUSEMOTION:
            # Seret potongan puzzle dengan mouse
            if dragging:
                mouse_x, mouse_y = event.pos
                positions[dragged_piece_index][0] = mouse_x - offset_x
                positions[dragged_piece_index][1] = mouse_y - offset_y

    # Menangani input pergerakan (kiri, kanan, atas, bawah)
    keys = pygame.key.get_pressed()

    # Mengisi layar dengan warna putih
    screen.fill(WHITE)

    # Menampilkan potongan-potongan puzzle pada posisi yang sesuai
    for idx, piece in enumerate(pieces):
        x, y = positions[idx]
        # Perbesar atau perkecil ukuran potongan puzzle
        resized_piece = pygame.transform.scale(piece, (int(piece_width * zoom_factor), int(piece_height * zoom_factor)))
        
        # Menampilkan nomor atau simbol pada tiap potongan
        num_text = font.render(str(idx+1), True, BLACK)
        text_rect = num_text.get_rect(center=(x + piece_width // 2, y + piece_height // 2))
        
        # Tempelkan gambar potongan puzzle
        screen.blit(resized_piece, (x, y))
        # Tempelkan nomor atau simbol pada potongan puzzle
        screen.blit(num_text, text_rect)

    # Mengecek apakah puzzle sudah selesai
    if check_solution():
        win_text = font.render("Puzzle Selesai!", True, BLACK)
        screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2))

    # Update tampilan layar
    pygame.display.flip()

# Keluar dari pygame
pygame.quit()