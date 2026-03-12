# Checklist de Implementación: VSL -> Survey -> Calendario (Jorge Vergara)

Esta hoja consolida todos los pasos necesarios para configurar el flujo de alta conversión en GoHighLevel, donde el prospecto califica su oportunidad mediante una encuesta antes de agendar su llamada.

## Fase 1: Optimización de la Encuesta (Survey)
- [x] **Eliminar Slide de Horarios:** Quitar las preguntas de "Días/Horas de contacto preferidos" (Slide 6 original) de la encuesta.
- [x] **Cambiar CTA Final:** Modificar el texto del botón de la última diapositiva a "VER HORARIOS DISPONIBLES".
- [ ] **Acortar Disclaimers (Términos y Condiciones):** Reemplazar los textos largos de las casillas de verificación por las versiones optimizadas (ver abajo en la sección de recursos).
- [ ] **Configurar Redirección "On Submit":** En las opciones de la encuesta, configurar que al enviar redirija a la URL del siguiente paso (la página del calendario).

## Fase 2: Configuración de la Landing Page del Calendario
- [ ] **Insertar Calendario:** Asegurarse de que el elemento del calendario esté correctamente incrustado en la página de destino post-encuesta.
- [ ] **Activar "Sticky Contact":** Entrar a la configuración de la Landing Page (Settings) y encender la opción "Sticky Contact" para que autocompiete el nombre, correo y teléfono del lead que viene de la encuesta.

## Fase 3: Automatización de Valoración de Oportunidad (Flujo en GHL)
- [ ] **Crear Workflow Nuevo:** Configurar el Trigger para que sea "Survey Submitted" y seleccionar la encuesta de Jorge.
- [ ] **Lógica Condicional de Calificación (If/Else):**
  - **Rama A (Alto Valor):** *Ejemplo:* Si los ingresos o dependientes cumplen ciertas características -> Actualizar oportunidad en el Pipeline con un "Value" alto (ej. $1000) y etiqueta "Hot Lead".
  - **Rama B (Valor Medio):** Si cumple características medias -> Valor medio (ej. $500).
  - **Rama C (Descalificado/Bajo Valor):** Si no califica o responde indicadores negativos -> Valor $0 y etiqueta "Baja Prioridad".
- [ ] **Recordatorio de Abandono (Opcional pero recomendado):** Configurar un paso de "Wait" (Esperar) por 15 minutos. Si la persona no ha agendado en el calendario tras llenar el Survey, enviar SMS automático: *"Hola [Nombre], vi que llenaste el formulario pero no confirmaste la fecha para la llamada. ¿Tuviste algún problema? Toca aquí para ver los horarios: [Link]"*.

---

### Recursos de Apoyo

#### Nuevos textos cortos para las casillas de consentimiento (Disclaimers)

**Casilla 1 (Transaccional):**
> Acepto recibir mensajes de texto (SMS) recordatorios de mis citas, servicios e información de mi cuenta. *(Pueden aplicar tarifas de datos. Responde STOP para cancelar).*

**Casilla 2 (Promocional):**
> Acepto recibir mensajes de texto (SMS) promocionales, incluyendo nuevas ofertas, descuentos y actualizaciones. *(Pueden aplicar tarifas de datos. Responde STOP para cancelar).*
