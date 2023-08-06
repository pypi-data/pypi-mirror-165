from copy import deepcopy
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Type, TypeVar, Union

from bson.objectid import ObjectId
from mytoolkit.basic.partition import partition
from mytoolkit.basic.strings import snake_to_camel
from pymongo.collection import ReturnDocument
from pymongo.cursor import Cursor
from pymongo.errors import BulkWriteError
from pymongo.operations import (
    DeleteMany,
    DeleteOne,
    InsertOne,
    ReplaceOne,
    UpdateMany,
    UpdateOne,
)

from ..dataclass import DataClass
from .connection import get_db

if TYPE_CHECKING:
    from pymongo.collection import Collection
    from pymongo.results import (
        BulkWriteResult,
        DeleteResult,
        InsertManyResult,
        InsertOneResult,
        UpdateResult,
    )

SubClassBaseModel = TypeVar("SubClassBaseModel", bound="BaseModel")


class BaseModel(DataClass):
    """
    Wrappers of pymongo, without distributed lock
    Don't embed BaseModel into another BaseModel, use subclass of
    DataClass to represent internal data structure
    """

    COLLECTION = ""

    def __eq__(self, o: object) -> bool:
        if isinstance(o, BaseModel):
            return self._id and o._id and self._id == o._id
        return False

    def __hash__(self) -> int:
        if self._id:
            return str(self._id).__hash__()
        return super().__hash__()

    def __init__(self, data: Optional[dict] = None):
        if not self.__class__.COLLECTION:
            raise NotImplementedError("Model {0} does not define a "
                                      "collection".format(str(type(self))))

        self._id = None
        super().__init__(data=data)

    def get_id(self):
        return None if not self._id else str(self._id)

    @classmethod
    def class_collection(cls) -> "Collection":
        """
        Get the db instance for class methods
        """
        db = get_db()
        return db.get_collection(cls.COLLECTION)

    @classmethod
    def count(cls, filter: dict) -> int:
        """
        ** Will be deprecated in next version of pymongo **
        Count the number of documents in the collection
        """
        replacer = DictReplacer(replace_enum=True, id_to_objectid=True)
        filter = replacer.replace_dict(filter)
        return cls.class_collection().count_documents(filter)

    @classmethod
    def find(
        cls: Type[SubClassBaseModel],
        filter: dict,
        projection: Optional[Union[list, dict]] = None,
        sort: Optional[list] = None,
        skip: int = 0,
        limit: int = 0,
        no_cursor_timeout: bool = False,
        *args,
        **kwargs
    ):
        """
        Wraps the `find()` of pymongo
        Returns a Generator.
        If you set `no_cursor_timeout=True`, but you don't exhaust the generator,
        make sure you call `close()` to close the generator as well as the mongo cursor
        """

        replacer = DictReplacer(replace_enum=True, id_to_objectid=True)
        filter = replacer.replace_dict(filter)

        iter: Cursor = cls.class_collection().find(
            filter, projection=projection, sort=sort, skip=skip,
            limit=limit, no_cursor_timeout=no_cursor_timeout,
            *args, **kwargs
        )

        with iter:
            for data in iter:
                ret = cls()
                ret.set_data(data)
                yield ret

    @classmethod
    def find_one(
        cls: Type[SubClassBaseModel],
        filter: dict,
        projection: Optional[Union[list, dict]] = None,
        *args,
        **kwargs
    ):
        """
        Wraps the "find_one()" of pymongo
        """

        replacer = DictReplacer(replace_enum=True, id_to_objectid=True)
        filter = replacer.replace_dict(filter)

        res = cls.class_collection().find_one(
            filter, projection=projection, *args, **kwargs)
        if not res:
            return None
        ret = cls()
        ret.set_data(res)
        return ret

    @classmethod
    def find_one_and_update(
        cls: Type[SubClassBaseModel],
        filter: Dict[str, Any],
        update: Dict[str, Any],
        return_document: ReturnDocument = ReturnDocument.AFTER,
        **kwargs
    ):
        """
        Wraps the "find_one_and_update()" of pymongo.
        :Parameters:
          - `filter`: A query that matches the document to update.
          - `update`: The update operations to apply or.
          - `return_document`: If :attr:`ReturnDocument.AFTER` (the default), returns the updated
            or inserted document. If :attr:`ReturnDocument.BEFORE`,
            returns the original document before it was updated.
          - `kwargs`: Additional parameters pass to pymongo

        """
        replacer = DictReplacer(replace_enum=True, id_to_objectid=True)
        filter = replacer.replace_dict(filter)

        replacer = DictReplacer(replace_enum=True, omit_none=True, id_to_objectid=True)
        update = replacer.replace_dict(update)

        coll = cls.class_collection()
        res = coll.find_one_and_update(filter, update, return_document=return_document, **kwargs)
        if not res:
            return None

        ret = cls()
        ret.set_data(res)
        return ret

    @classmethod
    def update_many(cls, filter, update, **kwargs) -> "UpdateResult":
        """
        Wraps the "update_many()" of pymongo
        """
        replacer = DictReplacer(replace_enum=True, id_to_objectid=True)
        filter = replacer.replace_dict(filter)

        replacer = DictReplacer(replace_enum=True, omit_none=True, id_to_objectid=True)
        update = replacer.replace_dict(update)

        coll = cls.class_collection()
        return coll.update_many(filter, update, **kwargs)

    @classmethod
    def insert_many(
        cls,
        documents: List[SubClassBaseModel],
        ordered: bool = False,
        ignore_duplicated: bool = False,
        **kwargs
    ) -> Tuple["InsertManyResult", int]:
        """Wraps the "insert_many()" of pymongo.
        When use `ignore_duplicated` function, please make sure the `ordered` is ``False``

        :Parameters:
          - `documents`: A iterable of documents to insert.
          - `ordered` (optional): If ``True`` documents will be
            inserted on the server serially, in the order provided. If an error
            occurs all remaining inserts are aborted. If ``False``, documents
            will be inserted on the server in arbitrary order, possibly in
            parallel, and all document inserts will be attempted. Default is
            ``False``.
          - `ignore_duplicated`: (optional) If ``True``, will ignore the duplicate error. Default is
            ``False``.
          - `kwargs` (optional): some other parameters to pymongo

        :Returns:
          An instance of :class:`~pymongo.results.InsertManyResult`.
        """
        replacer = DictReplacer(replace_enum=True, id_to_objectid=True)
        insert_data = [d.get_data() for d in documents]
        insert_data = replacer.replace_list(insert_data)
        for data in insert_data:
            if "_id" in data:
                del data["_id"]
        coll = cls.class_collection()
        if ignore_duplicated:
            #  ignore duplicate error must use with ordered=False
            ordered = False
        try:
            res = coll.insert_many(insert_data, ordered=ordered, **kwargs)
            return res, len(res.inserted_ids)
        except BulkWriteError as e:
            if not ignore_duplicated:
                raise e
            # copy from https://stackoverflow.com/a/44838740
            panic = filter(lambda x: x['code'] != 11000, e.details['writeErrors'])  # type: ignore
            if len(list(panic)):
                raise e
            duplicated_cnt = len(e.details['writeErrors'])
            return None, len(documents) - duplicated_cnt

    @classmethod
    def delete_many(cls, filter, **kwargs) -> "DeleteResult":
        """
        Wraps the "delete_many()" of pymongo
        """
        replacer = DictReplacer(replace_enum=True, id_to_objectid=True)
        filter = replacer.replace_dict(filter)
        coll = cls.class_collection()
        return coll.delete_many(filter, **kwargs)

    @classmethod
    def update_one(cls, filter, update, **kwargs) -> "UpdateResult":
        """
        Wraps the "update_one()" of pymongo
        """
        replacer = DictReplacer(replace_enum=True, id_to_objectid=True)
        filter = replacer.replace_dict(filter)

        replacer = DictReplacer(replace_enum=True, omit_none=True, id_to_objectid=True)
        update = replacer.replace_dict(update)

        coll = cls.class_collection()
        return coll.update_one(filter, update, **kwargs)

    def update_self(self, update, extra_filter=None, **kwargs) -> bool:
        """
        Wraps the "find_one_and_update()" of pymongo
        Returns whether the update is a success
        """
        if not self._id:
            return False

        replacer = DictReplacer(replace_enum=True, omit_none=True, id_to_objectid=True)
        update = replacer.replace_dict(update)
        coll = self.class_collection()
        filter = {}
        if extra_filter:
            filter = deepcopy(extra_filter)
            filter = replacer.replace_dict(filter)
        filter["_id"] = ObjectId(self._id)

        if "return_document" in kwargs:
            del kwargs["return_document"]

        res = coll.find_one_and_update(filter, update, return_document=ReturnDocument.AFTER, **kwargs)
        if not res:
            return False

        self.set_data(res)
        return True

    @classmethod
    def bulk_write(cls, requests, batch_size: int = 1000, ordered=False, **kwargs) -> List["BulkWriteResult"]:
        """
        Wraps the "bulk_write()" of pymongo
        """
        coll = cls.class_collection()
        result = []
        for chunk in partition(requests, batch_size):
            res = coll.bulk_write(chunk, ordered=ordered, **kwargs)
            result.append(res)
        return result

    @classmethod
    def aggregate(cls, pipeline: List[Dict[str, Any]], **kwargs):
        replacer = DictReplacer(replace_enum=True)
        pipeline = replacer.replace_list(pipeline)
        coll = cls.class_collection()
        return coll.aggregate(pipeline=pipeline, **kwargs)

    def create(self, **kwargs) -> "InsertOneResult":
        """
        Wraps the "insert_one()" of pymongo
        """
        coll = self.class_collection()
        data = self.get_data()

        # This method is to create new document,
        # the `_id` shouldn't exist.
        # We need to delete it if it does
        if "_id" in data and data["_id"] is None:
            del data["_id"]

        replacer = DictReplacer(replace_enum=True, omit_none=True, id_to_objectid=True)
        data = replacer.replace_dict(data)
        res = coll.insert_one(data, **kwargs)
        self._id = res.inserted_id
        return res

    def upsert(self, filter: Dict[str, Any], **kwargs) -> "UpdateResult":
        return self.update_one(filter, {"$set": self.get_data()}, upsert=True)

    # ----------------------------------
    # Some helper methods
    # ----------------------------------

    def get_data(self, for_client: bool = False, include_id: bool = True) -> dict:
        res = super().get_data(for_client)
        if self._id and include_id:
            res["_id"] = str(self._id)
        return res

    @classmethod
    def by_id(cls: Type[SubClassBaseModel], model_id: Union[str, ObjectId]) -> Optional[SubClassBaseModel]:
        """
        Search the collection by "_id".
        Return the initialized Model instance or None
        """

        obj_id = model_id
        if isinstance(model_id, str):
            if not ObjectId.is_valid(model_id):
                return None
            obj_id = ObjectId(model_id)

        res = cls.find_one({
            "_id": obj_id
        })
        return res  # type: ignore

    def reload(self):
        if not self._id:
            return

        res = self.class_collection().find_one({"_id": ObjectId(self._id)})
        if res:
            self.set_data(res)

    def simple_update_session(self, criteria={}):
        """
        It's for updating self conveniently
        ```
        with user.simple_update_session():
            user.name = "a"
            user.email = "b@c.com"
        ```

        It's only used for "$set" and "$unset" updating. If you want to do more advanced
        updating, like "$inc", you still need to call `update_xxx()` methods
        """
        return UpdateContextManager(self, criteria)

    @classmethod
    def batch_reload(cls: Type[SubClassBaseModel], model_list: Tuple[SubClassBaseModel]):
        ids = [ObjectId(item.get_id()) for item in model_list if item.get_id()]
        coll = cls.class_collection()
        result = coll.find(
            {
                "_id": {"$in": ids}
            }
        )
        ret = []
        for item in result:
            obj = cls()
            obj.set_data(item)
            ret.append(obj)
        return ret

    @classmethod
    def batch_load(cls: Type[SubClassBaseModel], ids: List[str]) -> List[SubClassBaseModel]:
        coll = cls.class_collection()
        object_ids = [ObjectId(_id) for _id in ids]
        result = coll.find(
            {
                "_id": {"$in": object_ids}
            }
        )
        ret = []
        for item in result:
            obj = cls()
            obj.set_data(item)
            ret.append(obj)
        return ret


class UpdateContextManager:
    """
    The context manager of BaseModel
    It's used when doing self-updating

    **Note:**
    It's only used for "$set" and "$unset" updating. If you want to do more advanced
    updating, like "$inc", you still need to call `update_xxx()` methods

    ```
    with user.simple_update_session():
        user.name = "a"
        user.email = "b@c.com"
    ```
    """

    def __init__(self, model: SubClassBaseModel, criteria: dict = {}, reload_if_failed=True):
        self.model = model
        self.criteria = criteria
        self.reload_if_failed = reload_if_failed
        self.before = {}
        self.after = {}

    def __enter__(self):
        # need to do deepcopy here in case there is
        # dict or list in the model field
        self.before = deepcopy(self.model.get_data())

    def __exit__(self, *args):
        self.after = self.model.get_data()

        # find the difference and generate the "$set" and "$unset" expressions
        set_data = {}
        unset_data = {}
        self.find_difference(self.before, self.after, set_data, unset_data)

        # update the db
        update = {}
        if set_data:
            update["$set"] = set_data
        if unset_data:
            update["$unset"] = unset_data

        if not update:
            return False

        self.model.update_self(update, extra_filter=self.criteria)

        return False

    def get_value_type(self, value):
        if value is None:
            return "none"

        type = "raw"
        if isinstance(value, dict):
            type = "dict"
        elif isinstance(value, list):
            type = "list"
        return type

    def find_difference(self, before: dict, after: dict, set_data: dict, unset_data: dict, prefix=""):
        for key, after_value in after.items():
            mongo_path = "{}{}".format(prefix, key)

            if key not in before:
                set_data[mongo_path] = after_value
                continue

            before_value = before[key]

            before_type = self.get_value_type(before_value)
            after_type = self.get_value_type(after_value)

            if after_type == "none" and before_type != "none":
                unset_data[mongo_path] = True
                continue

            if after_type != before_type:
                set_data[mongo_path] = after_value
                continue

            if after_value == before_value:
                continue

            if after_type in ["raw", "list"]:
                set_data[mongo_path] = after_value
            else:  # dict
                self.find_difference(
                    before_value, after_value, set_data, unset_data,
                    "{}.".format(mongo_path)
                )

        for key in before:
            if key not in after:
                mongo_path = "{}{}".format(prefix, key)
                unset_data[mongo_path] = True


class DictReplacer:
    def __init__(
        self,
        replace_enum: bool = False,
        omit_none: bool = False,
        snake_to_camel: bool = False,
        id_to_objectid: bool = False
    ) -> None:
        self.replace_enum = replace_enum
        self.omit_none = omit_none
        self.snake_to_camel = snake_to_camel
        self.id_to_objectid = id_to_objectid

    def replace_dict(self, data: Dict[str, Any]):
        if not self.replace_enum and not self.omit_none and not snake_to_camel:
            return data

        new_data = {}
        for key in data:
            val = data[key]
            new_key = key

            if self.omit_none and val is None:
                continue

            if self.snake_to_camel and key != "_id":
                new_key = snake_to_camel(key)

            if self.replace_enum and isinstance(val, Enum):
                val = val.value

            if self.id_to_objectid and key == "_id" and isinstance(val, str):
                val = ObjectId(val)

            if isinstance(val, dict):
                new_data[new_key] = self.replace_dict(val)
            elif isinstance(val, list):
                new_data[new_key] = self.replace_list(val)
            else:
                new_data[new_key] = val

        return new_data

    def replace_list(self, data: List[Any]):
        if not self.replace_enum and not self.omit_none and not snake_to_camel:
            return data

        new_list = []
        for item in data:
            if isinstance(item, dict):
                new_list.append(self.replace_dict(item))
            elif isinstance(item, list):
                new_list.append(self.replace_list(item))
            elif isinstance(item, Enum) and self.replace_enum:
                new_list.append(item.value)
            else:
                new_list.append(item)
        return new_list


def create_bulk_write_operation(request_cls, *args, **kwargs):
    replacer = DictReplacer(replace_enum=True, id_to_objectid=True)
    args = replacer.replace_list(list(args))
    kwargs = replacer.replace_dict(kwargs)
    return request_cls(*args, **kwargs)


def create_update_one(filter, update, upsert=False, **kwargs):
    replacer = DictReplacer(omit_none=True)
    update = replacer.replace_dict(update)
    return create_bulk_write_operation(UpdateOne, filter, update, upsert, **kwargs)


def create_update_many(filter, update, upsert=False, **kwargs):
    replacer = DictReplacer(omit_none=True)
    update = replacer.replace_dict(update)
    return create_bulk_write_operation(UpdateMany, filter, update, upsert, **kwargs)


def create_delete_one(filter, **kwargs):
    return create_bulk_write_operation(DeleteOne, filter, **kwargs)


def create_delete_many(filter, **kwargs):
    return create_bulk_write_operation(DeleteMany, filter, **kwargs)


def create_insert_one(document):
    return create_bulk_write_operation(InsertOne, document)


def create_replace_one(filter, replacement, upsert=False, **kwargs):
    return create_bulk_write_operation(ReplaceOne, filter, replacement, upsert, **kwargs)
