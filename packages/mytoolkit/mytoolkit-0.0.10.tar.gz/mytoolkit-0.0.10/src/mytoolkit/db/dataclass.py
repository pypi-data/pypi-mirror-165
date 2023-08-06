from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union

from mytoolkit.basic.strings import snake_to_camel

FieldType = TypeVar("FieldType")


class DataClass:
    """
    This class supports converting raw dict into the DataClass instance,
    and vise versa.

    Subclass should override the "define_fields()" method, and define
    the fields using "define_xxx()" methods.

    The "get_data()" and "set_data()" are automatically handled if fields
    are defined properly
    """

    def __init__(self, data: Optional[dict] = None) -> None:
        """
        subclass can override this method, but should keep the second parameter
        as the "data" dict, and all following parameters should be optional
        """
        self._defined_fields = {}
        self._client_visible_fields = []
        self.define_fields()
        if data:
            self.set_data(data)

    def define_fields(self):
        """
        subclass should override this method and define the fields
        """
        pass

    def define(
        self,
        field_name: str,
        field_type: Type[FieldType],
        default: Optional[FieldType] = None,
        visible_to_client: bool = False
    ) -> Optional[FieldType]:
        self._defined_fields[field_name] = field_type
        if visible_to_client:
            self._client_visible_fields.append(field_name)
        return default

    def define_list(
        self,
        field_name: str,
        field_type: Type[FieldType],
        default: Optional[List[FieldType]] = None,
        visible_to_client: bool = False
    ) -> Optional[List[FieldType]]:
        """
        `List` is invariant, which means an instance of List[subtype]
        CANNOT be used in a place where List[supertype] is expected.
        If you need this feature, you should use `tuple`
        """
        self._defined_fields[field_name] = field_type
        if visible_to_client:
            self._client_visible_fields.append(field_name)
        return default

    def define_tuple(
        self,
        field_name: str,
        field_type: Type[FieldType],
        default: Optional[Tuple[FieldType, ...]] = None,
        visible_to_client: bool = False
    ) -> Optional[Tuple[FieldType, ...]]:
        self._defined_fields[field_name] = field_type
        if visible_to_client:
            self._client_visible_fields.append(field_name)
        return default

    def define_str(self, field_name: str, default: Optional[str] = None, visible_to_client: bool = False):
        return self.define(field_name, str, default, visible_to_client)

    def define_int(self, field_name: str, default: Optional[int] = None, visible_to_client: bool = False):
        return self.define(field_name, int, default, visible_to_client)

    def define_float(self, field_name: str, default: Optional[float] = None, visible_to_client: bool = False):
        return self.define(field_name, float, default, visible_to_client)

    def define_bool(self, field_name: str, default: Optional[bool] = None, visible_to_client: bool = False):
        return self.define(field_name, bool, default, visible_to_client)

    def define_dict(
        self,
        field_name: str,
        field_type: Type[FieldType] = Any,
        default: Optional[Dict[str, FieldType]] = None,
        visible_to_client: bool = False
    ):
        """
        This method is used when the keys are dynamic

        For example, a dict with user_id -> user_name
        {
            "1": "Bob",
            "2": "Alice
        }

        And this is an example of static keys
        {
            "user": [
                {
                    "id": "1",
                    "name": "Bob"
                },
                {
                    "id": "2",
                    "name": "Alice"
                }
            ]
        }

        Dynamic-key dict cannot be properly typed, so is often used in a small
        scope, where you can easily figure out the meaning of the key and value.

        Static-key dict, we recommend to convert it to a class,
        so that it's properly typed, and can be used in a large scope.
        """
        return self.define(field_name, Dict[str, field_type], default, visible_to_client)

    def _serialize_field_value(self, field_value: Any, field_type: Any, for_client: bool = False) -> Any:
        if isinstance(field_value, (list, tuple, set)):
            ret = [self._serialize_field_value(v, type(v), for_client) for v in field_value]
        elif isinstance(field_value, dict):
            ret = {
                k: self._serialize_field_value(v, type(v), for_client)
                for k, v in field_value.items()
            }
        elif isinstance(field_value, Enum):
            ret = field_value.value
        elif issubclass(field_type, DataClass):
            ret = field_value.get_data(for_client)
        else:
            ret = field_value

        return ret

    def get_data(self, for_client: bool = False) -> Dict[Any, Any]:
        """
        Create raw dict based on the fields
        :return: A dict with all the data
        """
        ret = {}
        for (field_name, field_type) in self._defined_fields.items():
            if for_client and field_name not in self._client_visible_fields:
                continue

            field_value = getattr(self, field_name)
            if field_value is None:
                continue

            final_field_name = field_name
            if for_client:
                final_field_name = snake_to_camel(field_name)

            ret[final_field_name] = self._serialize_field_value(field_value, field_type, for_client)
        return ret

    def _get_data_class_from_key(self, key: str):
        """
        During set_data(), subclass can implement this method
        to define embedded model
        :return: dict[key -> subclass of DataClass]
        """
        try:
            if not self._defined_fields:
                return None
            field_type = self._defined_fields.get(key)
            if not field_type:
                return None
            if issubclass(field_type, DataClass):
                return field_type
            if issubclass(field_type, Enum):
                return field_type
            return None
        except Exception:
            return None

    def _handle_set_array(self, key: str, value: Union[list, tuple]):
        """
        During set_data(), try to convert list value into embedded model
        """
        embedded_data_class = self._get_data_class_from_key(key)
        if not embedded_data_class:
            setattr(self, key, value)
            return

        arr = []
        for item in value:
            embedded_model = embedded_data_class(item)
            arr.append(embedded_model)
        setattr(self, key, arr)

    def _handle_set_dict(self, key: str, value: dict):
        """
        During set_data(), try to convert dict value into embedded model
        """
        embedded_data_class = self._get_data_class_from_key(key)
        if not embedded_data_class:
            setattr(self, key, value)
            return

        embedded_model = embedded_data_class(value)
        setattr(self, key, embedded_model)

    def set_data(self, data: Dict[str, Any]):
        for key in data:
            value = data[key]
            if value is None:
                continue

            if key == "_id":
                self._id = str(value)
                continue

            if isinstance(value, dict):
                self._handle_set_dict(key, value)
                continue

            if isinstance(value, (list, tuple)):
                self._handle_set_array(key, value)
                continue

            field_type = self._get_data_class_from_key(key)
            if field_type:
                # maybe it's an enum
                try:
                    setattr(self, key, field_type(value))
                    continue
                except Exception:
                    pass

            setattr(self, key, value)

    @classmethod
    def get_data_list(cls, ins_list: Tuple["DataClass", ...], for_client: bool = False):
        ret = [i.get_data(for_client) for i in ins_list]
        return ret
