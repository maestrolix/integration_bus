from enum import StrEnum, auto, IntEnum


class RunnerStatus(StrEnum):
    READY = auto()          # Готов к исполнению
    RUNNING = auto()        # Исполняется ...


class RunnerExecutionRequestStatus(StrEnum): 
    IN_PROGRESS = auto()        # Запрос в исполнении.
    BLOCKED = auto()            # Во время исполнения запроса раннер или зависимые ранеры, были заблокированы.
    ERROR = auto()              # Какой-то ранер выполнился с ошибкой.
    SUCCESS = auto()            # Все ранеры выполнились успешно.
    KEY_NOT_FOUND = auto()      # Раннер не был найден в БД.
    

class RunnerEventStatus(StrEnum): 
    IN_PROGRESS = auto()    # Раннер в исполнении.
    
    SUCCESS = auto()        # Раннер выполнился успешно.
    ERROR = auto()          # Раннер завершился с ошибкой.                         
    NOT_EXEC = auto()       # Раннер не выполнялся из-за ошибки прошлого раннера.   
    
    BLOCKED = auto()        # Раннер был заблокирован на момент исполнения запроса.                                   
    FREE = auto()           # Ранер был свободен на момент исполнения запроса.
     
    
    
class RunnerLogStatus(StrEnum): 
    INFO = auto()           # Обычная информация
    WARNING = auto()        # Опасная информация
    ERROR = auto()          # Обрабатываемая ошибка
    CRITICAL = auto()       # Необрабатываемся ошибка
    

class RunnerLogType(StrEnum): 
    ROUTER = auto()         # Лог роутера
    CONNETION = auto()      # Лог соединения
    RUNNER = auto()         # Лог раннера


class EisKind(StrEnum):
    """
    Вид ВИС. Более общее понятие, чем тип ВИС.
    
    Вид ВИС может объединять в себе различные типы ВИС.
    Определяет интерфейс соединения, который следует использовать для
    взаимодействия с данной ВИС.
    """
    DATABASE = auto()
    HTTP = auto()


class EisType(StrEnum):
    """
    Тип ВИС.
    
    Точно определяет тип соединения, который следует использовать
    для взаимодействия с данной ВИС.
    """
    HTTP_NO_AUTH = auto()
    HTTP_BASIC_AUTH = auto()
    HTTP_JWT_AUTH = auto()
    DATABASE_AUTH = auto()


EIS_TYPES = {
    EisKind.DATABASE: [EisType.HTTP_NO_AUTH, EisType.HTTP_BASIC_AUTH, EisType.HTTP_JWT_AUTH],
    EisKind.HTTP: [EisType.DATABASE_AUTH]
}


class VisitedState(IntEnum):
    NOT_VISITED = auto()
    VISITED = auto()
    IN_STACK = auto()