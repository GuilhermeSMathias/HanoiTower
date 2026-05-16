# ─────────────────────────────────────────────
#  Constantes visuais do pygame
# ─────────────────────────────────────────────

# Dimensões da janela
W, H = 900, 650
FPS = 60
FOOTER_H = 90

# Cores
BG = (15, 12, 30)
PEG_COL = (60, 55, 90)
BASE_COL = (40, 36, 70)
TEXT_COL = (220, 210, 255)
ACCENT = (130, 100, 240)
WIN_COL = (80, 220, 140)
LOSE_COL = (240, 80, 80)

DISK_COLORS = [
    (255, 99, 132), (255, 159, 64), (255, 205, 86),
    (75, 192, 192), (54, 162, 235), (153, 102, 255),
    (201, 203, 207), (255, 140, 50), (100, 220, 120),
    (220, 100, 180),
]

# Layout centralizado
CENTER_X = W // 2
PEG_SPACING = 260

PEG_X = [
    CENTER_X - PEG_SPACING,
    CENTER_X,
    CENTER_X + PEG_SPACING
]

BASE_Y = H - FOOTER_H - 100

PEG_H = 320
PEG_W = 14
BASE_W = 220
BASE_H = 18

DISK_H = 26
MAX_DISK_W = 180
MIN_DISK_W = 46
DISK_GAP = 4
