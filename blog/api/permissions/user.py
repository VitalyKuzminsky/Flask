from combojsonapi.permission import PermissionMixin, PermissionForGet, PermissionUser, PermissionForPatch
from flask_combo_jsonapi.exceptions import AccessDenied
from flask_login import current_user

from blog.models import User


class UserListPermission(PermissionMixin):
    ALL_AVAILABLE_FIELDS = (
        'id',
        'email',
        'first_name',
        'last_name',
        'is_staff',
    )

    # Переопределяем существующий метод, что делать при получении данных:
    def get(self, *args, many=True, user_permission: PermissionUser = None, **kwargs) -> PermissionForGet:
        if not current_user.is_authenticated:
            raise AccessDenied('В доступе отказано')

        self.permission_for_get.allow_columns = (self.ALL_AVAILABLE_FIELDS, 10)  # правила для get-запросов. 10 -
        # это вес.

        return self.permission_for_get


class UserPatchPermission(PermissionMixin):
    """Редактирование юзера.
    Пример:
    curl --location --request PATCH 'http://127.0.0.1:5000/api/users/1' \
    --header 'Content-Type: application/json' \
    --data-raw '{
      "data": {
        "type": "user",
        "id": 1,
        "attributes": {
          "first_name": "Иван",
          "last_name": "Иванов"
        }
      }
    }'
    """
    # Указываем поля доступные для редактирования:
    PATCH_AVAILABLE_FIELDS = (
        'first_name',
        'last_name',
    )

    def patch_permission(self, *args, user_permission: PermissionUser = None, **kwargs) -> PermissionForPatch:
        """ Определяет доступные поля для редактирования. """
        self.permission_for_patch.allow_columns = (self.PATCH_AVAILABLE_FIELDS, 10)
        return self.permission_for_patch

    # Функция для редактирования:
    def patch_data(self, *args, data=None, obj=None, user_permission: PermissionUser = None, **kwargs) -> dict:
        permission_for_patch = user_permission.permission_for_patch_permission(model=User)  # Указывыаем модель для
        # редактирования.
        return {
            k: v
            for k, v in data.items()  # Данные, которые пришли от пользователя.
            if k in permission_for_patch.columns  # Проверяет доступно ли это поле для обновления или нет.
        }
