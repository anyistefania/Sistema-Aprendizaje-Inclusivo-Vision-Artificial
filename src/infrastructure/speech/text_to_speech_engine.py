"""
Motor de Síntesis de Voz - Capa de Infraestructura
Implementación concreta del motor de texto a voz
"""

import pyttsx3
from typing import Optional


class TextToSpeechEngine:
    """
    Motor de síntesis de voz para retroalimentación auditiva.

    Implementa la funcionalidad de convertir texto a voz
    usando la biblioteca pyttsx3.
    """

    def __init__(self, rate: int = 150, volume: float = 1.0):
        """
        Inicializa el motor de voz.

        Args:
            rate: Velocidad de habla (palabras por minuto)
            volume: Volumen (0.0 a 1.0)
        """
        self.engine = None
        self.is_available = False

        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)

            # Intentar configurar voz en español
            self._setup_spanish_voice()

            self.is_available = True

        except Exception as e:
            print(f"⚠️  Advertencia: No se pudo inicializar el motor de voz: {e}")
            self.is_available = False

    def _setup_spanish_voice(self):
        """Intenta configurar una voz en español"""
        if not self.engine:
            return

        try:
            voices = self.engine.getProperty('voices')
            for voice in voices:
                # Buscar voz en español
                if hasattr(voice, 'languages') and voice.languages:
                    if 'spanish' in str(voice.languages[0]).lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                # Alternativa: buscar por nombre
                if hasattr(voice, 'name') and 'spanish' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        except Exception as e:
            print(f"⚠️  No se pudo configurar voz en español: {e}")

    def speak(self, text: str, wait: bool = True):
        """
        Sintetiza texto a voz.

        Args:
            text: Texto a sintetizar
            wait: Si True, espera a que termine de hablar
        """
        if not self.is_available or not self.engine:
            return

        try:
            self.engine.say(text)
            if wait:
                self.engine.runAndWait()
        except Exception as e:
            print(f"⚠️  Error al sintetizar voz: {e}")

    def set_rate(self, rate: int):
        """
        Configura la velocidad de habla.

        Args:
            rate: Velocidad en palabras por minuto
        """
        if self.engine:
            try:
                self.engine.setProperty('rate', rate)
            except Exception as e:
                print(f"⚠️  Error al configurar velocidad: {e}")

    def set_volume(self, volume: float):
        """
        Configura el volumen.

        Args:
            volume: Volumen (0.0 a 1.0)
        """
        if self.engine:
            try:
                self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
            except Exception as e:
                print(f"⚠️  Error al configurar volumen: {e}")

    def stop(self):
        """Detiene la síntesis de voz actual"""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass

    def __del__(self):
        """Limpia recursos al destruir el objeto"""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
