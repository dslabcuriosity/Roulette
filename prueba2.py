import statistics
import math
from typing import List, Dict, Tuple


class RuletaAnalyzer:
    def __init__(self):
        self.historial = []  # Lista de números que han salido
        self.columnas = {
            1: [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
            2: [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
            3: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
        }
        self.docenas = {
            1: list(range(1, 13)),  # 1-12
            2: list(range(13, 25)),  # 13-24
            3: list(range(25, 37))  # 25-36
        }

    def agregar_numero(self, numero: int):
        """Agrega un número al historial"""
        if 0 <= numero <= 36:
            self.historial.append(numero)

    def cargar_historial(self, numeros: List[int]):
        """Carga una lista completa de números históricos"""
        self.historial = [n for n in numeros if 0 <= n <= 36]

    def obtener_columna(self, numero: int) -> int:
        """Devuelve la columna del número (1, 2, 3) o 0 si es cero"""
        if numero == 0:
            return 0
        for col, nums in self.columnas.items():
            if numero in nums:
                return col
        return 0

    def obtener_docena(self, numero: int) -> int:
        """Devuelve la docena del número (1, 2, 3) o 0 si es cero"""
        if numero == 0:
            return 0
        for doc, nums in self.docenas.items():
            if numero in nums:
                return doc
        return 0

    def calcular_demoras(self, tipo: str = 'columna') -> Dict[int, List[int]]:
        """
        Calcula las demoras entre apariciones
        tipo: 'columna' o 'docena'
        """
        demoras = {1: [], 2: [], 3: []}
        ultimas_apariciones = {1: -1, 2: -1, 3: -1}

        func_categoria = self.obtener_columna if tipo == 'columna' else self.obtener_docena

        for i, numero in enumerate(self.historial):
            categoria = func_categoria(numero)

            if categoria > 0:  # Ignorar el cero
                # Si ya apareció antes, calcular demora
                if ultimas_apariciones[categoria] != -1:
                    demora = i - ultimas_apariciones[categoria]
                    demoras[categoria].append(demora)

                # Actualizar última aparición
                ultimas_apariciones[categoria] = i

        return demoras

    def estadisticas_demoras(self, tipo: str = 'columna') -> Dict[int, Dict]:
        """
        Calcula estadísticas completas de demoras
        """
        demoras = self.calcular_demoras(tipo)
        estadisticas = {}

        for categoria, lista_demoras in demoras.items():
            if len(lista_demoras) > 1:
                promedio = statistics.mean(lista_demoras)
                desviacion = statistics.stdev(lista_demoras)
                minimo = min(lista_demoras)
                maximo = max(lista_demoras)

                estadisticas[categoria] = {
                    'promedio': round(promedio, 2),
                    'desviacion': round(desviacion, 2),
                    'minimo': minimo,
                    'maximo': maximo,
                    'total_apariciones': len(lista_demoras),
                    'umbral_1sigma': round(promedio + desviacion, 2),
                    'umbral_2sigma': round(promedio + 2 * desviacion, 2),
                    'umbral_3sigma': round(promedio + 3 * desviacion, 2)
                }
            else:
                estadisticas[categoria] = {
                    'promedio': 0,
                    'desviacion': 0,
                    'mensaje': 'Datos insuficientes'
                }

        return estadisticas

    def demora_actual(self, tipo: str = 'columna') -> Dict[int, int]:
        """
        Calcula cuántas tiradas han pasado desde la última aparición de cada categoría
        """
        if not self.historial:
            return {1: 0, 2: 0, 3: 0}

        demoras_actuales = {1: 0, 2: 0, 3: 0}
        func_categoria = self.obtener_columna if tipo == 'columna' else self.obtener_docena

        # Buscar desde el final hacia atrás
        for i in range(len(self.historial) - 1, -1, -1):
            numero = self.historial[i]
            categoria = func_categoria(numero)

            if categoria > 0:
                # Calcular demora desde esta aparición
                demoras_actuales[categoria] = len(self.historial) - 1 - i
                break

        # Para las categorías que no encontramos, buscar individualmente
        for cat in [1, 2, 3]:
            if demoras_actuales[cat] == 0:
                for i in range(len(self.historial) - 1, -1, -1):
                    if func_categoria(self.historial[i]) == cat:
                        demoras_actuales[cat] = len(self.historial) - 1 - i
                        break
                else:
                    demoras_actuales[cat] = len(self.historial)

        return demoras_actuales

    def señales_apuesta(self, tipo: str = 'columna', nivel_sigma: int = 2) -> Dict:
        """
        Identifica oportunidades de apuesta basadas en desviación estándar
        nivel_sigma: 1, 2, o 3 (conservador a extremo)
        """
        estadisticas = self.estadisticas_demoras(tipo)
        demoras_actuales = self.demora_actual(tipo)
        señales = {}

        for categoria in [1, 2, 3]:
            if 'umbral_1sigma' in estadisticas[categoria]:
                stats = estadisticas[categoria]
                demora_actual = demoras_actuales[categoria]

                umbral = stats[f'umbral_{nivel_sigma}sigma']

                señales[categoria] = {
                    'demora_actual': demora_actual,
                    'promedio': stats['promedio'],
                    'umbral': umbral,
                    'apostar': demora_actual >= umbral,
                    'intensidad': round((demora_actual - stats['promedio']) / stats['desviacion'], 2)
                }
            else:
                señales[categoria] = {
                    'apostar': False,
                    'mensaje': 'Datos insuficientes'
                }

        return señales

    def reporte_completo(self, tipo: str = 'columna', nivel_sigma: int = 2):
        """
        Genera un reporte completo del análisis
        """
        print(f"\n=== ANÁLISIS DE {tipo.upper()}S ===")
        print(f"Total de tiradas analizadas: {len(self.historial)}")
        print(f"Nivel de confianza: {nivel_sigma}σ")

        estadisticas = self.estadisticas_demoras(tipo)
        señales = self.señales_apuesta(tipo, nivel_sigma)

        for categoria in [1, 2, 3]:
            print(f"\n--- {tipo.title()} {categoria} ---")

            if 'promedio' in estadisticas[categoria] and estadisticas[categoria]['promedio'] > 0:
                stats = estadisticas[categoria]
                señal = señales[categoria]

                print(f"Promedio de demoras: {stats['promedio']}")
                print(f"Desviación estándar: {stats['desviacion']}")
                print(f"Rango: {stats['minimo']} - {stats['maximo']}")
                print(f"Umbral {nivel_sigma}σ: {stats[f'umbral_{nivel_sigma}sigma']}")
                print(f"Demora actual: {señal['demora_actual']}")
                print(f"Intensidad: {señal['intensidad']}σ")
                print(f"🎯 APOSTAR: {'SÍ' if señal['apostar'] else 'NO'}")
            else:
                print("Datos insuficientes para análisis")


def cargar_desde_excel(archivo_excel: str, columna: str = 'A') -> List[int]:
    """
    Carga números desde un archivo Excel
    archivo_excel: ruta del archivo (ej: 'datos.xlsx')
    columna: columna a leer (ej: 'A', 'B', etc.)
    """
    try:
        import pandas as pd
        df = pd.read_excel(archivo_excel)
        numeros = df.iloc[:, 0].dropna().astype(int).tolist()  # Primera columna
        print(f"✅ Cargados {len(numeros)} números desde {archivo_excel}")
        return numeros
    except ImportError:
        print("❌ Error: Necesitas instalar pandas y openpyxl")
        print("Ejecuta: pip install pandas openpyxl")
        return []
    except Exception as e:
        print(f"❌ Error cargando Excel: {e}")
        return []


def entrada_manual() -> List[int]:
    """
    Permite entrada manual de números desde teclado
    """
    print("\n=== ENTRADA MANUAL DE NÚMEROS ===")
    print("Ingresa los números separados por espacios o comas")
    print("Ejemplo: 15 22 8 31 4 17 25")
    print("Presiona Enter cuando termines:")

    entrada = input("\nNúmeros: ").strip()

    # Limpiar entrada (espacios, comas, etc.)
    import re
    numeros_texto = re.findall(r'\d+', entrada)

    try:
        numeros = [int(n) for n in numeros_texto if 0 <= int(n) <= 36]
        print(f"✅ Procesados {len(numeros)} números válidos")
        return numeros
    except ValueError:
        print("❌ Error: Algunos valores no son números válidos")
        return []


def menu_principal():
    """
    Menú interactivo para seleccionar método de carga
    """
    print("\n" + "=" * 50)
    print("🎰 ANALIZADOR DE RULETA")
    print("=" * 50)
    print("Selecciona cómo cargar los datos:")
    print("1. Desde archivo Excel")
    print("2. Entrada manual por teclado")
    print("3. Datos de ejemplo (para pruebas)")
    print("0. Salir")

    return input("\nOpción: ").strip()


def configurar_analisis():
    """
    Configuración del nivel de análisis
    """
    print("\n--- CONFIGURACIÓN DE ANÁLISIS ---")
    print("Nivel de confianza:")
    print("1. Conservador (1σ) - Más señales, menos confiables")
    print("2. Balanceado (2σ) - Recomendado")
    print("3. Estricto (3σ) - Pocas señales, muy confiables")

    try:
        nivel = int(input("Selecciona nivel (1-3): ").strip())
        return max(1, min(3, nivel))  # Entre 1 y 3
    except ValueError:
        print("Usando nivel 2 (balanceado) por defecto")
        return 2


# Programa principal
if __name__ == "__main__":
    while True:
        opcion = menu_principal()

        if opcion == "0":
            print("¡Hasta luego! 🎰")
            break

        numeros = []

        if opcion == "1":
            archivo = input("Nombre del archivo Excel (ej: datos.xlsx): ").strip()
            if archivo:
                numeros = cargar_desde_excel(archivo)

        elif opcion == "2":
            numeros = entrada_manual()

        elif opcion == "3":
            numeros = [15, 22, 8, 31, 4, 17, 25, 12, 36, 7, 19, 2,
                       28, 14, 33, 6, 20, 11, 29, 1, 35, 16, 24, 9,
                       13, 27, 10, 5, 30, 18, 23, 34, 3, 26, 21]
            print(f"✅ Usando datos de ejemplo ({len(numeros)} números)")

        else:
            print("❌ Opción no válida")
            continue

        if numeros:
            # Crear analizador y cargar datos
            analyzer = RuletaAnalyzer()
            analyzer.cargar_historial(numeros)

            # Configurar nivel de análisis
            nivel_sigma = configurar_analisis()

            # Generar reportes
            analyzer.reporte_completo('columna', nivel_sigma)
            analyzer.reporte_completo('docena', nivel_sigma)

            input("\nPresiona Enter para continuar...")
        else:
            print("❌ No se cargaron datos válidos")
            input("Presiona Enter para continuar...")