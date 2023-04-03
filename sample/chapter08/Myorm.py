import numbers


class Field:
    pass


# IntField数据描述符
class IntField(Field):
    def __init__(self, db_column, min_length=None, max_length=None):
        self._value = None
        self.db_column = db_column
        self.min_length = min_length
        self.max_length = max_length

        if min_length is not None:
            if not isinstance(min_length, numbers.Integral):
                raise ValueError("min_length must need Integral type")
            elif max_length < 0:
                raise ValueError("min_length must be positive int")

        if max_length is not None:
            if not isinstance(max_length, numbers.Integral):
                raise ValueError("max_length must need Integral type")
            elif max_length < 0:
                raise ValueError("max_length must be positive int")

        if min_length is not None and max_length is not None:
            if min_length > max_length:
                raise ValueError("min_length must be smaller than max_length")

    def __set__(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError("value must need Integral type")
        if value < self.min_length or value > self.max_length:
            raise ValueError("value must between min_length and max_length")
        self._value = value

    def __get__(self, instance, owner):
        return self._value


# CharField数据描述符
class CharField(Field):
    def __init__(self, db_column, max_length=None):
        self._value = None
        self.max_length = max_length
        self.db_column = db_column

        if max_length is None:
            raise ValueError("max_length is must need")

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("string value need")
        if len(value) > self.max_length:
            raise ValueError("value len excess len of max_length")
        self._value = value


# 元类
class ModelMetaClass(type):
    def __new__(cls, *args, **kwargs):  # *args 是一个元组，是元类创建类时传的位置参数 (name, base, attr)
        # 获取类中的字段
        fields = {}
        for key, value in args[2].items():
            if isinstance(value, Field):    # Field是字段的父类，所以也可以用于实例判断
                fields[key] = value
        # 获取数据库名称
        db_table = args[0].lower()
        _meta = {}  # 需要注入到新类的meta信息
        # 获取类中的meta信息
        meta_info =args[2].get("Meta", None)
        if meta_info is not None:
            table = getattr(meta_info, "db_table", None)
            if table is not None:
                db_table = table
        _meta["db_table"] = db_table
        args[2]["_meta"] = _meta
        args[2]["fields"] = fields
        del args[2]["Meta"]

        return super().__new__(cls, *args, **kwargs)


class User(metaclass=ModelMetaClass):
    name = CharField(db_column="", max_length=100)
    age = IntField(db_column="", min_length=0, max_length=100)

    class Meta:
        db_table = "user"


if __name__ == "__main__":
    user = User()
    user.name = "yjh"
    user.age = 18
    print(user.name)
    print(user.age)
    # user.save()
