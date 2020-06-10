import uuid


class UUIDConverter:
    """
    UUID converter
    """

    regex = "[0-9a-f]{8}-?[0-9a-f]{4}-?4[0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}"

    @staticmethod
    def to_python(value: str) -> uuid.UUID:
        return uuid.UUID(value)

    @staticmethod
    def to_url(value: str) -> str:
        return uuid.UUID(value).hex
