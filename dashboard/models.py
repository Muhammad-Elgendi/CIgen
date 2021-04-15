from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models

class User(AbstractUser):
    @property
    def is_student(self):
        return not (self.is_staff or self.is_superuser)

    def sum_points(self,from_time,to_time):   
        pass

    def sum_marks(self,from_time,to_time):   
        pass

    def sum_final_marks(self,from_time,to_time):   
        pass

    def percentage(self,from_time,to_time):
        return self.sum_marks(from_time,to_time) / self.sum_final_marks(from_time,to_time) * 100

    def sum_hours(self,from_time,to_time):   
        pass

    def gpa(self,from_time,to_time):
        return self.sum_points(from_time,to_time) / self.sum_hours(from_time,to_time)


# Create your models here.
class Course(models.Model):
    student = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length= 100)
    code = models.CharField(max_length= 10, null=True, blank=True)
    hours = models.IntegerField()
    mark = models.IntegerField(blank=True, null= True)
    final_mark = models.IntegerField()
    status = models.CharField(max_length=15)
    date_of_action = models.DateTimeField(auto_now_add=True)



    @property
    def points(self):
        #self.published_date = timezone.now()
        #self.save()
        pass

    @property
    def grade(self):
        #self.published_date = timezone.now()
        #self.save()
        # if self.mark >85:
        #     return 'A+'
        pass

    @property
    def percentage(self):
        return self.mark / self.final_mark * 100

@receiver(post_save, sender=User)
def create_user_course(sender, instance, created, **kwargs):
    # if created:
    #     Course.objects.create(user=instance)
    pass
    
@receiver(post_save, sender=User)
def save_user_course(sender, instance, **kwargs):
    # instance.course.save()
    pass