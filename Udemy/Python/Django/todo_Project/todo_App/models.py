from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True) # делает поле необязательным для заполнения
    create_date = models.DateTimeField(auto_now_add=True) # Автоматическая простановка даты создания записи. Не отображется в панели администратора
    date_complited = models.DateTimeField(null=True, blank=True) # Дата завершения записи. blank=True - необязательно для заполнения
    important = models.BooleanField(default=False) # Простановка важности задачи (False-по умолчанию не важно)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Определение связи между записью и пользователем, который ее создал

    def __str__(self):
        return self.title # Для отображения наименования задачи в панели администратора
