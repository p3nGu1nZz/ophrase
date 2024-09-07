from loguru import logger as log

class Log:
    @staticmethod
    def setup(debug: bool) -> None:
        log.remove()
        log.add(lambda msg: print(msg, end=''), level="DEBUG" if debug else "INFO")

    @staticmethod
    def debug(message: str) -> None:
        log.debug(message)

    @staticmethod
    def info(message: str) -> None:
        log.info(message)

    @staticmethod
    def warning(message: str) -> None:
        log.warning(message)

    @staticmethod
    def error(message: str) -> None:
        log.error(message)

    @staticmethod
    def critical(message: str) -> None:
        log.critical(message)

    @staticmethod
    def start_main_function() -> None:
        log.debug("Starting main function")
