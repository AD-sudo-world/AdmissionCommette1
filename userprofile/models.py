from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    class DocType(models.TextChoices):
        PASSPORT = 'passport', _('Паспорт')
        BIRTH_CERTIFICATE = 'birth_cert', _('Свидетельство о рождении')

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('Пользователь')
    )
    middle_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Отчество')
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Дата рождения')
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Телефон'),
        help_text=_('Формат: +7XXXXXXXXXX')
    )
    doc_type = models.CharField(
        max_length=20,
        choices=DocType.choices,
        default=DocType.PASSPORT,
        verbose_name=_('Тип документа')
    )
    doc_series = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_('Серия документа')
    )
    doc_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Номер документа')
    )
    dormitory_needed = models.BooleanField(
        default=False,
        verbose_name=_('Требуется общежитие')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )

    class Meta:
        db_table = 'user_profiles'  # Имя таблицы в БД
        verbose_name = _('Профиль пользователя')
        verbose_name_plural = _('Профили пользователей')
        ordering = ['user__last_name', 'user__first_name']  # Сортировка по ФИО
        indexes = [
            models.Index(fields=['phone'], name='profile_phone_idx'),
            models.Index(fields=['doc_series', 'doc_number'], name='profile_doc_idx'),
            models.Index(fields=['dormitory_needed'], name='profile_dormitory_idx'),
        ]
    def get_doc_type_display(self) -> str: ...
    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} {self.middle_name or ''}".strip()

    def get_full_name(self):
        """Возвращает полное ФИО пользователя"""
        parts = [self.user.last_name, self.user.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return ' '.join(parts)

    @property
    def document_info(self):
        """Возвращает информацию о документе"""
        if not self.doc_series and not self.doc_number:
            return ''
        doc_type = self.get_doc_type_display()
        return f"{doc_type} {self.doc_series} {self.doc_number}"