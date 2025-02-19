from django.db import models

# Create your models here.
class Space(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=255, unique=True, editable=True)
    view_Code = models.CharField(max_length=255, unique=True, editable=True)


    def __str__(self):
        return self.code
    

class Field(models.Model):
    space_code = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="field")
    field_code = models.CharField(max_length=255, unique=True, editable=True)
    title = models.CharField(max_length=255)
    last_modified = models.DateField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.title
    
    
