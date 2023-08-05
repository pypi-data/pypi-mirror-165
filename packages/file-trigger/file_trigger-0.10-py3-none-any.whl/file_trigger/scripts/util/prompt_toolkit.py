import os.path
from prompt_toolkit.validation import Validator, ValidationError

""" Some validation helpers that really should be part of prompt_toolkit """


class ComposableValidator(Validator):
    def __or__(self, other):
        return OrValidator(self, other)

    def __and__(self, other):
        return AndValidator(self, other)

    def __not__(self):
        return NotValidator(self)


class OrValidator(ComposableValidator):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def validate(self, document):
        try:
            self.left.validate(document)
        except ValidationError as left_err:
            try:
                self.right.validate(document)
            except ValidationError:
                raise left_err


class AndValidator(ComposableValidator):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def validate(self, document):
        self.left.validate(document)
        self.right.validate(document)


class NotValidator(ComposableValidator):
    def __init__(self, other):
        self.other = other

    def validate(self, document):
        try:
            self.other.validate(document)
        except ValidationError:
            return
        raise ValidationError("Didn't raise validation error")


class FileExists(ComposableValidator):
    def __init__(self, file_only=False):
        self.file_only = file_only

    def validate(self, document):
        text = document.text
        if len(text) == 0:
            raise ValidationError(message="You must specify an existing file")

        if not os.path.exists(text):
            raise ValidationError(message="File does not exist")

        if self.file_only and not os.path.isfile(text):
            raise ValidationError(message="You must specify a path to a file")


class FileExistsUnder(ComposableValidator):
    def __init__(self, file_name):
        self.file_name = file_name

    def validate(self, document):
        text = document.text
        if len(text) == 0:
            raise ValidationError(message="You must specify an existing file")

        if not os.path.exists(os.path.join(text, self.file_name)):
            raise ValidationError(
                message=f"File {self.file_name} doesn't exist under {text}"
            )
