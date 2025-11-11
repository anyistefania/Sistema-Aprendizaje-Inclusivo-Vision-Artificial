#!/usr/bin/env python3
"""
Reconocedor Simple de Vocales
Detecta vocales impresas usando características geométricas
"""

import cv2
import numpy as np
import pyttsx3
import time

class VocalRecognizer:
    """Reconocedor básico de vocales por características geométricas"""

    def __init__(self):
        self.engine = None
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 130)
            self.engine.setProperty('volume', 1.0)
        except:
            print("⚠️ Sistema de voz no disponible")

    def speak(self, text):
        """Sintetiza voz"""
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass

    def detectar_vocal_simple(self, contour):
        """
        Detecta vocales por características geométricas básicas.
        NOTA: Funciona mejor con vocales impresas en mayúsculas.
        """
        # Calcular características
        area = cv2.contourArea(contour)
        perimetro = cv2.arcLength(contour, True)

        if perimetro == 0:
            return None

        # Aproximar contorno
        approx = cv2.approxPolyDP(contour, 0.02 * perimetro, True)
        vertices = len(approx)

        # Calcular circularidad
        circularidad = 4 * np.pi * area / (perimetro * perimetro) if perimetro > 0 else 0

        # Bounding box y aspect ratio
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h) if h > 0 else 0

        # Calcular solidez
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        solidez = area / hull_area if hull_area > 0 else 0

        # HEURÍSTICAS SIMPLES:

        # O - circular, alta circularidad
        if circularidad > 0.75 and 0.7 < aspect_ratio < 1.3:
            return "O"

        # I - muy vertical, estrecha
        if aspect_ratio < 0.4 and vertices < 8:
            return "I"

        # A - triangular en la parte superior, tiene hueco
        if 0.5 < aspect_ratio < 0.9 and solidez < 0.85 and vertices > 6:
            # Verificar si tiene "pico" arriba
            top_points = [pt for pt in approx if pt[0][1] < y + h * 0.3]
            if len(top_points) > 0:
                return "A"

        # E - rectángulo con baja solidez (tiene huecos)
        if 0.4 < aspect_ratio < 0.7 and solidez < 0.80 and vertices >= 8:
            return "E"

        # U - semicircular, abierto arriba
        if 0.6 < aspect_ratio < 1.0 and 0.5 < circularidad < 0.75:
            # Verificar apertura arriba
            top_y = y + h * 0.2
            top_region = contour[contour[:, 0, 1] < top_y]
            if len(top_region) < len(contour) * 0.3:
                return "U"

        return None

    def run(self):
        """Ejecuta el reconocedor"""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("❌ Error: No se pudo abrir la cámara")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print("\n" + "="*70)
        print("   RECONOCEDOR SIMPLE DE VOCALES")
        print("="*70)
        print("\n📝 INSTRUCCIONES:")
        print("   1. Imprime vocales MAYÚSCULAS en papel (tamaño A4)")
        print("   2. Usa LETRA NEGRA sobre FONDO BLANCO")
        print("   3. Muestra UNA vocal a la vez")
        print("   4. Presiona ESPACIO para identificar")
        print("   5. Presiona Q para salir")
        print("\n💡 CONSEJO: Funciona mejor con:")
        print("   - Tipografía simple (Arial, Helvetica)")
        print("   - Tamaño grande (fuente 200+)")
        print("   - Buena iluminación")
        print("   - Sin sombras")
        print("="*70 + "\n")

        last_detection_time = 0
        cooldown = 2.0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frame = cv2.flip(frame, 1)

            # Preprocesar
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Umbralización para letras negras
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

            # Limpiar ruido
            kernel = np.ones((5, 5), np.uint8)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

            # Encontrar contornos
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)

            detected_vocals = []

            for contour in contours:
                area = cv2.contourArea(contour)

                # Filtrar por tamaño
                if area < 2000 or area > 100000:
                    continue

                # Detectar vocal
                vocal = self.detectar_vocal_simple(contour)

                if vocal:
                    # Dibujar
                    x, y, w, h = cv2.boundingRect(contour)

                    cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Etiqueta
                    label = f"Vocal: {vocal}"
                    label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
                    cv2.rectangle(frame,
                                (x, y - label_size[1] - 15),
                                (x + label_size[0] + 10, y),
                                (0, 255, 0), -1)
                    cv2.putText(frame, label, (x + 5, y - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

                    detected_vocals.append(vocal)

            # Panel de información
            cv2.rectangle(frame, (0, 0), (640, 80), (0, 0, 0), -1)
            cv2.putText(frame, "RECONOCEDOR DE VOCALES", (10, 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            if detected_vocals:
                texto = f"Detectadas: {', '.join(detected_vocals)}"
                cv2.putText(frame, texto, (10, 55),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Muestra una vocal...", (10, 55),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Ayuda
            cv2.putText(frame, "ESPACIO: Identificar | Q: Salir", (10, 470),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

            # Mostrar
            cv2.imshow("Reconocedor de Vocales", frame)
            cv2.imshow("Procesamiento", thresh)

            # Teclas
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break

            elif key == ord(' '):
                current_time = time.time()

                if detected_vocals and (current_time - last_detection_time) > cooldown:
                    vocal = detected_vocals[0]
                    mensaje = f"Veo la vocal {vocal}"
                    print(f"🎯 {mensaje}")
                    self.speak(mensaje)

                    last_detection_time = current_time
                elif not detected_vocals:
                    self.speak("No veo ninguna vocal. Muestra una letra más grande.")
                    print("⚠️ No se detectó ninguna vocal")

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        recognizer = VocalRecognizer()
        recognizer.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Programa interrumpido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
