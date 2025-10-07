'''
Custom exceptions for argument handling in CLI applications.
'''

# Exception raised when not enough arguments are provided.
class InsufficientArgsException(Exception):
    def __init__(self, 
                 provided=None,
                 expected=None,
                 message="Insufficient arguments provided. Use -h for help.", 
                 error_code=None):
        super().__init__(message)
        self.error_code = error_code
        self.provided = provided
        self.expected = expected

    def __str__(self):
        msg = super().__str__()
        if self.provided is not None and self.expected is not None:
            if isinstance(self.provided, list):
                self.provided = len(self.provided)
            msg += f" (Provided: {self.provided}, Expected: {self.expected})"
        if self.error_code is not None:
            return f"[{self.error_code}] {msg}"
        return msg
...

# Exception raised when invalid arguments are provided.
class InvalidArgsException(Exception):
    def __init__(self,
                 args=None,
                 message="Invalid argument(s) provided. Use -h for help."):
        super().__init__(message)
        self.invalid_args = args
        self.message = message

    def __str__(self):
        msg = self.message
        if self.invalid_args is not None:
            msg += f" (args: {', '.join(map(str, self.invalid_args))})"
        return msg
...