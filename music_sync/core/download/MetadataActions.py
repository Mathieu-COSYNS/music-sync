import csv
from copy import deepcopy
from io import StringIO

from yt_dlp import MetadataParserPP


class MetadataActions:
    def __init__(self) -> None:
        self._actions: list[MetadataParserPP] = []

    def add(self, action: MetadataParserPP):
        MetadataParserPP.validate_action(*action)
        self._actions.append(action)

    def add_interpret(self, inp: str, out: str):
        self.add((MetadataParserPP.Actions.INTERPRET, inp, out))

    def add_replace(self, fields: str | list[str], old: str, new: str):
        if isinstance(fields, str):
            fields_list = fields.split(",")
        elif isinstance(fields, list):
            fields_list = fields
        else:
            raise ValueError(f"{fields} in invalid")

        if len(fields_list) == 1:
            self.add((MetadataParserPP.Actions.REPLACE, fields_list[0], old, new))
        else:
            for field in fields_list:
                self.add_replace(field, old, new)

    def parse(self, metadata: str | list[str], type_="interpret"):
        if isinstance(metadata, str):
            try:
                reader = csv.reader(StringIO(metadata), delimiter=" ")
            except Exception as err:
                raise ValueError(f"{metadata} is invalid; {err}") from err
            for row in reader:
                if type_ == "interpret":
                    try:
                        self.add_interpret(*row)
                    except Exception as err:
                        raise ValueError(f"{metadata} is invalid; {err}") from err
                elif type_ == "replace":
                    try:
                        self.add_replace(*row)
                    except Exception as err:
                        raise ValueError(f"{metadata} is invalid; {err}") from err
                else:
                    raise ValueError(f"{type_} is unknown")
        elif isinstance(metadata, list):
            for metadata_item in metadata:
                self.parse(metadata_item, type_)
        else:
            raise ValueError(f"{metadata} in invalid")

    @property
    def actions(self):
        return self._actions

    def __repr__(self) -> str:
        return "[" + " ".join(repr(action) for action in self.actions) + "]"

    def __deepcopy__(self, memo):
        deepcopy_method = self.__deepcopy__
        self.__deepcopy__ = None
        cp = deepcopy(self, memo)
        self.__deepcopy__ = deepcopy_method
        cp.__deepcopy__ = deepcopy_method

        cp._actions = []

        for action in self.actions:
            metadata_parser_action, *args = action
            cp._actions.append((metadata_parser_action, *deepcopy(args)))

        return cp
