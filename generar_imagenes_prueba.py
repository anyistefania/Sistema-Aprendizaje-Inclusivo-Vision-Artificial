"""
Generador de Imágenes de Prueba
Proyecto: Entornos de Aprendizaje Inclusivos
Autor: Semillero de Investigación

Este script crea imágenes de prueba con formas y colores
para probar el sistema sin necesidad de objetos físicos.
"""

import cv2
import numpy as np
import os


def create_test_images():
    """
    Crea imágenes de prueba con diferentes formas y colores.
    """
    print("🎨 Generando imágenes de prueba...\n")
    
    # Crear carpeta para imágenes
    output_dir = "imagenes_prueba"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Colores en BGR
    colors = {
        'rojo': (0, 0, 255),
        'azul': (255, 0, 0),
        'verde': (0, 255, 0),
        'amarillo': (0, 255, 255),
        'naranja': (0, 165, 255),
        'morado': (255, 0, 255)
    }
    
    # Imagen 1: Formas básicas de diferentes colores
    img1 = np.ones((600, 800, 3), dtype=np.uint8) * 240
    
    # Círculo rojo
    cv2.circle(img1, (150, 150), 80, colors['rojo'], -1)
    
    # Cuadrado azul
    cv2.rectangle(img1, (300, 70), (460, 230), colors['azul'], -1)
    
    # Triángulo verde
    pts = np.array([[600, 230], [530, 80], [670, 80]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(img1, [pts], colors['verde'])
    
    # Rectángulo amarillo
    cv2.rectangle(img1, (100, 350), (300, 500), colors['amarillo'], -1)
    
    # Pentágono naranja
    center = (500, 425)
    radius = 75
    pts = []
    for i in range(5):
        angle = np.pi/2 + (2*np.pi/5)*i
        x = int(center[0] + radius * np.cos(angle))
        y = int(center[1] + radius * np.sin(angle))
        pts.append([x, y])
    pts = np.array(pts, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(img1, [pts], colors['naranja'])
    
    filename1 = os.path.join(output_dir, "01_formas_basicas.png")
    cv2.imwrite(filename1, img1)
    print(f"✅ Creada: {filename1}")
    
    # Imagen 2: Nivel básico - Un círculo rojo grande
    img2 = np.ones((600, 800, 3), dtype=np.uint8) * 240
    cv2.circle(img2, (400, 300), 120, colors['rojo'], -1)
    
    filename2 = os.path.join(output_dir, "02_nivel_basico_circulo_rojo.png")
    cv2.imwrite(filename2, img2)
    print(f"✅ Creada: {filename2}")
    
    # Imagen 3: Nivel básico - Un cuadrado azul grande
    img3 = np.ones((600, 800, 3), dtype=np.uint8) * 240
    cv2.rectangle(img3, (250, 150), (550, 450), colors['azul'], -1)
    
    filename3 = os.path.join(output_dir, "03_nivel_basico_cuadrado_azul.png")
    cv2.imwrite(filename3, img3)
    print(f"✅ Creada: {filename3}")
    
    # Imagen 4: Nivel básico - Un triángulo verde grande
    img4 = np.ones((600, 800, 3), dtype=np.uint8) * 240
    pts = np.array([[400, 100], [200, 450], [600, 450]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(img4, [pts], colors['verde'])
    
    filename4 = os.path.join(output_dir, "04_nivel_basico_triangulo_verde.png")
    cv2.imwrite(filename4, img4)
    print(f"✅ Creada: {filename4}")
    
    # Imagen 5: Nivel intermedio - Varias formas
    img5 = np.ones((600, 800, 3), dtype=np.uint8) * 240
    
    cv2.circle(img5, (200, 150), 60, colors['azul'], -1)
    cv2.rectangle(img5, (350, 90), (490, 230), colors['rojo'], -1)
    cv2.circle(img5, (650, 150), 60, colors['amarillo'], -1)
    
    cv2.rectangle(img5, (100, 350), (240, 490), colors['verde'], -1)
    
    pts = np.array([[420, 500], [350, 370], [490, 370]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(img5, [pts], colors['naranja'])
    
    cv2.circle(img5, (650, 420), 60, colors['morado'], -1)
    
    filename5 = os.path.join(output_dir, "05_nivel_intermedio_multiple.png")
    cv2.imwrite(filename5, img5)
    print(f"✅ Creada: {filename5}")
    
    # Imagen 6: Colores primarios
    img6 = np.ones((400, 600, 3), dtype=np.uint8) * 240
    
    cv2.circle(img6, (150, 200), 80, colors['rojo'], -1)
    cv2.circle(img6, (300, 200), 80, colors['azul'], -1)
    cv2.circle(img6, (450, 200), 80, colors['amarillo'], -1)
    
    filename6 = os.path.join(output_dir, "06_colores_primarios.png")
    cv2.imwrite(filename6, img6)
    print(f"✅ Creada: {filename6}")
    
    # Imagen 7: Ejercicio de clasificación
    img7 = np.ones((600, 800, 3), dtype=np.uint8) * 240
    
    # Fila 1: Todos círculos de diferentes colores
    cv2.circle(img7, (150, 120), 50, colors['rojo'], -1)
    cv2.circle(img7, (300, 120), 50, colors['azul'], -1)
    cv2.circle(img7, (450, 120), 50, colors['verde'], -1)
    cv2.circle(img7, (600, 120), 50, colors['amarillo'], -1)
    
    # Fila 2: Todos cuadrados de diferentes colores
    cv2.rectangle(img7, (100, 270), (200, 370), colors['azul'], -1)
    cv2.rectangle(img7, (250, 270), (350, 370), colors['rojo'], -1)
    cv2.rectangle(img7, (400, 270), (500, 370), colors['amarillo'], -1)
    cv2.rectangle(img7, (550, 270), (650, 370), colors['verde'], -1)
    
    # Fila 3: Todos triángulos de diferentes colores
    for i, color in enumerate(['naranja', 'morado', 'verde', 'rojo']):
        x_base = 125 + i * 150
        pts = np.array([[x_base, 530], [x_base-40, 450], [x_base+40, 450]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(img7, [pts], colors[color])
    
    filename7 = os.path.join(output_dir, "07_ejercicio_clasificacion.png")
    cv2.imwrite(filename7, img7)
    print(f"✅ Creada: {filename7}")
    
    # Imagen 8: Patrón para completar
    img8 = np.ones((400, 800, 3), dtype=np.uint8) * 240
    
    cv2.circle(img8, (100, 200), 60, colors['rojo'], -1)
    cv2.circle(img8, (250, 200), 60, colors['azul'], -1)
    cv2.circle(img8, (400, 200), 60, colors['rojo'], -1)
    cv2.circle(img8, (550, 200), 60, colors['azul'], -1)
    
    # Signo de interrogación para completar
    cv2.putText(img8, "?", (680, 230), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 100, 100), 5)
    
    filename8 = os.path.join(output_dir, "08_patron_secuencia.png")
    cv2.imwrite(filename8, img8)
    print(f"✅ Creada: {filename8}")
    
    print(f"\n✨ Se crearon 8 imágenes de prueba en la carpeta '{output_dir}/'")
    print("\n📝 Descripción de las imágenes:")
    print("   01 - Formas básicas variadas (círculo, cuadrado, triángulo, rectángulo, pentágono)")
    print("   02 - Nivel básico: Círculo rojo")
    print("   03 - Nivel básico: Cuadrado azul")
    print("   04 - Nivel básico: Triángulo verde")
    print("   05 - Nivel intermedio: Múltiples formas y colores")
    print("   06 - Colores primarios: Rojo, azul, amarillo")
    print("   07 - Ejercicio de clasificación: Formas organizadas")
    print("   08 - Patrón de secuencia para completar")
    print("\n💡 Usa estas imágenes para probar el detector de formas:")
    print("   python shape_detector.py")
    print("   Luego selecciona opción 1 e ingresa la ruta de la imagen")


def create_guide_image():
    """
    Crea una imagen guía con instrucciones.
    """
    img = np.ones((800, 1000, 3), dtype=np.uint8) * 250
    
    # Título
    cv2.putText(img, "GUIA DE USO - SISTEMA DE APRENDIZAJE", (50, 50),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Instrucciones
    instructions = [
        "1. Coloca objetos de colores frente a la camara",
        "2. Usa fondo claro y uniforme (blanco o beige)",
        "3. Buena iluminacion (sin sombras fuertes)",
        "4. Objetos grandes (minimo 5x5 cm)",
        "5. Colores vivos y saturados",
        "",
        "FORMAS DETECTADAS:",
        "- Circulo (como una pelota)",
        "- Triangulo (como un tejado)",
        "- Cuadrado (como una ventana)",
        "- Rectangulo (como una puerta)",
        "- Pentagono (5 lados)",
        "",
        "COLORES DETECTADOS:",
        "- Rojo, Azul, Verde (primarios)",
        "- Amarillo, Naranja, Morado (secundarios)",
    ]
    
    y = 120
    for line in instructions:
        if line.startswith("-"):
            cv2.putText(img, line, (100, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 50), 1)
        elif line == "":
            y += 10
        else:
            cv2.putText(img, line, (70, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        y += 35
    
    # Ejemplos visuales
    y = 550
    cv2.putText(img, "EJEMPLOS:", (70, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    y += 50
    cv2.circle(img, (150, y), 40, (0, 0, 255), -1)
    cv2.putText(img, "Circulo Rojo", (220, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    cv2.rectangle(img, (500, y-40), (580, y+40), (255, 0, 0), -1)
    cv2.putText(img, "Cuadrado Azul", (620, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    y += 100
    pts = np.array([[150, y], [110, y-60], [190, y-60]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], (0, 255, 0))
    cv2.putText(img, "Triangulo Verde", (220, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    cv2.rectangle(img, (500, y-60), (650, y+20), (0, 255, 255), -1)
    cv2.putText(img, "Rectangulo Amarillo", (680, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    output_dir = "imagenes_prueba"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = os.path.join(output_dir, "00_GUIA_DE_USO.png")
    cv2.imwrite(filename, img)
    print(f"\n✅ Guía creada: {filename}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("   GENERADOR DE IMÁGENES DE PRUEBA")
    print("   Sistema de Aprendizaje Inclusivo")
    print("="*70 + "\n")
    
    try:
        create_guide_image()
        create_test_images()
        
        print("\n" + "="*70)
        print("✨ ¡Proceso completado exitosamente!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
