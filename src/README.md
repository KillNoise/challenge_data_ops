# Analisis de Resultados

## Metricas obtenidas

| Function | Time (s) | Memory (MiB) | Approach |
|----------|----------|--------------|----------|
| q1_time | 2.96 | 494.3 | orjson + bulk |
| q1_memory | 6.97 | 86.3 | streaming |
| q2_time | 48.23 | 495.3 | orjson + bulk |
| q2_memory | 52.04 | 86.4 | streaming |
| q3_time | 2.80 | 496.0 | orjson + bulk |
| q3_memory | 6.68 | 73.4 | streaming |

> Nota: los tiempos incluyen overhead de cProfile (~2-5x). Los tiempos reales de ejecucion son menores.

## Analisis por problema

### Q1 - Top fechas
- **Speedup time vs memory**: 1.7x mas rapido
- **Tradeoff memoria**: 5.7x mas RAM (493 vs 85 MiB)
- La ganancia de orjson se nota claramente: el parsing de JSON es el cuello de botella principal.

### Q2 - Top emojis
- **Speedup time vs memory**: 1.2x (minimo)
- **Tradeoff memoria**: 5.8x mas RAM
- El cuello de botella NO es el parsing JSON sino `emoji.emoji_list()` que se invoca 117K veces. Por eso la diferencia de tiempo es minima entre ambos enfoques. La ganancia real del enfoque time esta en el parser (orjson), pero `emoji_list()` domina el costo total.

### Q3 - Top menciones
- **Speedup time vs memory**: 2.3x mas rapido
- **Tradeoff memoria**: 5.7x mas RAM
- Mejor caso de optimizacion: regex pre-compilado + orjson logran el mayor speedup. El parsing JSON + regex son operaciones que orjson y `re.compile()` optimizan muy bien.

## Posible optimizacion para Q2

El cuello de botella de Q2 es `emoji.emoji_list()`, no el parsing JSON. Una alternativa seria pre-computar un `set` con todos los emojis conocidos desde `emoji.EMOJI_DATA` y hacer un simple check `char in set` (O(1)) por cada caracter del content, en lugar de invocar `emoji_list()` que internamente ejecuta regex y crea objetos dict por cada match.

```python
EMOJI_SET = set(emoji.EMOJI_DATA.keys())
for char in content:
    if char in EMOJI_SET:
        emoji_counter[char] += 1
```

Sin embargo, este approach **no detecta emojis compuestos** (como banderas o emojis con skin tone modifiers que son multiples codepoints). Se decidio mantener `emoji.emoji_list()` para garantizar precision en la deteccion, priorizando correctitud sobre velocidad.

## Herramientas de profiling

El challenge recomienda `memory-profiler`/`memray` para memoria y `py-spy`/`Python Profilers` para tiempo. Se eligio:

| Herramienta | Elegida | Alternativa | Razon |
|-------------|---------|-------------|-------|
| Memoria | `memory-profiler` | `memray` | memray no soporta Windows (solo Linux/macOS) |
| Tiempo | `cProfile` | `py-spy` | py-spy es CLI externo, no se integra con notebook. cProfile se usa directo desde codigo |

- **`cProfile`** (Python Profilers): profiler deterministico integrado en Python. Instrumenta cada llamada a funcion, lo que agrega overhead (~2-5x) pero permite analisis detallado desde codigo.
- **`py-spy`**: sampling profiler en Rust con overhead minimo (<5%). Ideal para produccion pero requiere adjuntarse externamente a un proceso (`py-spy record --pid 1234`), lo cual no es practico en un notebook.
- **`memory-profiler`**: mide pico de RAM via polling en proceso separado. Unica opcion viable en Windows de las recomendadas.
- **`memray`**: mas moderno y preciso que memory-profiler, pero solo compatible con Linux/macOS.

## Conclusion

El tradeoff es consistente: las versiones `*_time` usan ~5-6x mas memoria pero son ~1.2-2.3x mas rapidas. La diferencia clave entre enfoques:

- **Time**: `orjson` (Rust) + `readlines()` bulk = rapido, alto RAM
- **Memory**: `json` (stdlib) + iteracion linea a linea = lento, bajo RAM