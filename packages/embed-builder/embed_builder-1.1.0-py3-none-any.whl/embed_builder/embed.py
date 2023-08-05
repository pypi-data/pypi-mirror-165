from datetime import datetime

_TITLE_CHAR_LIMIT = 256
_DESCRIPTION_CHAR_LIMIT = 4096
_FIELD_LIMIT = 25
_FIELD_NAME_CHAR_LIMIT = 256
_FIELD_VALUE_CHAR_LIMIT = 1024
_FOOTER_TEXT_CHAR_LIMIT = 2048
_AUTHOR_NAME_CHAT_LIMIT = 256


class Embed:
    _embed: dict
    _field_count: int

    def __init__(self):
        self._embed = {}
        self._field_count = 0

    def set_title(self, title: str):
        """
        Sets the title of the embed.

        :param title: The embed title
        """
        assert len(title) <= _TITLE_CHAR_LIMIT, f"Title must not exceed {_TITLE_CHAR_LIMIT}"

        self._embed["title"] = title
        return self

    def set_description(self, description: str):
        """
        Sets the description of the embed.

        :param description: The embed description
        """
        assert len(description) <= _DESCRIPTION_CHAR_LIMIT, f"Description must not exceed {_DESCRIPTION_CHAR_LIMIT}"

        self._embed["description"] = description
        return self

    def set_color(self, color: int):
        """
        Sets the embed color.

        :param color: The embed color in decimal format
        """
        self._embed["color"] = color
        return self

    def set_url(self, url: str):
        """
        Sets the embed URL.

        :param url: The embed URL
        """
        self._embed["url"] = url
        return self

    def set_footer(self, text: str, *, icon_url: str = None):
        """
        Sets the embed footer.

        :param text: The footer text
        :param icon_url: The footer icon URL
        """
        assert len(text) <= _FOOTER_TEXT_CHAR_LIMIT, f"Footer text must not exceed {_FOOTER_TEXT_CHAR_LIMIT}"

        self._embed["footer"] = {
            "text": text
        }

        if icon_url:
            self._embed["footer"]["icon_url"] = icon_url

        return self

    def set_image(self, url: str):
        """
        Sets the embed image.

        :param url: The image URL
        """
        self._embed["image"] = {
            "url": url
        }

        return self

    def set_thumbnail(self, url: str):
        """
        Sets the embed thumbnail image.

        :param url: The thumbnail URL
        """
        self._embed["thumbnail"] = {
            "url": url
        }

        return self

    def set_timestamp(self, timestamp: datetime = None):
        """
        Sets the embed timestamp, uses the current time if argument is omitted.

        :param timestamp: ISO8601-formatted timestamp
        """
        self._embed["timestamp"] = datetime.utcnow().isoformat() if not timestamp else timestamp.isoformat()
        return self

    def set_author(self, name: str, *, url: str = None, icon_url: str = None):
        """
        Sets the embed author.

        :param name: The author name
        :param url: The author URL
        :param icon_url: The author icon URL
        """
        assert len(name) <= _AUTHOR_NAME_CHAT_LIMIT, f"Author name must not exceed {_AUTHOR_NAME_CHAT_LIMIT}"

        self._embed["author"] = {
            "name": name
        }

        if url:
            self._embed["author"]["url"] = url

        if icon_url:
            self._embed["author"]["icon_url"] = icon_url

        return self

    def add_field(self, name: str, value: str, *, inline: bool = False):
        """
        Adds a field to the embed.

        :param name: The field title
        :param value: The field content
        :param inline: Whether the field should display inline
        """
        assert self._field_count < _FIELD_LIMIT, f"Number of fields is at maximum of {_FIELD_LIMIT}"
        assert len(name) <= _FIELD_NAME_CHAR_LIMIT, f"Field name must not exceed {_FIELD_NAME_CHAR_LIMIT}"
        assert len(value) <= _FIELD_VALUE_CHAR_LIMIT, f"Field value must not exceed {_FIELD_VALUE_CHAR_LIMIT}"

        if "fields" not in self._embed:
            self._embed["fields"] = []

        self._embed["fields"].append({
            "name": name,
            "value": value,
            "inline": inline
        })

        self._field_count += 1

        return self

    def build(self) -> dict:
        """
        Returns the embed dictionary.
        """
        return self._embed
