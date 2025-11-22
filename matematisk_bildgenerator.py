"""
MATEMATISK BILDGENERATOR - Exakt rendering med matplotlib
För Matematik 3c-hemsidan

Detta skript skapar matematiskt korrekta figurer programmatiskt,
INTE med AI-bildgenerering.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch, Polygon, Wedge
from matplotlib.transforms import Affine2D

# Konfigurera matplotlib för svenska tecken
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

def create_triangle_areasatsen(filename='areasatsen_korrekt.png'):
    """
    Skapar en pedagogisk figur för areasatsen.
    A = 1/2 * a * b * sin(C)
    """
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)

    # Definiera triangelns hörn (exakta koordinater)
    A = np.array([2, 6])
    B = np.array([10, 1])
    C = np.array([1, 1])

    # Rita triangeln
    triangle = Polygon([A, B, C], fill=True, alpha=0.4,
                      edgecolor='#2563EB', facecolor='#93C5FD', linewidth=3)
    ax.add_patch(triangle)

    # Rita hörn (röda punkter)
    for point, label, offset in [(A, 'A', (0, 0.4)), (B, 'B', (0.3, 0)), (C, 'C', (-0.5, 0))]:
        ax.plot(*point, 'o', color='#DC2626', markersize=12, zorder=5)
        ax.text(point[0] + offset[0], point[1] + offset[1], label,
               fontsize=20, fontweight='bold', ha='center', va='center')

    # Märk sidorna
    mid_AB = (A + B) / 2
    mid_BC = (B + C) / 2
    mid_CA = (C + A) / 2

    ax.text(mid_AB[0] + 0.5, mid_AB[1] + 0.3, 'c', fontsize=16,
           style='italic', color='#1E40AF')
    ax.text(mid_BC[0], mid_BC[1] - 0.5, 'a', fontsize=16,
           style='italic', color='#1E40AF')
    ax.text(mid_CA[0] - 0.5, mid_CA[1] + 0.3, 'b', fontsize=16,
           style='italic', color='#1E40AF')

    # Rita vinkelbåge vid C (KORREKT!)
    angle_C_start = np.degrees(np.arctan2(A[1] - C[1], A[0] - C[0]))
    angle_C_end = np.degrees(np.arctan2(B[1] - C[1], B[0] - C[0]))

    arc_C = Arc(C, 1.2, 1.2, angle=0, theta1=angle_C_end, theta2=angle_C_start,
               color='#B45309', linewidth=2.5)
    ax.add_patch(arc_C)

    # Märk vinkeln C
    angle_mid = (angle_C_start + angle_C_end) / 2
    label_x = C[0] + 0.8 * np.cos(np.radians(angle_mid))
    label_y = C[1] + 0.8 * np.sin(np.radians(angle_mid))
    ax.text(label_x, label_y, 'C', fontsize=16, fontweight='bold', color='#92400E')

    # Formeln
    formula_text = r'$A = \frac{1}{2} \cdot a \cdot b \cdot \sin(C)$'
    ax.text(5.5, -1, formula_text, fontsize=22, ha='center',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='#FEF3C7',
                    edgecolor='#F59E0B', linewidth=2))

    # Exempel
    example_text = 'Exempel:\n' + r'$a = 8, b = 12, C = 45°$' + '\n' + r'$A \approx 33.9$ cm²'
    ax.text(10, 8, example_text, fontsize=14, ha='left', va='top',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#ECFDF5',
                    edgecolor='#10B981', linewidth=1.5))

    # Anpassningar
    ax.set_xlim(-0.5, 12)
    ax.set_ylim(-2, 8.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Areasatsen', fontsize=24, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Areasatsen-figur sparad: {filename}')
    return filename


def create_triangle_sinussatsen(filename='sinussatsen_korrekt.png'):
    """
    Skapar en pedagogisk figur för sinussatsen.
    a/sin(A) = b/sin(B) = c/sin(C)
    """
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)

    # Definiera triangelns hörn
    A = np.array([6, 7])
    B = np.array([10, 1])
    C = np.array([1, 1])

    # Rita triangeln
    triangle = Polygon([A, B, C], fill=True, alpha=0.4,
                      edgecolor='#2563EB', facecolor='#93C5FD', linewidth=3)
    ax.add_patch(triangle)

    # Rita höjd från A till BC
    foot_x = A[0]
    foot_y = C[1]
    ax.plot([A[0], foot_x], [A[1], foot_y], 'r--', linewidth=2, label='Höjd')

    # Märk höjden
    ax.text(foot_x + 0.3, (A[1] + foot_y) / 2, 'h', fontsize=16,
           style='italic', color='#DC2626')

    # Rita hörn
    for point, label, offset in [(A, 'A', (0, 0.5)), (B, 'B', (0.3, 0)), (C, 'C', (-0.5, 0))]:
        ax.plot(*point, 'o', color='#DC2626', markersize=12, zorder=5)
        ax.text(point[0] + offset[0], point[1] + offset[1], label,
               fontsize=20, fontweight='bold', ha='center')

    # Märk sidorna
    mid_AB = (A + B) / 2
    mid_BC = (B + C) / 2
    mid_CA = (C + A) / 2

    ax.text(mid_BC[0], mid_BC[1] - 0.5, 'a', fontsize=16, style='italic', color='#1E40AF')
    ax.text(mid_CA[0] - 0.6, mid_CA[1], 'b', fontsize=16, style='italic', color='#1E40AF')
    ax.text(mid_AB[0] + 0.4, mid_AB[1], 'c', fontsize=16, style='italic', color='#1E40AF')

    # Vinkelbågar vid alla hörn
    # Vinkel vid A
    angle_A_start = np.degrees(np.arctan2(C[1] - A[1], C[0] - A[0]))
    angle_A_end = np.degrees(np.arctan2(B[1] - A[1], B[0] - A[0]))
    arc_A = Arc(A, 1, 1, angle=0, theta1=angle_A_start, theta2=angle_A_end,
               color='#B45309', linewidth=2.5)
    ax.add_patch(arc_A)

    # Vinkel vid B
    angle_B_start = np.degrees(np.arctan2(A[1] - B[1], A[0] - B[0]))
    angle_B_end = np.degrees(np.arctan2(C[1] - B[1], C[0] - B[0]))
    arc_B = Arc(B, 1, 1, angle=0, theta1=angle_B_start, theta2=angle_B_end,
               color='#B45309', linewidth=2.5)
    ax.add_patch(arc_B)

    # Vinkel vid C
    angle_C_start = np.degrees(np.arctan2(A[1] - C[1], A[0] - C[0]))
    angle_C_end = np.degrees(np.arctan2(B[1] - C[1], B[0] - C[0]))
    arc_C = Arc(C, 1, 1, angle=0, theta1=angle_C_end, theta2=angle_C_start,
               color='#B45309', linewidth=2.5)
    ax.add_patch(arc_C)

    # Formeln
    formula_text = r'$\frac{a}{\sin(A)} = \frac{b}{\sin(B)} = \frac{c}{\sin(C)}$'
    ax.text(5.5, -1.5, formula_text, fontsize=22, ha='center',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='#FEF3C7',
                    edgecolor='#F59E0B', linewidth=2))

    # Exempel
    example_text = 'Exempel:\n' + r'$A = 30°, B = 45°, c = 10$ cm' + '\n' + r'Bestäm $b$' + '\n' + r'$b = 10 \cdot \frac{\sin(45°)}{\sin(30°)} \approx 14.1$ cm'
    ax.text(10.5, 7.5, example_text, fontsize=13, ha='left', va='top',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#ECFDF5',
                    edgecolor='#10B981', linewidth=1.5))

    ax.set_xlim(-0.5, 12)
    ax.set_ylim(-3, 8.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Sinussatsen', fontsize=24, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Sinussatsen-figur sparad: {filename}')
    return filename


def create_triangle_cosinussatsen(filename='cosinussatsen_korrekt.png'):
    """
    Skapar en pedagogisk figur för cosinussatsen.
    a² = b² + c² - 2bc·cos(A)
    """
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)

    # Definiera triangelns hörn
    A = np.array([2, 6])
    B = np.array([10, 1])
    C = np.array([1, 1])

    # Rita triangeln
    triangle = Polygon([A, B, C], fill=True, alpha=0.4,
                      edgecolor='#2563EB', facecolor='#93C5FD', linewidth=3)
    ax.add_patch(triangle)

    # Rita hörn
    for point, label, offset in [(A, 'A', (0, 0.5)), (B, 'B', (0.3, 0)), (C, 'C', (-0.5, 0))]:
        ax.plot(*point, 'o', color='#DC2626', markersize=12, zorder=5)
        ax.text(point[0] + offset[0], point[1] + offset[1], label,
               fontsize=20, fontweight='bold', ha='center')

    # Märk sidorna
    mid_AB = (A + B) / 2
    mid_BC = (B + C) / 2
    mid_CA = (C + A) / 2

    # a = motstående sida till A (BC)
    ax.text(mid_BC[0], mid_BC[1] - 0.5, 'a', fontsize=16, style='italic', color='#1E40AF')
    # b = motstående sida till B (AC)
    ax.text(mid_CA[0] - 0.5, mid_CA[1] + 0.3, 'b', fontsize=16, style='italic', color='#1E40AF')
    # c = motstående sida till C (AB)
    ax.text(mid_AB[0] + 0.5, mid_AB[1] + 0.3, 'c', fontsize=16, style='italic', color='#1E40AF')

    # Rita vinkelbåge vid A (fokusvinkel för formeln)
    angle_A_start = np.degrees(np.arctan2(C[1] - A[1], C[0] - A[0]))
    angle_A_end = np.degrees(np.arctan2(B[1] - A[1], B[0] - A[0]))

    arc_A = Arc(A, 1.2, 1.2, angle=0, theta1=angle_A_start, theta2=angle_A_end,
               color='#EF4444', linewidth=3)
    ax.add_patch(arc_A)

    # Märk vinkeln A (röd för att framhäva)
    angle_mid = (angle_A_start + angle_A_end) / 2
    label_x = A[0] + 0.7 * np.cos(np.radians(angle_mid))
    label_y = A[1] + 0.7 * np.sin(np.radians(angle_mid))
    ax.text(label_x, label_y, 'A', fontsize=16, fontweight='bold', color='#DC2626')

    # Formeln
    formula_text = r'$a^2 = b^2 + c^2 - 2bc \cdot \cos(A)$'
    ax.text(5.5, -1, formula_text, fontsize=22, ha='center',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='#FEF3C7',
                    edgecolor='#F59E0B', linewidth=2))

    # Exempel
    example_text = 'Exempel:\n' + r'$b = 5, c = 7, A = 60°$' + '\n' + r'$a^2 = 25 + 49 - 2·5·7·\cos(60°)$' + '\n' + r'$a^2 = 74 - 35 = 39$' + '\n' + r'$a \approx 6.2$ cm'
    ax.text(10, 8, example_text, fontsize=13, ha='left', va='top',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#ECFDF5',
                    edgecolor='#10B981', linewidth=1.5))

    ax.set_xlim(-0.5, 12)
    ax.set_ylim(-2, 8.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Cosinussatsen', fontsize=24, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Cosinussatsen-figur sparad: {filename}')
    return filename


def create_derivative_secant(filename='sekant_korrekt.png'):
    """
    Skapar figur för sekantens lutning.
    """
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)

    # Funktion
    x = np.linspace(-1, 5, 400)
    y = 0.3 * x**2 - 0.5 * x + 2

    ax.plot(x, y, 'b-', linewidth=2.5, label=r'$f(x)$')

    # Två punkter på kurvan
    x1, x2 = 1, 3.5
    y1 = 0.3 * x1**2 - 0.5 * x1 + 2
    y2 = 0.3 * x2**2 - 0.5 * x2 + 2

    # Sekantlinjen
    ax.plot([x1, x2], [y1, y2], 'r-', linewidth=2, label='Sekant')
    ax.plot([x1, x2], [y1, y2], 'ro', markersize=10)

    # Märk punkterna
    ax.text(x1, y1 - 0.5, f'$(x_1, f(x_1))$', fontsize=12, ha='center')
    ax.text(x2, y2 + 0.5, f'$(x_2, f(x_2))$', fontsize=12, ha='center')

    # Lutning
    slope = (y2 - y1) / (x2 - x1)
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    ax.text(mid_x, mid_y - 1, f'Lutning = {slope:.2f}', fontsize=14,
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    ax.set_title('Sekantens lutning', fontsize=18, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.5, 5)
    ax.set_ylim(0, 6)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Sekant-figur sparad: {filename}')
    return filename


# ============================================================================
# VIKTIGA FIGURER (8 st)
# ============================================================================

def create_kap1_01_brakforkortning(filename='kap1-01-brakforkortning.png'):
    """Skapar figur för algebraisk bråkförkortning"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Titel
    ax.text(5, 9.5, 'Bråkförkortning', fontsize=24, fontweight='bold', ha='center')

    # Exempel 1: Numeriskt
    ax.text(5, 8.3, 'Exempel 1: Numeriskt', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=2))

    ax.text(2.5, 7.2, r'$\frac{12}{18}$', fontsize=36, ha='center')
    ax.text(3.8, 7.2, '=', fontsize=36, ha='center')
    ax.text(5, 7.2, r'$\frac{6 \cdot 2}{6 \cdot 3}$', fontsize=36, ha='center')
    ax.text(6.8, 7.2, '=', fontsize=36, ha='center')
    ax.text(7.8, 7.2, r'$\frac{2}{3}$', fontsize=36, ha='center')

    # Förklaring
    ax.text(5, 6.2, 'Förkortning med 6', fontsize=14, ha='center', style='italic', color='#0284C7')

    # Exempel 2: Algebraiskt
    ax.text(5, 5.3, 'Exempel 2: Algebraiskt', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=2))

    ax.text(2, 4.2, r'$\frac{x^2 - 4}{x + 2}$', fontsize=36, ha='center')
    ax.text(3.5, 4.2, '=', fontsize=36, ha='center')
    ax.text(5, 4.2, r'$\frac{(x-2)(x+2)}{x+2}$', fontsize=36, ha='center')
    ax.text(7, 4.2, '=', fontsize=36, ha='center')
    ax.text(8, 4.2, r'$x - 2$', fontsize=36, ha='center')

    # Förklaring
    ax.text(5, 3, 'Faktorisera och förkorta gemensam faktor', fontsize=14, ha='center',
           style='italic', color='#D97706')

    # Exempel 3: Mer komplext
    ax.text(5, 2.2, 'Exempel 3: Mer komplext', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#ECFDF5', edgecolor='#10B981', linewidth=2))

    ax.text(2.5, 1.1, r'$\frac{2x^2 + 4x}{2x}$', fontsize=36, ha='center')
    ax.text(4, 1.1, '=', fontsize=36, ha='center')
    ax.text(5.5, 1.1, r'$\frac{2x(x+2)}{2x}$', fontsize=36, ha='center')
    ax.text(7, 1.1, '=', fontsize=36, ha='center')
    ax.text(8, 1.1, r'$x + 2$', fontsize=36, ha='center')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap1_02_brakaddition(filename='kap1-02-brakaddition.png'):
    """Skapar figur för bråkaddition och subtraktion"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Titel
    ax.text(5, 9.5, 'Bråkaddition och subtraktion', fontsize=24, fontweight='bold', ha='center')

    # Regel
    ax.text(5, 8.7, 'Grundregel: Hitta gemensam nämnare', fontsize=16, ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=2))

    # Exempel 1: Enkel addition
    ax.text(5, 7.8, 'Exempel 1: Addition', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=2))

    ax.text(2, 6.8, r'$\frac{1}{3} + \frac{1}{4}$', fontsize=32, ha='center')
    ax.text(3.2, 6.8, '=', fontsize=32, ha='center')
    ax.text(4.5, 6.8, r'$\frac{4}{12} + \frac{3}{12}$', fontsize=32, ha='center')
    ax.text(6.2, 6.8, '=', fontsize=32, ha='center')
    ax.text(7.2, 6.8, r'$\frac{7}{12}$', fontsize=32, ha='center')

    ax.text(5, 6, 'Gemensam nämnare: 12', fontsize=14, ha='center', style='italic', color='#0284C7')

    # Exempel 2: Algebraisk addition
    ax.text(5, 5.2, 'Exempel 2: Algebraiskt', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#ECFDF5', edgecolor='#10B981', linewidth=2))

    ax.text(2, 4.2, r'$\frac{2}{x} + \frac{3}{y}$', fontsize=32, ha='center')
    ax.text(3.5, 4.2, '=', fontsize=32, ha='center')
    ax.text(5.5, 4.2, r'$\frac{2y + 3x}{xy}$', fontsize=32, ha='center')

    ax.text(5, 3.4, 'Gemensam nämnare: xy', fontsize=14, ha='center', style='italic', color='#10B981')

    # Exempel 3: Subtraktion med variabler
    ax.text(5, 2.6, 'Exempel 3: Subtraktion', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=2))

    ax.text(1.5, 1.6, r'$\frac{1}{x-1} - \frac{2}{x+1}$', fontsize=28, ha='center')
    ax.text(3.5, 1.6, '=', fontsize=28, ha='center')
    ax.text(5.5, 1.6, r'$\frac{(x+1) - 2(x-1)}{(x-1)(x+1)}$', fontsize=28, ha='center')
    ax.text(8, 1.6, '=', fontsize=28, ha='center')

    ax.text(5, 0.7, r'$= \frac{x+1-2x+2}{(x-1)(x+1)} = \frac{-x+3}{x^2-1}$',
           fontsize=24, ha='center')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap2_03_derivata_definition(filename='kap2-03-derivata-definition.png'):
    """Skapar figur för derivatans formella definition"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Titel
    ax.text(5, 9.5, 'Derivatans definition', fontsize=24, fontweight='bold', ha='center')

    # Definition box
    ax.text(5, 8.5, 'Formell definition:', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=2))

    # Huvudformeln
    formula = r"$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$"
    ax.text(5, 7.3, formula, fontsize=40, ha='center',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=3))

    # Förklaringar
    ax.text(5, 6.2, 'Tolkning:', fontsize=16, fontweight='bold', ha='center')

    ax.text(1, 5.5, r'$\bullet$', fontsize=20, ha='center')
    ax.text(1.5, 5.5, r'$h$ är en liten förändring i $x$', fontsize=14, ha='left')

    ax.text(1, 5, r'$\bullet$', fontsize=20, ha='center')
    ax.text(1.5, 5, r'$f(x+h) - f(x)$ är förändring i $y$', fontsize=14, ha='left')

    ax.text(1, 4.5, r'$\bullet$', fontsize=20, ha='center')
    ax.text(1.5, 4.5, r'$\frac{f(x+h) - f(x)}{h}$ är differenskvoten', fontsize=14, ha='left')

    ax.text(1, 4, r'$\bullet$', fontsize=20, ha='center')
    ax.text(1.5, 4, r'$\lim_{h \to 0}$ betyder att $h$ går mot noll', fontsize=14, ha='left')

    # Exempel
    ax.text(5, 3.2, 'Exempel: Beräkna derivatan av ' + r'$f(x) = x^2$',
           fontsize=16, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#ECFDF5', edgecolor='#10B981', linewidth=2))

    ax.text(5, 2.5, r"$f'(x) = \lim_{h \to 0} \frac{(x+h)^2 - x^2}{h}$", fontsize=22, ha='center')

    ax.text(5, 1.9, r"$= \lim_{h \to 0} \frac{x^2 + 2xh + h^2 - x^2}{h}$", fontsize=22, ha='center')

    ax.text(5, 1.3, r"$= \lim_{h \to 0} \frac{2xh + h^2}{h}$", fontsize=22, ha='center')

    ax.text(5, 0.7, r"$= \lim_{h \to 0} (2x + h) = 2x$", fontsize=22, ha='center')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap2_04_derivering_exempel(filename='kap2-04-derivering-exempel.png'):
    """Skapar figur för derivering steg-för-steg"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Titel
    ax.text(5, 9.5, 'Derivering steg-för-steg', fontsize=24, fontweight='bold', ha='center')

    # Potensregeln
    ax.text(5, 8.7, 'Potensregeln:', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=2))

    ax.text(5, 7.9, r"$(x^n)' = n \cdot x^{n-1}$", fontsize=32, ha='center',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=2))

    # Exempel 1
    ax.text(5, 7, 'Exempel 1:', fontsize=16, fontweight='bold', ha='center')
    ax.text(2.5, 6.3, r"$f(x) = x^3$", fontsize=28, ha='center')
    ax.text(4, 6.3, r'$\Rightarrow$', fontsize=28, ha='center')
    ax.text(6, 6.3, r"$f'(x) = 3x^2$", fontsize=28, ha='center')

    # Exempel 2
    ax.text(5, 5.5, 'Exempel 2:', fontsize=16, fontweight='bold', ha='center')
    ax.text(2.5, 4.8, r"$f(x) = 5x^4$", fontsize=28, ha='center')
    ax.text(4, 4.8, r'$\Rightarrow$', fontsize=28, ha='center')
    ax.text(6, 4.8, r"$f'(x) = 20x^3$", fontsize=28, ha='center')

    # Exempel 3 - Mer komplext
    ax.text(5, 4, 'Exempel 3: Flera termer', fontsize=16, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#ECFDF5', edgecolor='#10B981', linewidth=2))

    ax.text(5, 3.3, r"$f(x) = 3x^4 - 2x^3 + 5x^2 - 7x + 4$", fontsize=24, ha='center')

    ax.text(5, 2.5, 'Derivera varje term:', fontsize=14, ha='center', style='italic')

    ax.text(5, 1.9, r"$f'(x) = 12x^3 - 6x^2 + 10x - 7$", fontsize=24, ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF9C3', edgecolor='#EAB308', linewidth=2))

    # Notering
    ax.text(5, 1.1, 'Observera: Konstanten 4 försvinner!', fontsize=14, ha='center',
           style='italic', color='#DC2626')
    ax.text(5, 0.6, r"$(c)' = 0$ där $c$ är en konstant", fontsize=14, ha='center')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap3_02_produktregeln(filename='kap3-02-produktregeln.png'):
    """Skapar figur för produktregeln visualiserad"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Titel
    ax.text(5, 9.5, 'Produktregeln', fontsize=24, fontweight='bold', ha='center')

    # Formeln
    ax.text(5, 8.7, 'Om ' + r"$f(x) = u(x) \cdot v(x)$" + ' då:', fontsize=16, ha='center')

    formula = r"$f'(x) = u'(x) \cdot v(x) + u(x) \cdot v'(x)$"
    ax.text(5, 7.8, formula, fontsize=36, ha='center',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=3))

    # Geometrisk tolkning
    ax.text(5, 6.8, 'Geometrisk tolkning: Area av rektangel', fontsize=16, fontweight='bold',
           ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#E0F2FE',
                                 edgecolor='#0284C7', linewidth=2))

    # Rita rektangel
    u_len = 3
    v_len = 2
    du_len = 0.8
    dv_len = 0.6

    start_x = 2
    start_y = 4

    # Original rektangel (u × v)
    rect1 = patches.Rectangle((start_x, start_y), u_len, v_len,
                              linewidth=3, edgecolor='#2563EB', facecolor='#93C5FD', alpha=0.6)
    ax.add_patch(rect1)
    ax.text(start_x + u_len/2, start_y + v_len/2, r'$u \cdot v$',
           fontsize=20, ha='center', fontweight='bold')

    # Ökning i u (u' × v)
    rect2 = patches.Rectangle((start_x + u_len, start_y), du_len, v_len,
                              linewidth=3, edgecolor='#DC2626', facecolor='#FCA5A5', alpha=0.6)
    ax.add_patch(rect2)
    ax.text(start_x + u_len + du_len/2, start_y + v_len/2, r"$u' \cdot v$",
           fontsize=16, ha='center', fontweight='bold')

    # Ökning i v (u × v')
    rect3 = patches.Rectangle((start_x, start_y + v_len), u_len, dv_len,
                              linewidth=3, edgecolor='#059669', facecolor='#86EFAC', alpha=0.6)
    ax.add_patch(rect3)
    ax.text(start_x + u_len/2, start_y + v_len + dv_len/2, r"$u \cdot v'$",
           fontsize=16, ha='center', fontweight='bold')

    # Liten hörnbit (försumbar i gränsvärdet)
    rect4 = patches.Rectangle((start_x + u_len, start_y + v_len), du_len, dv_len,
                              linewidth=2, edgecolor='gray', facecolor='lightgray', alpha=0.4)
    ax.add_patch(rect4)

    # Märk sidorna
    ax.text(start_x + u_len/2, start_y - 0.3, r'$u$', fontsize=18, ha='center',
           style='italic', color='#2563EB')
    ax.text(start_x - 0.3, start_y + v_len/2, r'$v$', fontsize=18, ha='center',
           style='italic', color='#2563EB')

    # Exempel
    ax.text(5, 2.5, 'Exempel:', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#ECFDF5', edgecolor='#10B981', linewidth=2))

    ax.text(5, 1.9, r"$f(x) = x^2 \cdot e^x$", fontsize=24, ha='center')
    ax.text(5, 1.4, r"$f'(x) = 2x \cdot e^x + x^2 \cdot e^x$", fontsize=24, ha='center')
    ax.text(5, 0.9, r"$= e^x(2x + x^2)$", fontsize=24, ha='center')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap3_05_kedjeregeln(filename='kap3-05-kedjeregeln.png'):
    """Skapar figur för kedjeregeln steg-för-steg"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Titel
    ax.text(5, 9.5, 'Kedjeregeln', fontsize=24, fontweight='bold', ha='center')

    # Formeln
    ax.text(5, 8.7, 'Om ' + r"$f(x) = g(h(x))$" + ' då:', fontsize=16, ha='center')

    formula = r"$f'(x) = g'(h(x)) \cdot h'(x)$"
    ax.text(5, 7.8, formula, fontsize=36, ha='center',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=3))

    # Minnesstrategi
    ax.text(5, 6.9, 'Minnesregel: "Yttre derivatan × inre derivatan"', fontsize=14,
           ha='center', style='italic', color='#D97706')

    # Exempel 1
    ax.text(5, 6.2, 'Exempel 1:', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=2))

    ax.text(5, 5.6, r"$f(x) = (x^2 + 1)^3$", fontsize=24, ha='center')
    ax.text(5, 5.1, 'Steg 1: Identifiera yttre och inre funktion', fontsize=12, ha='center', style='italic')
    ax.text(5, 4.7, r"Yttre: $g(u) = u^3$, Inre: $h(x) = x^2 + 1$", fontsize=14, ha='center')
    ax.text(5, 4.3, 'Steg 2: Derivera båda', fontsize=12, ha='center', style='italic')
    ax.text(5, 3.9, r"$g'(u) = 3u^2$, $h'(x) = 2x$", fontsize=14, ha='center')
    ax.text(5, 3.5, 'Steg 3: Använd kedjeregeln', fontsize=12, ha='center', style='italic')
    ax.text(5, 3, r"$f'(x) = 3(x^2+1)^2 \cdot 2x = 6x(x^2+1)^2$", fontsize=22, ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF9C3', edgecolor='#EAB308', linewidth=2))

    # Exempel 2
    ax.text(5, 2.2, 'Exempel 2:', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#ECFDF5', edgecolor='#10B981', linewidth=2))

    ax.text(5, 1.6, r"$f(x) = e^{2x^2}$", fontsize=24, ha='center')
    ax.text(5, 1.1, r"$f'(x) = e^{2x^2} \cdot 4x = 4xe^{2x^2}$", fontsize=22, ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF9C3', edgecolor='#EAB308', linewidth=2))

    ax.text(5, 0.5, r"Yttre: $e^u$, Inre: $2x^2$ (derivata: $4x$)",
           fontsize=12, ha='center', style='italic')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap4_02_derivata_nollstallen(filename='kap4-02-derivata-nollstallen.png'):
    """Skapar figur för derivatans nollställen (graf med f och f')"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), dpi=300)

    # Funktion
    x = np.linspace(-3, 3, 500)
    f = x**3 - 3*x
    f_prime = 3*x**2 - 3

    # Graf 1: f(x)
    ax1.plot(x, f, 'b-', linewidth=3, label=r"$f(x) = x^3 - 3x$")
    ax1.axhline(y=0, color='k', linestyle='--', linewidth=1, alpha=0.3)
    ax1.axvline(x=0, color='k', linestyle='--', linewidth=1, alpha=0.3)

    # Markera extrempunkter
    x_max = -1
    x_min = 1
    ax1.plot(x_max, x_max**3 - 3*x_max, 'ro', markersize=12, label='Maximum')
    ax1.plot(x_min, x_min**3 - 3*x_min, 'go', markersize=12, label='Minimum')

    ax1.set_xlabel('x', fontsize=14)
    ax1.set_ylabel('y', fontsize=14)
    ax1.set_title(r"Funktionen $f(x)$", fontsize=18, fontweight='bold')
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-5, 5)

    # Graf 2: f'(x)
    ax2.plot(x, f_prime, 'r-', linewidth=3, label=r"$f'(x) = 3x^2 - 3$")
    ax2.axhline(y=0, color='k', linestyle='-', linewidth=2, alpha=0.5)
    ax2.axvline(x=0, color='k', linestyle='--', linewidth=1, alpha=0.3)

    # Markera nollställen
    ax2.plot(x_max, 0, 'ro', markersize=12, label='Nollställe (maximum)')
    ax2.plot(x_min, 0, 'go', markersize=12, label='Nollställe (minimum)')

    # Annotationer
    ax2.text(-1, -1.5, r'$f\'(x) < 0$' + '\n(fallande)', fontsize=12, ha='center',
            bbox=dict(boxstyle='round', facecolor='#FEE2E2', alpha=0.8))
    ax2.text(0, 2, r'$f\'(x) > 0$' + '\n(växande)', fontsize=12, ha='center',
            bbox=dict(boxstyle='round', facecolor='#DCFCE7', alpha=0.8))
    ax2.text(1, -1.5, r'$f\'(x) < 0$' + '\n(fallande)', fontsize=12, ha='center',
            bbox=dict(boxstyle='round', facecolor='#FEE2E2', alpha=0.8))

    ax2.set_xlabel('x', fontsize=14)
    ax2.set_ylabel("y", fontsize=14)
    ax2.set_title(r"Derivatan $f'(x)$ - nollställen visar extrempunkter",
                 fontsize=18, fontweight='bold')
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-4, 6)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap5_01_primitiv_funktion(filename='kap5-01-primitiv-funktion.png'):
    """Skapar figur för primitiv funktion (graf med f och F)"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), dpi=300)

    # Funktion och primitiv
    x = np.linspace(0, 4, 500)
    f = 2*x  # f(x) = 2x
    F = x**2  # F(x) = x^2 (primitiv funktion)

    # Graf 1: f(x)
    ax1.plot(x, f, 'r-', linewidth=3, label=r"$f(x) = 2x$")
    ax1.axhline(y=0, color='k', linestyle='--', linewidth=1, alpha=0.3)
    ax1.axvline(x=0, color='k', linestyle='--', linewidth=1, alpha=0.3)
    ax1.fill_between(x[100:300], 0, f[100:300], alpha=0.3, color='red',
                     label='Area = integral')

    ax1.set_xlabel('x', fontsize=14)
    ax1.set_ylabel('y', fontsize=14)
    ax1.set_title(r"Funktionen $f(x) = 2x$", fontsize=18, fontweight='bold')
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-1, 9)

    # Graf 2: F(x)
    ax2.plot(x, F, 'b-', linewidth=3, label=r"$F(x) = x^2$ (primitiv funktion)")
    ax2.axhline(y=0, color='k', linestyle='--', linewidth=1, alpha=0.3)
    ax2.axvline(x=0, color='k', linestyle='--', linewidth=1, alpha=0.3)

    # Markera lutningen vid några punkter
    for x_point in [1, 2, 3]:
        slope = 2*x_point  # f(x_point)
        y_point = x_point**2
        dx = 0.4
        ax2.plot([x_point - dx, x_point + dx],
                [y_point - slope*dx, y_point + slope*dx],
                'r--', linewidth=2, alpha=0.7)
        ax2.plot(x_point, y_point, 'ro', markersize=8)
        ax2.text(x_point, y_point - 1.5, f"Lutning = {slope}",
                fontsize=10, ha='center',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

    ax2.set_xlabel('x', fontsize=14)
    ax2.set_ylabel('y', fontsize=14)
    ax2.set_title(r"Primitiv funktion $F(x)$ där $F'(x) = f(x)$",
                 fontsize=18, fontweight='bold')
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-1, 17)

    # Förklaring
    ax2.text(2, 15, r"$F'(x) = f(x)$", fontsize=20, ha='center',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#FEF3C7',
                     edgecolor='#F59E0B', linewidth=2))

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


# ============================================================================
# ÖNSKVÄRDA FIGURER (16 st)
# ============================================================================

def create_kap1_03_brak_multiplikation(filename='kap1-03-brak-multiplikation.png'):
    """Skapar figur för multiplikation och division av bråk"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Titel
    ax.text(5, 9.5, 'Multiplikation och division av bråk', fontsize=24, fontweight='bold', ha='center')

    # Multiplikation
    ax.text(5, 8.7, 'Multiplikation:', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=2))

    ax.text(5, 7.9, r'$\frac{a}{b} \cdot \frac{c}{d} = \frac{a \cdot c}{b \cdot d}$',
           fontsize=32, ha='center',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=2))

    # Exempel multiplikation
    ax.text(5, 7, 'Exempel:', fontsize=16, fontweight='bold', ha='center')
    ax.text(2.5, 6.3, r'$\frac{2}{3} \cdot \frac{5}{7}$', fontsize=28, ha='center')
    ax.text(3.8, 6.3, '=', fontsize=28, ha='center')
    ax.text(5.5, 6.3, r'$\frac{10}{21}$', fontsize=28, ha='center')

    # Division
    ax.text(5, 5.3, 'Division:', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#ECFDF5', edgecolor='#10B981', linewidth=2))

    ax.text(5, 4.5, r'$\frac{a}{b} \div \frac{c}{d} = \frac{a}{b} \cdot \frac{d}{c} = \frac{a \cdot d}{b \cdot c}$',
           fontsize=28, ha='center',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=2))

    ax.text(5, 3.6, 'Minnesregel: Vänd och multiplicera!', fontsize=14, ha='center',
           style='italic', color='#059669')

    # Exempel division
    ax.text(5, 3, 'Exempel:', fontsize=16, fontweight='bold', ha='center')
    ax.text(2, 2.3, r'$\frac{3}{4} \div \frac{2}{5}$', fontsize=28, ha='center')
    ax.text(3.5, 2.3, '=', fontsize=28, ha='center')
    ax.text(5, 2.3, r'$\frac{3}{4} \cdot \frac{5}{2}$', fontsize=28, ha='center')
    ax.text(6.5, 2.3, '=', fontsize=28, ha='center')
    ax.text(7.8, 2.3, r'$\frac{15}{8}$', fontsize=28, ha='center')

    # Algebraiskt exempel
    ax.text(5, 1.4, 'Algebraiskt exempel:', fontsize=16, fontweight='bold', ha='center')
    ax.text(2, 0.7, r'$\frac{x}{y} \cdot \frac{y^2}{x^2}$', fontsize=24, ha='center')
    ax.text(3.5, 0.7, '=', fontsize=24, ha='center')
    ax.text(5, 0.7, r'$\frac{xy^2}{x^2y}$', fontsize=24, ha='center')
    ax.text(6.5, 0.7, '=', fontsize=24, ha='center')
    ax.text(7.5, 0.7, r'$\frac{y}{x}$', fontsize=24, ha='center')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap2_02_tangent_lutning(filename='kap2-02-tangent-lutning.png'):
    """Skapar förbättrad figur för tangentens lutning"""
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)

    # Funktion
    x = np.linspace(-1, 5, 400)
    y = 0.3 * x**2 - 0.5 * x + 2

    ax.plot(x, y, 'b-', linewidth=3, label=r'$f(x) = 0.3x^2 - 0.5x + 2$')

    # Punkt på kurvan
    x0 = 2.5
    y0 = 0.3 * x0**2 - 0.5 * x0 + 2

    # Derivata (lutning)
    slope = 2 * 0.3 * x0 - 0.5

    # Tangentlinjen
    x_tangent = np.linspace(0.5, 4.5, 100)
    y_tangent = slope * (x_tangent - x0) + y0

    ax.plot(x_tangent, y_tangent, 'r-', linewidth=2.5, label='Tangent')
    ax.plot(x0, y0, 'ro', markersize=12, zorder=5)

    # Märk punkten
    ax.text(x0, y0 + 0.6, f'$(x_0, f(x_0))$', fontsize=14, ha='center',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

    # Lutning annotation
    ax.text(3.5, 3.5, f"Lutning = f'(x₀) = {slope:.2f}", fontsize=14,
           bbox=dict(boxstyle='round', facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=2))

    # Rita lutningstriangel
    dx = 1
    dy = slope * dx
    ax.plot([x0, x0 + dx, x0 + dx], [y0, y0, y0 + dy], 'k--', linewidth=1.5, alpha=0.7)
    ax.text(x0 + dx/2, y0 - 0.3, r'$\Delta x$', fontsize=12, ha='center')
    ax.text(x0 + dx + 0.3, y0 + dy/2, r'$\Delta y$', fontsize=12, ha='center')

    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    ax.set_title('Tangentens lutning = Derivatan', fontsize=18, fontweight='bold')
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.5, 5)
    ax.set_ylim(0, 6)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap2_05_deriverbarhet_absolutbelopp(filename='kap2-05-deriverbarhet-absolutbelopp.png'):
    """Skapar figur för deriverbarhet och absolutbelopp"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

    # Graf 1: Deriverbar funktion
    x1 = np.linspace(-3, 3, 400)
    y1 = x1**2

    ax1.plot(x1, y1, 'b-', linewidth=3, label=r'$f(x) = x^2$')
    ax1.axhline(y=0, color='k', linestyle='--', linewidth=1, alpha=0.3)
    ax1.axvline(x=0, color='k', linestyle='--', linewidth=1, alpha=0.3)
    ax1.plot(0, 0, 'go', markersize=12, label='Deriverbar vid x=0')

    ax1.set_xlabel('x', fontsize=14)
    ax1.set_ylabel('y', fontsize=14)
    ax1.set_title('Deriverbar funktion', fontsize=16, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-1, 9)

    # Graf 2: Ej deriverbar (absolutbelopp)
    x2 = np.linspace(-3, 3, 400)
    y2 = np.abs(x2)

    ax2.plot(x2, y2, 'r-', linewidth=3, label=r'$f(x) = |x|$')
    ax2.axhline(y=0, color='k', linestyle='--', linewidth=1, alpha=0.3)
    ax2.axvline(x=0, color='k', linestyle='--', linewidth=1, alpha=0.3)
    ax2.plot(0, 0, 'rx', markersize=15, markeredgewidth=3, label='EJ deriverbar vid x=0')

    # Visa vänster- och högerlutning
    ax2.plot([-2, 0], [2, 0], 'b--', linewidth=2, alpha=0.7, label='Vänster: lutning = -1')
    ax2.plot([0, 2], [0, 2], 'g--', linewidth=2, alpha=0.7, label='Höger: lutning = +1')

    ax2.set_xlabel('x', fontsize=14)
    ax2.set_ylabel('y', fontsize=14)
    ax2.set_title('Ej deriverbar vid "knäck"', fontsize=16, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-1, 3)

    plt.suptitle('Deriverbarhet', fontsize=20, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap3_03_potensfunktioner(filename='kap3-03-potensfunktioner.png'):
    """Skapar figur för derivata av potensfunktioner"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Titel
    ax.text(5, 9.5, 'Derivata av potensfunktioner', fontsize=24, fontweight='bold', ha='center')

    # Huvudregel
    ax.text(5, 8.7, r"$(x^n)' = n \cdot x^{n-1}$", fontsize=36, ha='center',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=3))

    # Exempel tabell
    examples = [
        (r'$x^5$', r'$5x^4$'),
        (r'$x^{-2}$', r'$-2x^{-3} = \frac{-2}{x^3}$'),
        (r'$\sqrt{x} = x^{1/2}$', r'$\frac{1}{2}x^{-1/2} = \frac{1}{2\sqrt{x}}$'),
        (r'$\frac{1}{x} = x^{-1}$', r'$-x^{-2} = \frac{-1}{x^2}$'),
        (r'$x^{3/2}$', r'$\frac{3}{2}x^{1/2}$'),
    ]

    y_pos = 7.5
    ax.text(3, y_pos, 'Funktion f(x)', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=2))
    ax.text(7, y_pos, "Derivata f'(x)", fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#ECFDF5', edgecolor='#10B981', linewidth=2))

    y_pos -= 0.7
    for func, deriv in examples:
        ax.text(3, y_pos, func, fontsize=20, ha='center')
        ax.text(5, y_pos, r'$\Rightarrow$', fontsize=20, ha='center')
        ax.text(7, y_pos, deriv, fontsize=20, ha='center')
        y_pos -= 0.9

    # Speciella fall
    ax.text(5, 1.2, 'Observera:', fontsize=16, fontweight='bold', ha='center')
    ax.text(5, 0.7, r'$(c)^\prime = 0$ (konstant)', fontsize=14, ha='center')
    ax.text(5, 0.3, r'$(cx^n)^\prime = cn \cdot x^{n-1}$ (konstant faktor)', fontsize=14, ha='center')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap3_06_tillampningar_derivata(filename='kap3-06-tillampningar-derivata.png'):
    """Skapar figur för tillämpningar av derivata"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)

    # Läge-tid graf
    t = np.linspace(0, 10, 500)
    s = 2*t**2 + 3*t + 1  # Läge
    v = 4*t + 3  # Hastighet (derivata)

    ax.plot(t, s, 'b-', linewidth=3, label=r'Läge: $s(t) = 2t^2 + 3t + 1$')

    # Markera några punkter och deras hastigheter
    for t_point in [2, 4, 6]:
        s_point = 2*t_point**2 + 3*t_point + 1
        v_point = 4*t_point + 3

        # Tangentlinje
        dt = 0.8
        ax.plot([t_point - dt, t_point + dt],
               [s_point - v_point*dt, s_point + v_point*dt],
               'r--', linewidth=2, alpha=0.7)

        ax.plot(t_point, s_point, 'ro', markersize=10)
        ax.text(t_point, s_point + 15, f'v = {v_point} m/s',
               fontsize=11, ha='center',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

    ax.set_xlabel('Tid t (s)', fontsize=14)
    ax.set_ylabel('Läge s (m)', fontsize=14)
    ax.set_title('Tillämpning: Hastighet som derivata av läge', fontsize=18, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)

    # Formel box
    ax.text(7, 30, r"$v(t) = s'(t) = 4t + 3$", fontsize=18, ha='center',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#FEF3C7',
                    edgecolor='#F59E0B', linewidth=2))

    ax.text(7, 15, 'Hastighet = lutning\npå läge-tid-kurvan', fontsize=12, ha='center',
           style='italic')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap4_05_andraderivata(filename='kap4-05-andraderivata.png'):
    """Skapar figur för andraderivatan och lokala extrempunkter"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Titel
    ax.text(5, 9.5, 'Andraderivatan och extrempunkter', fontsize=24, fontweight='bold', ha='center')

    # Test för extrempunkter
    ax.text(5, 8.7, 'Test för lokala extrempunkter:', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=2))

    # Villkor
    ax.text(5, 8, r"1. Hitta kritiska punkter där $f'(x) = 0$", fontsize=16, ha='center')

    ax.text(5, 7.4, r"2. Använd andraderivatan $f''(x)$:", fontsize=16, ha='center')

    # Maximum
    ax.text(5, 6.7, 'Maximum:', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=2))
    ax.text(5, 6.1, r"$f'(x_0) = 0$ och $f''(x_0) < 0$", fontsize=20, ha='center')
    ax.text(5, 5.6, '(Kurvan böjer nedåt)', fontsize=14, ha='center', style='italic', color='#DC2626')

    # Rita max-kurva
    x_max = np.linspace(1, 3, 100)
    y_max = -0.5 * (x_max - 2)**2 + 5
    ax.plot(x_max, y_max, 'r-', linewidth=3)
    ax.plot(2, 5, 'ro', markersize=12)
    ax.annotate('', xy=(2.5, 4.9), xytext=(2.5, 4.4),
               arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.annotate('', xy=(1.5, 4.9), xytext=(1.5, 4.4),
               arrowprops=dict(arrowstyle='->', color='red', lw=2))

    # Minimum
    ax.text(5, 3.7, 'Minimum:', fontsize=18, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#DCFCE7', edgecolor='#059669', linewidth=2))
    ax.text(5, 3.1, r"$f'(x_0) = 0$ och $f''(x_0) > 0$", fontsize=20, ha='center')
    ax.text(5, 2.6, '(Kurvan böjer uppåt)', fontsize=14, ha='center', style='italic', color='#059669')

    # Rita min-kurva
    x_min = np.linspace(6.5, 8.5, 100)
    y_min = 0.5 * (x_min - 7.5)**2 + 1.8
    ax.plot(x_min, y_min, 'g-', linewidth=3)
    ax.plot(7.5, 1.8, 'go', markersize=12)
    ax.annotate('', xy=(8, 1.9), xytext=(8, 2.4),
               arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.annotate('', xy=(7, 1.9), xytext=(7, 2.4),
               arrowprops=dict(arrowstyle='->', color='green', lw=2))

    # Notering
    ax.text(5, 0.8, r"Om $f''(x_0) = 0$ är testet oklart", fontsize=14, ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEFCE8', edgecolor='#EAB308', linewidth=2))

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap4_06_extremvardesproblem(filename='kap4-06-extremvardesproblem.png'):
    """Skapar figur för extremvärdesproblem exempel"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)

    # Problem: Maximera area av rektangel med given omkrets
    # Omkrets = 40, sidor x och y
    # 2x + 2y = 40 => y = 20 - x
    # Area A = xy = x(20-x) = 20x - x^2

    x = np.linspace(0, 20, 500)
    A = 20*x - x**2

    ax.plot(x, A, 'b-', linewidth=3, label=r'Area: $A(x) = 20x - x^2$')
    ax.axhline(y=0, color='k', linestyle='--', linewidth=1, alpha=0.3)

    # Maximum vid x = 10
    x_max = 10
    A_max = 100
    ax.plot(x_max, A_max, 'ro', markersize=15, label=f'Maximum: x = {x_max}, A = {A_max}')

    # Tangent vid maximum
    ax.plot([5, 15], [A_max, A_max], 'r--', linewidth=2, alpha=0.7)

    ax.set_xlabel('Sidlängd x (m)', fontsize=14)
    ax.set_ylabel('Area A (m²)', fontsize=14)
    ax.set_title('Extremvärdesproblem: Maximera rektangelns area', fontsize=18, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 20)
    ax.set_ylim(-10, 110)

    # Problem och lösning
    problem_text = 'Problem:\nEn rektangel har omkrets 40 m.\nVilka sidor ger maximal area?'
    ax.text(3, 80, problem_text, fontsize=12, ha='left',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#FEF3C7',
                    edgecolor='#F59E0B', linewidth=2))

    solution_text = "Lösning:\n" + r"$A(x) = x(20-x) = 20x - x^2$" + "\n" + r"$A'(x) = 20 - 2x = 0$" + "\n" + r"$x = 10$ m, $y = 10$ m" + "\nMaximal area: 100 m²"
    ax.text(15, 80, solution_text, fontsize=12, ha='left',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#ECFDF5',
                    edgecolor='#10B981', linewidth=2))

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap5_02_primitiva_villkor(filename='kap5-02-primitiva-villkor.png'):
    """Skapar figur för primitiva funktioner med villkor"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)

    # Flera primitiva funktioner (skiljer sig med konstant)
    x = np.linspace(0, 5, 500)
    f = 2*x  # Derivata

    for C in [-2, 0, 2, 4]:
        F = x**2 + C
        ax.plot(x, F, linewidth=2.5, label=f'$F(x) = x^2 + {C}$' if C >= 0 else f'$F(x) = x^2 {C}$')

    # Markera en specifik primitiv med villkor
    x0, y0 = 2, 6
    ax.plot(x0, y0, 'ro', markersize=12, zorder=5)
    ax.text(x0, y0 + 1.5, f'Villkor: F({x0}) = {y0}', fontsize=14, ha='center',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))

    # C = y0 - x0^2 = 6 - 4 = 2
    ax.plot([0, 5], [2, 27], 'r-', linewidth=3.5, alpha=0.7, label='F(x) med villkor')

    ax.axhline(y=0, color='k', linestyle='--', linewidth=1, alpha=0.3)
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    ax.set_title('Primitiva funktioner: Oändligt många lösningar', fontsize=18, fontweight='bold')
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-5, 30)

    # Förklaring
    explanation = r"Om $F'(x) = f(x)$ så är $F(x) + C$ också en primitiv funktion" + "\n" + "Villkor bestämmer konstanten C"
    ax.text(3.5, 20, explanation, fontsize=13, ha='center',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#FEF3C7',
                    edgecolor='#F59E0B', linewidth=2))

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap5_04_fundamentalsats(filename='kap5-04-fundamentalsats.png'):
    """Skapar figur för integralkalkylens fundamentalsats"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)

    # Funktion
    x = np.linspace(0, 5, 500)
    f = 2*x

    ax.plot(x, f, 'r-', linewidth=3, label=r'$f(x) = 2x$')

    # Intervall [a, b]
    a, b = 1, 4
    x_fill = np.linspace(a, b, 300)
    f_fill = 2*x_fill
    ax.fill_between(x_fill, 0, f_fill, alpha=0.4, color='blue', label='Area = Integral')

    # Markera gränser
    ax.axvline(x=a, color='g', linestyle='--', linewidth=2, label=f'a = {a}')
    ax.axvline(x=b, color='purple', linestyle='--', linewidth=2, label=f'b = {b}')
    ax.plot([a, b], [2*a, 2*b], 'ko', markersize=10)

    ax.axhline(y=0, color='k', linestyle='-', linewidth=1.5)
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    ax.set_title('Integralkalkylens fundamentalsats', fontsize=20, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 11)

    # Fundamentalsatsen
    formula = r"$\int_a^b f(x) \, dx = F(b) - F(a)$"
    ax.text(2.5, 9, formula, fontsize=28, ha='center',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='#FEF3C7',
                    edgecolor='#F59E0B', linewidth=3))

    # Beräkning
    calc_text = r"Exempel: $\int_1^4 2x \, dx = [x^2]_1^4 = 16 - 1 = 15$"
    ax.text(2.5, 7, calc_text, fontsize=18, ha='center',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#ECFDF5',
                    edgecolor='#10B981', linewidth=2))

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap5_07_tillampningar_integral(filename='kap5-07-tillampningar-integral.png'):
    """Skapar figur för tillämpningar av integraler"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)

    # Hastighet över tid
    t = np.linspace(0, 5, 500)
    v = 10 + 2*t  # Hastighet

    ax.plot(t, v, 'b-', linewidth=3, label=r'Hastighet: $v(t) = 10 + 2t$ m/s')

    # Area under kurvan = sträcka
    t_fill = np.linspace(1, 4, 300)
    v_fill = 10 + 2*t_fill
    ax.fill_between(t_fill, 0, v_fill, alpha=0.4, color='green', label='Area = Sträcka')

    # Markera intervall
    ax.axvline(x=1, color='r', linestyle='--', linewidth=2)
    ax.axvline(x=4, color='r', linestyle='--', linewidth=2)

    ax.axhline(y=0, color='k', linestyle='-', linewidth=1.5)
    ax.set_xlabel('Tid t (s)', fontsize=14)
    ax.set_ylabel('Hastighet v (m/s)', fontsize=14)
    ax.set_title('Tillämpning: Sträcka som integral av hastighet', fontsize=18, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 22)

    # Beräkning
    calc_text = r"Sträcka: $s = \int_1^4 (10 + 2t) \, dt$" + "\n" + r"$= [10t + t^2]_1^4 = (40 + 16) - (10 + 1) = 45$ m"
    ax.text(2.5, 17, calc_text, fontsize=16, ha='center',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#FEF3C7',
                    edgecolor='#F59E0B', linewidth=2))

    # Princip
    principle = 'Integral av hastighet = Sträcka\nIntegral av acceleration = Hastighet'
    ax.text(2.5, 3, principle, fontsize=13, ha='center', style='italic',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#E0F2FE',
                    edgecolor='#0284C7', linewidth=2))

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap6_01_trigonometri_triangel(filename='kap6-01-trigonometri-triangel.png'):
    """Skapar figur för trigonometri i rätvinkliga trianglar"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    # Rätvinklig triangel
    A = np.array([2, 2])
    B = np.array([8, 2])
    C = np.array([8, 6])

    triangle = Polygon([A, B, C], fill=True, alpha=0.4,
                      edgecolor='#2563EB', facecolor='#93C5FD', linewidth=3)
    ax.add_patch(triangle)

    # Räta vinkeln
    square_size = 0.4
    square = patches.Rectangle((B[0] - square_size, B[1]), square_size, square_size,
                               linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(square)

    # Hörn
    ax.plot(*A, 'o', color='#DC2626', markersize=12, zorder=5)
    ax.plot(*B, 'o', color='#DC2626', markersize=12, zorder=5)
    ax.plot(*C, 'o', color='#DC2626', markersize=12, zorder=5)

    ax.text(A[0] - 0.4, A[1], 'A', fontsize=20, fontweight='bold', ha='right')
    ax.text(B[0] + 0.4, B[1] - 0.4, 'B (90°)', fontsize=20, fontweight='bold', ha='left')
    ax.text(C[0] + 0.4, C[1], 'C', fontsize=20, fontweight='bold', ha='left')

    # Märk sidorna
    ax.text(5, 1.5, 'b (närliggande)', fontsize=16, ha='center', color='#1E40AF', style='italic')
    ax.text(8.7, 4, 'a (motstående)', fontsize=16, ha='left', color='#DC2626', style='italic')
    ax.text(4.5, 4.5, 'c (hypotenusa)', fontsize=16, ha='center', color='#059669', style='italic')

    # Vinkel vid A
    angle_arc = Arc(A, 1.2, 1.2, angle=0, theta1=0, theta2=np.degrees(np.arctan(4/6)),
                   color='#B45309', linewidth=3)
    ax.add_patch(angle_arc)
    ax.text(A[0] + 0.8, A[1] + 0.3, r'$\alpha$', fontsize=18, fontweight='bold', color='#92400E')

    # Formler
    y_pos = 8.5
    ax.text(5, y_pos, 'Trigonometriska förhållanden:', fontsize=18, fontweight='bold', ha='center')

    y_pos -= 0.7
    formulas = [
        r'$\sin(\alpha) = \frac{\text{motstående}}{\text{hypotenusa}} = \frac{a}{c}$',
        r'$\cos(\alpha) = \frac{\text{närliggande}}{\text{hypotenusa}} = \frac{b}{c}$',
        r'$\tan(\alpha) = \frac{\text{motstående}}{\text{närliggande}} = \frac{a}{b}$'
    ]

    colors = ['#FEE2E2', '#E0F2FE', '#FEF3C7']
    edge_colors = ['#DC2626', '#0284C7', '#F59E0B']

    for formula, color, edge_color in zip(formulas, colors, edge_colors):
        ax.text(5, y_pos, formula, fontsize=18, ha='center',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=color, edgecolor=edge_color, linewidth=2))
        y_pos -= 0.7

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap6_03_enhetscirkel(filename='kap6-03-enhetscirkel.png'):
    """Skapar figur för trigonometriska ekvationer på enhetscirkel"""
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')

    # Enhetscirkel
    circle = plt.Circle((0, 0), 1, fill=False, color='#2563EB', linewidth=3)
    ax.add_patch(circle)

    # Axlar
    ax.axhline(y=0, color='k', linestyle='-', linewidth=1.5)
    ax.axvline(x=0, color='k', linestyle='-', linewidth=1.5)
    ax.text(1.3, 0.1, 'x', fontsize=16, fontweight='bold')
    ax.text(0.1, 1.3, 'y', fontsize=16, fontweight='bold')

    # Speciella vinklar
    angles_rad = [0, np.pi/6, np.pi/4, np.pi/3, np.pi/2, 2*np.pi/3, 3*np.pi/4, 5*np.pi/6, np.pi]
    angles_deg = [0, 30, 45, 60, 90, 120, 135, 150, 180]

    for angle_rad, angle_deg in zip(angles_rad, angles_deg):
        x = np.cos(angle_rad)
        y = np.sin(angle_rad)

        ax.plot(x, y, 'ro', markersize=8)
        ax.plot([0, x], [0, y], 'r-', linewidth=1.5, alpha=0.6)

        # Märk några viktiga vinklar
        if angle_deg in [0, 45, 90, 135, 180]:
            label_x = x * 1.25
            label_y = y * 1.25
            ax.text(label_x, label_y, f'{angle_deg}°', fontsize=12, ha='center',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

    # En specifik vinkel (60°)
    angle = np.pi/3
    x = np.cos(angle)
    y = np.sin(angle)
    ax.plot([0, x], [0, y], 'g-', linewidth=3)
    ax.plot(x, y, 'go', markersize=12)

    # Koordinater
    ax.plot([x, x], [0, y], 'g--', linewidth=2)
    ax.plot([0, x], [y, y], 'g--', linewidth=2)

    ax.text(x/2, -0.15, f'cos(60°) = {x:.2f}', fontsize=12, ha='center', color='#059669')
    ax.text(-0.3, y/2, f'sin(60°) = {y:.2f}', fontsize=12, ha='center', color='#059669')

    # Titel och förklaring
    ax.set_title('Enhetscirkeln', fontsize=20, fontweight='bold', pad=20)

    explanation = 'På enhetscirkeln:\n' + r'$x = \cos(\theta)$' + '\n' + r'$y = \sin(\theta)$' + '\n' + r'Radie = 1'
    ax.text(0, -1.3, explanation, fontsize=14, ha='center',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#FEF3C7',
                    edgecolor='#F59E0B', linewidth=2))

    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap6_04_trigonometriska_formler(filename='kap6-04-trigonometriska-formler.png'):
    """Skapar figur för trigonometriska formler (sin²+cos²=1)"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), dpi=300)

    # Vänster: Geometrisk tolkning på enhetscirkel
    ax1.set_xlim(-0.2, 1.3)
    ax1.set_ylim(-0.2, 1.3)
    ax1.set_aspect('equal')

    # Enhetscirkel (första kvadranten)
    theta = np.linspace(0, np.pi/2, 100)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)
    ax1.plot(x_circle, y_circle, 'b-', linewidth=3, label='Enhetscirkel')

    # Specifik vinkel
    angle = np.pi/4
    x = np.cos(angle)
    y = np.sin(angle)

    # Rätvinklig triangel
    ax1.plot([0, x, x, 0], [0, 0, y, 0], 'r-', linewidth=2)
    ax1.plot([0, x], [0, y], 'g-', linewidth=3, label='Radie = 1')
    ax1.plot(x, y, 'go', markersize=12)

    # Märk sidor
    ax1.text(x/2, -0.08, f'cos(θ)', fontsize=14, ha='center', color='#DC2626')
    ax1.text(x + 0.1, y/2, f'sin(θ)', fontsize=14, ha='left', color='#DC2626')
    ax1.text(x/2 - 0.1, y/2 + 0.1, '1', fontsize=14, ha='center', color='#059669')

    # Räta vinkeln
    square_size = 0.1
    square = patches.Rectangle((x - square_size, 0), square_size, square_size,
                               linewidth=2, edgecolor='black', facecolor='none')
    ax1.add_patch(square)

    ax1.axhline(y=0, color='k', linestyle='-', linewidth=1.5)
    ax1.axvline(x=0, color='k', linestyle='-', linewidth=1.5)
    ax1.set_title('Pythagoras sats på enhetscirkeln', fontsize=16, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)

    # Höger: Formler
    ax2.axis('off')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)

    ax2.text(5, 9, 'Trigonometriska identiteter', fontsize=20, fontweight='bold', ha='center')

    # Huvudformel
    ax2.text(5, 7.8, r'$\sin^2(\theta) + \cos^2(\theta) = 1$', fontsize=28, ha='center',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#FEF3C7',
                     edgecolor='#F59E0B', linewidth=3))

    # Andra formler
    formulas = [
        ('Övriga identiteter:', 18, 'bold', '#E0F2FE', '#0284C7'),
        (r'$\tan(\theta) = \frac{\sin(\theta)}{\cos(\theta)}$', 16, 'normal', '#ECFDF5', '#10B981'),
        (r'$1 + \tan^2(\theta) = \frac{1}{\cos^2(\theta)}$', 16, 'normal', '#ECFDF5', '#10B981'),
        (r'$\sin(2\theta) = 2\sin(\theta)\cos(\theta)$', 16, 'normal', '#FEE2E2', '#DC2626'),
        (r'$\cos(2\theta) = \cos^2(\theta) - \sin^2(\theta)$', 16, 'normal', '#FEE2E2', '#DC2626'),
    ]

    y_pos = 6.5
    for formula, size, weight, bg, edge in formulas:
        ax2.text(5, y_pos, formula, fontsize=size, fontweight=weight, ha='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=bg, edgecolor=edge, linewidth=2))
        y_pos -= 0.9

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


def create_kap6_08_triangelsatser(filename='kap6-08-triangelsatser.png'):
    """Skapar figur för tillämpning av triangelsatser"""
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    # Problem: Hitta höjd av torn
    # Triangel från observationspunkt
    A = np.array([2, 1])  # Observationspunkt
    B = np.array([10, 1])  # Tornets bas
    C = np.array([10, 7])  # Tornets topp

    # Rita tornet
    ax.plot([B[0], C[0]], [B[1], C[1]], 'brown', linewidth=8, label='Torn')
    ax.plot([B[0] - 0.3, B[0] + 0.3], [B[1], B[1]], 'k-', linewidth=3)  # Markera bas

    # Siktlinje
    ax.plot([A[0], C[0]], [A[1], C[1]], 'r--', linewidth=2, label='Siktlinje')

    # Marknivå
    ax.plot([A[0] - 0.5, C[0] + 0.5], [A[1], B[1]], 'g-', linewidth=3, alpha=0.5, label='Marknivå')

    # Avstånd på marken
    ax.plot([A[0], B[0]], [A[1], B[1]], 'b-', linewidth=3)
    ax.text(6, 0.5, 'Avstånd = 8 m', fontsize=14, ha='center', color='#0284C7',
           bbox=dict(boxstyle='round', facecolor='#E0F2FE', alpha=0.9))

    # Vinkel vid A
    angle_size = 1.5
    angle = np.degrees(np.arctan((C[1] - A[1]) / (C[0] - A[0])))
    angle_arc = Arc(A, angle_size, angle_size, angle=0, theta1=0, theta2=angle,
                   color='#DC2626', linewidth=3)
    ax.add_patch(angle_arc)
    ax.text(A[0] + 1, A[1] + 0.5, '35°', fontsize=14, fontweight='bold', color='#DC2626')

    # Punkter
    ax.plot(*A, 'o', color='blue', markersize=12, zorder=5)
    ax.plot(*C, 'o', color='red', markersize=12, zorder=5)

    ax.text(A[0] - 0.5, A[1] - 0.5, 'A (observatör)', fontsize=12, ha='right')
    ax.text(C[0] + 0.5, C[1], 'C (topp)', fontsize=12, ha='left')
    ax.text(B[0] + 0.5, B[1] - 0.5, 'B (bas)', fontsize=12, ha='left')

    # Höjd (sökta)
    ax.text(C[0] + 0.7, 4, 'h = ?', fontsize=16, ha='left', color='brown',
           fontweight='bold', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

    # Lösning
    solution = 'Lösning:\n' + r'$\tan(35°) = \frac{h}{8}$' + '\n' + r'$h = 8 \cdot \tan(35°) \approx 5.6$ m'
    ax.text(2, 8, solution, fontsize=16, ha='left',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#FEF3C7',
                    edgecolor='#F59E0B', linewidth=2))

    ax.set_title('Tillämpning: Bestäm tornets höjd', fontsize=20, fontweight='bold', pad=20)
    ax.legend(fontsize=11, loc='upper right')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Figur sparad: {filename}')
    return filename


if __name__ == '__main__':
    print('=' * 60)
    print('MATEMATISK BILDGENERATOR')
    print('Skapar pedagogiska figurer med exakt matematisk precision')
    print('=' * 60)
    print()

    # Ursprungliga figurer
    print('Skapar ursprungliga figurer...')
    create_triangle_areasatsen()
    create_triangle_sinussatsen()
    create_triangle_cosinussatsen()
    create_derivative_secant()
    print()

    # VIKTIGA FIGURER (8 st)
    print('=' * 60)
    print('VIKTIGA FIGURER (8 st)')
    print('=' * 60)
    create_kap1_01_brakforkortning()
    create_kap1_02_brakaddition()
    create_kap2_03_derivata_definition()
    create_kap2_04_derivering_exempel()
    create_kap3_02_produktregeln()
    create_kap3_05_kedjeregeln()
    create_kap4_02_derivata_nollstallen()
    create_kap5_01_primitiv_funktion()
    print()

    # ÖNSKVÄRDA FIGURER (16 st)
    print('=' * 60)
    print('ÖNSKVÄRDA FIGURER (16 st)')
    print('=' * 60)
    create_kap1_03_brak_multiplikation()
    create_kap2_02_tangent_lutning()
    create_kap2_05_deriverbarhet_absolutbelopp()
    create_kap3_03_potensfunktioner()
    create_kap3_06_tillampningar_derivata()
    create_kap4_05_andraderivata()
    create_kap4_06_extremvardesproblem()
    create_kap5_02_primitiva_villkor()
    create_kap5_04_fundamentalsats()
    create_kap5_07_tillampningar_integral()
    create_kap6_01_trigonometri_triangel()
    create_kap6_03_enhetscirkel()
    create_kap6_04_trigonometriska_formler()
    create_kap6_08_triangelsatser()
    print()

    print('=' * 60)
    print('KLART! Alla 28 figurer är skapade och redo att användas.')
    print('4 ursprungliga + 8 viktiga + 16 önskvärda = 28 figurer totalt')
    print('=' * 60)
