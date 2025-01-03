from functools import wraps
import uuid
from flask import request, g
from ..utils.logger import system_logger, error_logger, log_event
import time
from typing import Callable, Any

def generate_request_id() -> str:
    """Generar un ID único para la petición"""
    return str(uuid.uuid4())

def log_request_info(func: Callable) -> Callable:
    """Decorator para logging de información de peticiones"""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Generar ID único para la petición
        request_id = generate_request_id()
        g.request_id = request_id
        
        # Registrar inicio de petición
        start_time = time.time()
        log_event(
            system_logger,
            f"Request started: {request.method} {request.path}",
            trace_id=request_id,
            extra_data={
                'method': request.method,
                'path': request.path,
                'ip': request.remote_addr,
                'user_agent': request.user_agent.string
            }
        )
        
        try:
            # Ejecutar vista
            response = func(*args, **kwargs)
            
            # Registrar fin de petición exitosa
            duration = time.time() - start_time
            log_event(
                system_logger,
                f"Request completed: {request.method} {request.path}",
                trace_id=request_id,
                extra_data={
                    'duration': f"{duration:.3f}s",
                    'status_code': getattr(response, 'status_code', None)
                }
            )
            
            return response
            
        except Exception as e:
            # Registrar error
            duration = time.time() - start_time
            log_event(
                error_logger,
                f"Request failed: {str(e)}",
                level='ERROR',
                trace_id=request_id,
                extra_data={
                    'duration': f"{duration:.3f}s",
                    'error_type': type(e).__name__,
                    'error_details': str(e)
                }
            )
            raise
            
    return wrapper 