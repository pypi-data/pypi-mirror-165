import logging.handlers


class HTTPHandler(logging.handlers.HTTPHandler):
    def mapLogRecord(self, record):
        """only emit args, with message and level"""
        args = record.args
        if isinstance(args, tuple):
            return {
                "log_message": record.getMessage(),
                "log_levelname": record.levelname,
                "log_levelno": record.levelno,
                "log_args": list(args),
            }
        elif isinstance(args, dict):
            ret = {
                "log_message": record.getMessage(),
                "log_levelname": record.levelname,
                "log_levelno": record.levelno,
            }
            ret.update(**args)
            return ret
        else:
            return {}
