from logger import Logger


class File:
    __logger = Logger.get_logger()

    @classmethod
    def read_file(cls, filename):
        content = None
        try:
            cls.__logger.info(f'reading file: {filename}')
            with open(filename, 'r') as file:
                content = file.read()
        except Exception as exception:
            print(exception)
        finally:
            return content
