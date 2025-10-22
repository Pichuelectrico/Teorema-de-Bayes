# Instrucciones de Uso del Generador de Texto con Teorema de Bayes

Este programa genera texto utilizando modelos de n-gramas de caracteres (2, 3 y 4 caracteres) y bigramas de palabras, basados en el libro "El Principito".

## Requisitos

- Python 3.6 o superior
- No se requieren dependencias externas

## Archivos Necesarios

1. `text_generator.py` - El script principal del generador
2. `book.txt` - El texto de "El Principito" (ya incluido en el repositorio)

## Cómo Ejecutar el Programa

1. Abre una terminal en el directorio del proyecto
2. Ejecuta el siguiente comando:

```bash
python text_generator.py
```

## Funcionamiento del Programa

El programa realiza lo siguiente:

1. **Preprocesamiento del texto**:
   - Convierte todo el texto a minúsculas
   - Elimina tildes y caracteres especiales
   - Elimina signos de puntuación
   - Normaliza los espacios en blanco

2. **Entrenamiento de modelos**:
   - Genera modelos de n-gramas de caracteres (para n=2,3,4)
   - Genera un modelo de bigramas de palabras

3. **Generación de texto**:
   - **Basado en caracteres**: Genera texto a partir de secuencias de 1-3 caracteres iniciales
   - **Basado en palabras**: Genera texto a partir de una palabra inicial

## Ejemplos de Uso

### Generación basada en caracteres

```python
generator = TextGenerator(texto)
generator.train_ngram_models()

# Generar 250 caracteres comenzando con "el" (usando bigramas)
print(generator.generate_from_chars("el", 250))

# Generar 250 caracteres comenzando con "el_" (usando trigramas)
print(generator.generate_from_chars("el_", 250))

# Generar 250 caracteres comenzando con "el_p" (usando 4-gramas)
print(generator.generate_from_chars("el_p", 250))
```

### Generación basada en palabras

```python
generator = TextGenerator(texto)
generator.train_word_bigram_model()

# Generar 50 palabras comenzando con "el_principito"
print(generator.generate_from_words("el_principito", 50))

# Generar 50 palabras comenzando con "el_rey_hablo_con"
print(generator.generate_from_words("el_rey_hablo_con", 50))
```

## Notas Importantes

- El texto generado es estocástico, por lo que puede variar en cada ejecución
- Para obtener mejores resultados, se recomienda usar secuencias iniciales que aparezcan frecuentemente en el texto
- El modelo de caracteres tiende a generar texto más coherente a medida que aumenta el valor de n (2, 3, o 4)
- El modelo de palabras genera texto más significativo pero puede ser más repetitivo

## Personalización

Puedes modificar el código para:
- Cambiar el texto de entrada (sustituyendo `book.txt` por otro archivo)
- Ajustar la longitud del texto generado
- Probar con diferentes secuencias iniciales
- Modificar los parámetros de los modelos
