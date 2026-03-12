"""
⚠️ ADVERTENCIA: CÓDIGO STUB - NO EJECUTABLE ⚠️

Este archivo contiene ÚNICAMENTE código de referencia y ejemplos.
NO se ejecuta directamente por el agente.

Las llamadas MCP reales están COMENTADAS y solo hay simulaciones.

Para implementar llamadas a Notion, consulta el SKILL.md que documenta
las herramientas MCP que el agente debe usar directamente:
- mcp_notion-mcp-server_API-retrieve-a-page
- mcp_notion-mcp-server_API-post-page
- mcp_notion-mcp-server_API-patch-block-children

Este archivo sirve como:
1. Referencia de la estructura de error handling deseada
2. Ejemplo de cómo organizar validaciones
3. Template para futura implementación si se necesita

Helper module para Notion MCP con Error Handling Robusto
Implementa patrones de error-handling-patterns skill
"""

from typing import Optional, Dict, Any, List, Callable, TypeVar
from functools import wraps
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')

# ============================================================================
# CUSTOM ERROR HIERARCHY
# ============================================================================

class NotionError(Exception):
    """Base exception para errores de Notion."""
    def __init__(self, message: str, code: Optional[str] = None, details: Optional[dict] = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}
        
class NotionPermissionError(NotionError):
    """Raised cuando hay error de permisos."""
    def __init__(self, resource: str, page_id: str):
        super().__init__(
            f"No tienes permisos para acceder a {resource}",
            code="PERMISSION_DENIED",
            details={"resource": resource, "page_id": page_id}
        )

class NotionNotFoundError(NotionError):
    """Raised cuando no se encuentra el recurso."""
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            f"{resource} con ID {resource_id} no encontrado",
            code="NOT_FOUND",
            details={"resource": resource, "id": resource_id}
        )

class NotionValidationError(NotionError):
    """Raised cuando la validación falla."""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, code="VALIDATION_ERROR", details=details)

class NotionAPIError(NotionError):
    """Raised cuando la API devuelve un error."""
    def __init__(self, message: str, status_code: Optional[int] = None, details: Optional[dict] = None):
        super().__init__(message, code="API_ERROR", details=details)
        self.status_code = status_code

# ============================================================================
# RETRY WITH EXPONENTIAL BACKOFF
# ============================================================================

def retry(
    max_attempts: int = 3,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """Retry decorator con exponential backoff."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    logger.info(f"Intento {attempt + 1}/{max_attempts}: {func.__name__}")
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = backoff_factor ** attempt
                        logger.warning(
                            f"Error en {func.__name__}, reintentando en {sleep_time}s",
                            extra={"error": str(e), "attempt": attempt + 1}
                        )
                        time.sleep(sleep_time)
                        continue
                    logger.error(f"Falló después de {max_attempts} intentos: {func.__name__}")
                    raise
            if last_exception:
                raise last_exception
            else:
                raise Exception(f"{func.__name__} falló sin excepción")
        return wrapper
    return decorator

# ============================================================================
# GRACEFUL DEGRADATION
# ============================================================================

def with_fallback(
    primary: Callable[[], T],
    fallback: Callable[[], T],
    log_error: bool = True
) -> T:
    """Try primary function, fall back to fallback on error."""
    try:
        return primary()
    except Exception as e:
        if log_error:
            logger.error(f"Primary function failed: {e}, usando fallback")
        return fallback()

# ============================================================================
# NOTION MCP WRAPPERS
# ============================================================================

class NotionMCPHelper:
    """Helper class con wrappers robustos para Notion MCP."""
    
    @staticmethod
    def validate_page_id(page_id: str) -> None:
        """Valida que el page_id tenga formato correcto."""
        if not page_id:
            raise NotionValidationError("page_id no puede estar vacío")
        
        # UUIDs tienen 32 caracteres hex + 4 guiones = 36 caracteres
        if len(page_id.replace("-", "")) != 32:
            raise NotionValidationError(
                f"page_id tiene formato inválido: {page_id}",
                details={"page_id": page_id}
            )
    
    @staticmethod
    def validate_block_structure(block: Dict[str, Any]) -> None:
        """Valida que un bloque Notion tenga la estructura correcta."""
        if "type" not in block:
            raise NotionValidationError(
                "El bloque debe tener campo 'type'",
                details={"block": block}
            )
        
        block_type = block["type"]
        if block_type not in block:
            raise NotionValidationError(
                f"El bloque de tipo '{block_type}' debe tener campo '{block_type}'",
                details={"block": block}
            )
    
    @staticmethod
    @retry(max_attempts=3, exceptions=(NotionAPIError,))
    def safe_retrieve_page(mcp_client, page_id: str) -> Optional[Dict[str, Any]]:
        """
        Recupera una página de Notion con validación, retry y error handling.
        
        Returns:
            Dict con datos de la página o None si hay error de permisos
        """
        NotionMCPHelper.validate_page_id(page_id)
        
        logger.info(f"Recuperando página: {page_id}")
        
        try:
            # Aquí iría la llamada real al MCP
            # result = mcp_client.call("mcp_notion-mcp-server_API-retrieve-a-page", {
            #     "page_id": page_id
            # })
            
            # Por ahora simulamos la llamada
            result = {"id": page_id, "properties": {}}
            logger.info(f"Página recuperada exitosamente: {page_id}")
            return result
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Detectar errores de permisos
            if "permission" in error_msg or "403" in error_msg:
                logger.warning(f"Sin permisos para página: {page_id}")
                raise NotionPermissionError("página", page_id)
            
            # Detectar errores de not found
            if "not found" in error_msg or "404" in error_msg:
                logger.warning(f"Página no encontrada: {page_id}")
                raise NotionNotFoundError("página", page_id)
            
            # Otros errores de API
            logger.error(f"Error de API en retrieve_page: {e}")
            raise NotionAPIError(str(e), details={"page_id": page_id})
    
    @staticmethod
    @retry(max_attempts=3, exceptions=(NotionAPIError,))
    def safe_create_page(
        mcp_client,
        parent_id: str,
        title: str,
        icon: str = "🎯",
        properties: Optional[Dict] = None
    ) -> str:
        """
        Crea una página en Notion con validación y retry.
        
        Returns:
            page_id de la página creada
        """
        NotionMCPHelper.validate_page_id(parent_id)
        
        if not title:
            raise NotionValidationError("El título no puede estar vacío")
        
        logger.info(f"Creando página: {title} bajo parent: {parent_id}")
        
        # Primero validar que tenemos acceso al parent
        try:
            NotionMCPHelper.safe_retrieve_page(mcp_client, parent_id)
        except NotionPermissionError:
            raise NotionPermissionError("página padre", parent_id)
        except NotionNotFoundError:
            raise NotionNotFoundError("página padre", parent_id)
        
        try:
            # Aquí iría la llamada real al MCP
            # result = mcp_client.call("mcp_notion-mcp-server_API-post-page", {
            #     "parent": {"page_id": parent_id},
            #     "icon": {"emoji": icon},
            #     "properties": {
            #         "title": [{"text": {"content": title}}]
            #     }
            # })
            
            # Simulación
            new_page_id = "new-page-123"
            logger.info(f"Página creada exitosamente: {new_page_id}")
            return new_page_id
            
        except Exception as e:
            logger.error(f"Error creando página: {e}")
            raise NotionAPIError(
                f"Error al crear página: {str(e)}",
                details={"parent_id": parent_id, "title": title}
            )
    
    @staticmethod
    @retry(max_attempts=2, exceptions=(NotionAPIError,))
    def safe_append_blocks(
        mcp_client,
        block_id: str,
        children: List[Dict[str, Any]]
    ) -> bool:
        """
        Añade bloques a una página con validación.
        
        Returns:
            True si se añadieron exitosamente
        """
        NotionMCPHelper.validate_page_id(block_id)
        
        if not children:
            raise NotionValidationError("La lista de children no puede estar vacía")
        
        # Validar cada bloque
        for i, block in enumerate(children):
            try:
                NotionMCPHelper.validate_block_structure(block)
            except NotionValidationError as e:
                raise NotionValidationError(
                    f"Bloque #{i} inválido: {e}",
                    details={"block_index": i, "block": block}
                )
        
        logger.info(f"Añadiendo {len(children)} bloques a {block_id}")
        
        try:
            # Aquí iría la llamada real al MCP
            # result = mcp_client.call("mcp_notion-mcp-server_API-patch-block-children", {
            #     "block_id": block_id,
            #     "children": children
            # })
            
            logger.info(f"Bloques añadidos exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error añadiendo bloques: {e}")
            raise NotionAPIError(
                f"Error al añadir bloques: {str(e)}",
                details={"block_id": block_id, "num_children": len(children)}
            )

# ============================================================================
# WORKFLOW HELPERS
# ============================================================================

def create_offer_page_with_validation(
    mcp_client,
    parent_id: str,
    client_name: str,
    offer_content: Dict[str, Any]
) -> Optional[str]:
    """
    Workflow completo para crear una página de oferta con manejo de errores robusto.
    
    Returns:
        page_id de la página creada o None si falló
    """
    logger.info(
        f"Iniciando creación de oferta para: {client_name}",
        extra={"parent_id": parent_id, "client": client_name}
    )
    
    try:
        # Paso 1: Validar parent
        logger.info("Validando parent page...")
        NotionMCPHelper.safe_retrieve_page(mcp_client, parent_id)
        
        # Paso 2: Crear página
        logger.info("Creando página de oferta...")
        title = f"🎯 Oferta del Agente - {client_name}"
        page_id = NotionMCPHelper.safe_create_page(
            mcp_client,
            parent_id,
            title,
            icon="🎯"
        )
        
        # Paso 3: Añadir contenido
        logger.info("Añadiendo contenido a la página...")
        blocks = offer_content.get("blocks", [])
        
        if blocks:
            NotionMCPHelper.safe_append_blocks(mcp_client, page_id, blocks)
        
        logger.info(f"✅ Oferta creada exitosamente: {page_id}")
        return page_id
        
    except NotionPermissionError as e:
        logger.error(
            f"❌ Error de permisos: {e.details}",
            extra={"error_code": e.code, "details": e.details}
        )
        return None
        
    except NotionNotFoundError as e:
        logger.error(
            f"❌ Recurso no encontrado: {e.details}",
            extra={"error_code": e.code, "details": e.details}
        )
        return None
        
    except NotionValidationError as e:
        logger.error(
            f"❌ Error de validación: {e.details}",
            extra={"error_code": e.code, "details": e.details}
        )
        return None
        
    except NotionAPIError as e:
        logger.error(
            f"❌ Error de API: {e.details}",
            extra={"error_code": e.code, "details": e.details}
        )
        return None
        
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        return None

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Ejemplo de uso
    print("NotionMCPHelper - Error Handling Module")
    print("=" * 50)
    
    # Simular cliente MCP
    class MockMCPClient:
        pass
    
    mcp = MockMCPClient()
    
    # Ejemplo 1: Validar page_id
    try:
        NotionMCPHelper.validate_page_id("invalid")
    except NotionValidationError as e:
        print(f"✓ Validación funcionando: {e}")
    
    # Ejemplo 2: Crear oferta con error handling
    result = create_offer_page_with_validation(
        mcp,
        parent_id="12345678-1234-1234-1234-123456789012",
        client_name="Test Client",
        offer_content={"blocks": []}
    )
    
    print(f"Resultado: {result}")
