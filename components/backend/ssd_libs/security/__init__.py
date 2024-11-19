from .hasher import Hasher
from .auth_strategies import JWT



__all__ = ['Hasher', 'jwt_strategy']
__version__ = '1.0.0'

jwt_strategy = JWT()