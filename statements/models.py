from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название факультета")
    short_name = models.CharField(max_length=50, verbose_name="Короткое название")
    
    class Meta:
        db_table = 'faculties'  # Имя таблицы в БД
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'
        ordering = ['name']  # Сортировка по умолчанию
    
    def __str__(self):
        return self.name

class Direction(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='directions')
    name = models.CharField(max_length=200, verbose_name="Название направления")
    code = models.CharField(max_length=50, verbose_name="Код направления")
    
    class Meta:
        db_table = 'directions'  # Имя таблицы в БД
        verbose_name = 'Направление подготовки'
        verbose_name_plural = 'Направления подготовки'
        ordering = ['faculty', 'code']  # Сортировка по факультету и коду
        indexes = [
            models.Index(fields=['code'], name='direction_code_idx'),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Exam(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название экзамена")
    min_score = models.IntegerField(verbose_name="Минимальный балл")
    max_score = models.IntegerField(verbose_name="Максимальный балл")
    
    class Meta:
        db_table = 'exams'  # Имя таблицы в БД
        verbose_name = 'Экзамен'
        verbose_name_plural = 'Экзамены'
        ordering = ['name']  # Сортировка по названию
    
    def __str__(self):
        return self.name

class DirectionExam(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    required = models.BooleanField(default=True, verbose_name="Обязательный экзамен")
    
    class Meta:
        db_table = 'direction_exams'  # Имя таблицы в БД
        verbose_name = 'Экзамен направления'
        verbose_name_plural = 'Экзамены направлений'
        ordering = ['direction', 'exam']
        unique_together = ('direction', 'exam')  # Уникальная связка
        indexes = [
            models.Index(fields=['direction'], name='direction_exam_direction_idx'),
            models.Index(fields=['exam'], name='direction_exam_exam_idx'),
        ]
    
    def __str__(self):
        return f"{self.direction} - {self.exam} (Обязательный: {'Да' if self.required else 'Нет'})"

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Черновик'),
        ('submitted', 'Подано'),
        ('approved', 'Принято'),
        ('rejected', 'Отклонено')
    ], default='draft')
    
    class Meta:
        db_table = 'applications'  # Имя таблицы в БД
        verbose_name = 'Заявление'
        verbose_name_plural = 'Заявления'
        ordering = ['-created_at']  # Сортировка по дате создания (новые сначала)
        indexes = [
            models.Index(fields=['user'], name='application_user_idx'),
            models.Index(fields=['direction'], name='application_direction_idx'),
            models.Index(fields=['status'], name='application_status_idx'),
        ]
        unique_together = ('user', 'direction')  # Одно заявление на направление
    
    def __str__(self):
        return f"Заявление {self.user} на {self.direction}"