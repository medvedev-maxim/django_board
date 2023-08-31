from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    
    title = models.CharField(max_length=128)
    content = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)

    TANK = 'TK'
    HEAL = 'HL'  
    DD = 'DD'
    MERCHANT = 'MC' 
    GUILDMASTER = 'GM'
    QUESTGIVER = 'QG'
    BLACKSMITH = 'BS'
    LEATHERWORKER = 'LW'
    POTIONSMASTER = 'PM'
    SPELLMASTER = 'SM'
    CATEGORY_CHOICES = (
        (TANK, 'Танки'),
        (HEAL, 'Хилы'),
        (DD, 'ДД'),
        (MERCHANT, 'Торговцы'),
        (GUILDMASTER, 'Гилдмастеры'),
        (QUESTGIVER, 'Квестгиверы'),
        (BLACKSMITH, 'Кузнецы'),
        (LEATHERWORKER, 'Кожевники'),
        (POTIONSMASTER, 'Зельевары'),
        (SPELLMASTER, 'Мастера заклинаний'),
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f'Объявление #{self.pk} - {self.title}'
    
    def get_absolute_url(self):
        return f'posts/{self.id}'


class Reply(models.Model):
    feedbackUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_replys')
    feedbackPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_replys' )
    
    title = models.CharField(max_length=128)
    acceptStatus = models.BooleanField(default=False)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)

    def accept (self):
        if not self.acceptStatus:
            self.acceptStatus = True
    
    def __str__(self):
        return f'Комментарий #{self.pk} от {self.feedbackUser.last_name}'

