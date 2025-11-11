"""
Detector de Formas Geométricas
Proyecto: Entornos de Aprendizaje Inclusivos con Visión Artificial
Autor: Semillero de Investigación
Fecha: Noviembre 2025

Este módulo implementa la detección de formas geométricas básicas
utilizando OpenCV y aproximación poligonal de contornos.
"""

import cv2
import numpy as np
import imutils


class ShapeDetector:
    """
    Clase para detectar y clasificar formas geométricas en imágenes.
    
    Utiliza aproximación poligonal de contornos para identificar:
    - Círculos
    - Triángulos
    - Cuadrados
    - Rectángulos
    - Pentágonos
    - Hexágonos
    """
    
    def __init__(self):
        """Inicializa el detector de formas."""
        pass
    
    def detect(self, contour):
        """
        Detecta el tipo de forma geométrica de un contorno.
        
        Args:
            contour: Contorno de OpenCV (numpy array)
            
        Returns:
            str: Nombre de la forma detectada
        """
        # Inicializar el nombre de la forma
        shape = "desconocido"
        
        # Calcular el perímetro del contorno
        perimeter = cv2.arcLength(contour, True)
        
        # Aproximar el contorno con un polígono
        # El parámetro 0.04 controla la precisión de la aproximación
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        
        # Clasificar la forma según el número de vértices
        vertices = len(approx)
        
        if vertices == 3:
            shape = "triángulo"
            
        elif vertices == 4:
            # Calcular el bounding box del contorno
            (x, y, w, h) = cv2.boundingRect(approx)
            
            # Calcular la relación de aspecto
            aspect_ratio = w / float(h)
            
            # Distinguir entre cuadrado y rectángulo
            # Si la relación de aspecto está entre 0.95 y 1.05, es un cuadrado
            if 0.95 <= aspect_ratio <= 1.05:
                shape = "cuadrado"
            else:
                shape = "rectángulo"
                
        elif vertices == 5:
            shape = "pentágono"
            
        elif vertices == 6:
            shape = "hexágono"
            
        else:
            # Si tiene más de 6 vértices, probablemente sea un círculo
            # Verificamos calculando la circularidad
            area = cv2.contourArea(contour)
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            if circularity > 0.8:
                shape = "círculo"
        
        return shape
    
    def get_center(self, contour):
        """
        Calcula el centro del contorno usando momentos.
        
        Args:
            contour: Contorno de OpenCV
            
        Returns:
            tuple: Coordenadas (x, y) del centro
        """
        M = cv2.moments(contour)
        
        # Evitar división por cero
        if M["m00"] == 0:
            return (0, 0)
        
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        return (cX, cY)
    
    def get_dimensions(self, contour):
        """
        Obtiene las dimensiones del contorno.
        
        Args:
            contour: Contorno de OpenCV
            
        Returns:
            dict: Diccionario con área, perímetro, ancho y alto
        """
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        (x, y, w, h) = cv2.boundingRect(contour)
        
        return {
            'area': area,
            'perimetro': perimeter,
            'ancho': w,
            'alto': h
        }


def detect_shapes_in_image(image_path, show_steps=False):
    """
    Detecta formas geométricas en una imagen.
    
    Args:
        image_path: Ruta a la imagen
        show_steps: Si True, muestra los pasos del procesamiento
        
    Returns:
        tuple: (imagen procesada, lista de formas detectadas)
    """
    # Cargar la imagen
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: No se pudo cargar la imagen {image_path}")
        return None, []
    
    # Redimensionar la imagen para mejor procesamiento
    resized = imutils.resize(image, width=800)
    ratio = image.shape[0] / float(resized.shape[0])
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    if show_steps:
        cv2.imshow("1. Escala de grises", gray)
    
    # Aplicar desenfoque Gaussiano para reducir ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    if show_steps:
        cv2.imshow("2. Desenfoque Gaussiano", blurred)
    
    # Aplicar umbralización
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    
    if show_steps:
        cv2.imshow("3. Umbralización", thresh)
    
    # Encontrar contornos
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    
    # Inicializar el detector de formas
    shape_detector = ShapeDetector()
    
    # Lista para almacenar las formas detectadas
    detected_shapes = []
    
    # Procesar cada contorno
    for i, contour in enumerate(contours):
        # Filtrar contornos pequeños (ruido)
        if cv2.contourArea(contour) < 100:
            continue
        
        # Detectar la forma
        shape = shape_detector.detect(contour)
        
        # Obtener el centro del contorno
        center = shape_detector.get_center(contour)
        
        # Obtener dimensiones
        dimensions = shape_detector.get_dimensions(contour)
        
        # Dibujar el contorno
        cv2.drawContours(resized, [contour], -1, (0, 255, 0), 2)
        
        # Dibujar el centro
        cv2.circle(resized, center, 5, (255, 0, 0), -1)
        
        # Escribir el nombre de la forma
        cv2.putText(resized, shape, center, cv2.FONT_HERSHEY_SIMPLEX,
                   0.6, (255, 255, 255), 2)
        
        # Agregar a la lista de formas detectadas
        detected_shapes.append({
            'forma': shape,
            'centro': center,
            'area': dimensions['area'],
            'perimetro': dimensions['perimetro']
        })
        
        print(f"Forma {i+1}: {shape} - Centro: {center} - Área: {dimensions['area']:.2f}")
    
    return resized, detected_shapes


def detect_shapes_from_camera():
    """
    Detecta formas geométricas en tiempo real desde la cámara web.
    
    Controles:
    - 'q': Salir
    - 's': Capturar imagen
    """
    # Inicializar la cámara
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara")
        return
    
    # Inicializar el detector de formas
    shape_detector = ShapeDetector()
    
    print("Detector de formas en tiempo real")
    print("Controles:")
    print("  'q' - Salir")
    print("  's' - Capturar imagen")
    print("-" * 50)
    
    while True:
        # Capturar frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: No se pudo leer el frame")
            break
        
        # Crear una copia del frame para procesar
        processed = frame.copy()
        
        # Convertir a escala de grises
        gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        
        # Aplicar desenfoque
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Umbralización adaptativa (mejor para iluminación variable)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 11, 2)
        
        # Encontrar contornos
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        
        # Procesar cada contorno
        for contour in contours:
            # Filtrar contornos pequeños
            if cv2.contourArea(contour) < 500:
                continue
            
            # Detectar la forma
            shape = shape_detector.detect(contour)
            
            # Obtener el centro
            center = shape_detector.get_center(contour)
            
            # Dibujar contorno
            cv2.drawContours(processed, [contour], -1, (0, 255, 0), 2)
            
            # Dibujar centro
            cv2.circle(processed, center, 5, (0, 0, 255), -1)
            
            # Escribir el nombre de la forma
            cv2.putText(processed, shape, 
                       (center[0] - 30, center[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Mostrar información en pantalla
        cv2.putText(processed, "Presiona 'q' para salir, 's' para capturar",
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Mostrar el frame procesado
        cv2.imshow("Detector de Formas - Tiempo Real", processed)
        cv2.imshow("Umbralización", thresh)
        
        # Esperar por tecla
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("Saliendo...")
            break
        elif key == ord('s'):
            # Guardar la imagen capturada
            filename = f"captura_{cv2.getTickCount()}.png"
            cv2.imwrite(filename, processed)
            print(f"Imagen guardada: {filename}")
    
    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("DETECTOR DE FORMAS GEOMÉTRICAS")
    print("Proyecto: Entornos de Aprendizaje Inclusivos")
    print("=" * 60)
    print()
    
    # Menú de opciones
    print("Opciones:")
    print("1. Detectar formas en una imagen")
    print("2. Detectar formas desde la cámara (tiempo real)")
    print("3. Salir")
    print()
    
    try:
        opcion = input("Seleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            # Detectar formas en imagen
            image_path = input("Ingrese la ruta de la imagen: ").strip()
            
            if not image_path:
                print("Usando imagen de prueba...")
                # Aquí puedes poner una ruta por defecto
                image_path = "test_shapes.png"
            
            show_steps = input("¿Mostrar pasos del procesamiento? (s/n): ").strip().lower() == 's'
            
            result, shapes = detect_shapes_in_image(image_path, show_steps)
            
            if result is not None:
                print(f"\nSe detectaron {len(shapes)} formas:")
                for i, shape in enumerate(shapes, 1):
                    print(f"{i}. {shape['forma'].capitalize()} - Área: {shape['area']:.2f}")
                
                cv2.imshow("Resultado - Presione cualquier tecla para salir", result)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        
        elif opcion == "2":
            # Detectar formas desde cámara
            detect_shapes_from_camera()
        
        elif opcion == "3":
            print("¡Hasta luego!")
            sys.exit(0)
        
        else:
            print("Opción no válida")
    
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario")
    except Exception as e:
        print(f"Error: {e}")
