"""
Написать декоратор instances_counter, который применяется к любому классу
и добавляет ему 2 метода:
get_created_instances - возвращает количество созданых экземпляров класса
reset_instances_counter - сбросить счетчик экземпляров,
возвращает значение до сброса
Имя декоратора и методов не менять
Ниже пример использования
"""
import functools


def instances_counter(cls):

    def get_created_instances():
        return cls.count

    def reset_instances_counter():
        res, cls.count = cls.count, 0
        return res

    setattr(cls, 'count', 0)
    setattr(cls, get_created_instances.__name__, staticmethod(get_created_instances))
    setattr(cls, reset_instances_counter.__name__, staticmethod(reset_instances_counter))

    origin_init = cls.__init__

    @functools.wraps(cls.__init__)
    def new_init(self, *args, **kwargs):
        self.__class__.count += 1
        origin_init(self, *args, **kwargs)

    cls.__init__ = new_init

    return cls


@instances_counter
class User:
    pass


if __name__ == '__main__':
    User.get_created_instances()  # 0
    user, _, _ = User(), User(), User()

    print(user.get_created_instances())  # 3
    print(user.reset_instances_counter())  # 3
    print(user.get_created_instances())
