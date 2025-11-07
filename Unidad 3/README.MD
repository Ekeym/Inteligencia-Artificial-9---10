# 🧩 Instrucciones de Asignación: Sistema Experto *Evidence-03*

En esta tarea, crearás un **Sistema Experto (SE)** diseñado para ayudar en el **diagnóstico de enfermedades respiratorias**.
Este sistema utilizará **Inteligencia Artificial** para simular el proceso de razonamiento de un médico especialista, mejorando la **precisión** y **eficiencia** de los diagnósticos.

A continuación, encontrarás las instrucciones detalladas para completar cada componente.

---

## 1. 💻 Interfaz de Usuario

La interfaz de usuario es una parte crucial de tu sistema experto.
Es el punto de interacción entre el usuario (médico, personal sanitario o paciente) y el sistema.
Debe ser **intuitiva, amigable y eficiente**.

### 🔹 Características clave a incluir

#### Entrada de síntomas y signos

Crea un formulario o conjunto de preguntas para ingresar datos del paciente:

* **Datos demográficos:**

  * Edad
  * Sexo
* **Síntomas principales:**

  * Tos (tipo y duración)
  * Disnea (dificultad para respirar)
  * Sibilancias
  * Dolor en el pecho
  * Fiebre
  * Fatiga
* **Factores de riesgo:**

  * Antecedentes de tabaquismo
  * Exposición a contaminantes
  * Antecedentes alérgicos o familiares
* **Hallazgos físicos / de laboratorio:**

  * Auscultación (crepitantes, ronquidos)
  * Saturación de oxígeno
  * Radiografías o pruebas de laboratorio (hemograma, PCR)

#### Presentación del diagnóstico

Incluye una sección que muestre los resultados del diagnóstico:

* **Diagnóstico(s) presuntivo(s):**
  Mostrar con un factor de certeza o probabilidad
  Ejemplo: `Asma (certeza 85%)`
* **Recomendaciones:**
  Sugerir pruebas adicionales o tratamientos iniciales.

#### Módulo de explicación

Agrega una función que explique **cómo** el sistema llegó al diagnóstico.
Ejemplo:

> “Se activaron las reglas relacionadas con fiebre alta + crepitantes en la auscultación + edad avanzada.”

---

## 2. 🧠 Base de Conocimientos (BC)

La **Base de Conocimientos** almacena toda la información necesaria para el diagnóstico.
Debe estar estructurada de forma clara y precisa.

### 🔹 Elementos a incluir

#### Hechos (datos)

Organiza la información en dos categorías:

1. **Conocimiento estático:**
   Define enfermedades como **asma**, **bronquitis**, **EPOC**, **neumonía** y **COVID-19**, junto con sus síntomas y factores de riesgo.
2. **Datos del paciente:**
   Incluir los síntomas y signos que el usuario ingrese, por ejemplo:

   ```
   Fiebre = Sí  
   Duración de la tos = Más de 7 días
   ```

#### Reglas de producción

Desarrolla reglas que representen el conocimiento del experto.
(Ver sección 3 para estructura).

#### Manejo de incertidumbre

Implementa métodos para gestionar incertidumbre, como:

* **Factores de certeza (CF)**
* **Lógica difusa**

---

## 3. ⚙️ Reglas de Derivación (Motor de Inferencia)

El **motor de inferencia** es el núcleo del sistema experto, donde ocurre el razonamiento.
Crea reglas de derivación que formalicen el conocimiento médico.

### 🔹 Ejemplos de reglas

#### 🫁 Asma

```
SI (Sibilancias = Sí)
Y (Tos por la noche o ejercicio = Sí)
Y (Antecedentes de alergia o atopia = Sí)
ENTONCES (Diagnóstico: Asma) [CF = 0.9]
```

#### 🌡️ Neumonía

```
IF (Fiebre > 38.5°C = Sí)
Y (Tos productiva con expectoración = Sí)
Y (Dificultad respiratoria aguda = Sí)
Y (Crepitantes en la auscultación = Sí)
ENTONCES (Diagnóstico: Neumonía) [CF = 0.85]
```

#### 🤧 Bronquitis aguda

```
SI (Tos seca o productiva = Sí)
Y (Infección previa del tracto respiratorio superior = Sí)
Y (Duración de síntomas < 3 semanas = Sí)
Y (Signos de consolidación pulmonar en Rx = No)
ENTONCES (Diagnóstico: Bronquitis aguda) [CF = 0.75]
```

### 🔹 Mecanismos de inferencia

#### Encadenamiento hacia adelante

* Inicia con los **hechos** (síntomas ingresados).
* Aplica reglas hasta derivar un diagnóstico final.
  Ideal cuando hay muchos datos iniciales.

#### Encadenamiento hacia atrás

* Inicia con una **hipótesis** (“¿Tiene asma?”).
* Busca los hechos necesarios para confirmarla o refutarla.
  Ideal para consultas dirigidas.

---

## 4. ✅ Validación de las Reglas

La validación garantiza que el sistema sea **confiable, preciso y robusto**.

### 🔹 Fases de validación

#### 1. Validación con el experto (verificación)

* Revisa cada regla con un **médico especialista**.
* Asegura consistencia, integridad y actualización médica.

#### 2. Pruebas con casos clínicos

Evalúa el sistema con **casos reales** y mide:

* **Sensibilidad:** Verdaderos positivos
* **Especificidad:** Verdaderos negativos
* **Precisión:** Porcentaje de diagnósticos correctos

#### 3. Ajuste y refinamiento (iterativo)

Proceso iterativo:

> Validar → Detectar fallas → Ajustar reglas → Revalidar

Objetivo: alcanzar **>90% de precisión**.

#### 4. Validación cruzada

Si usas aprendizaje automático, divide los datos en subconjuntos de **entrenamiento** y **prueba** para evitar sobreajuste.

---

## 🎯 Conclusión

Siguiendo estas instrucciones, podrás crear un **sistema experto integral** para el diagnóstico de enfermedades respiratorias.

> 💡 *¡Buena suerte! Y no dudes en hacer preguntas si necesitas aclaraciones.*

---
