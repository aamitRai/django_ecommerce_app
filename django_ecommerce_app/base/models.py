from django.db import models
import uuid
# Create your models here.
# BaseModel name is  given by me 
class BaseModel(models.Model):
    base_uuid=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    #uuid4 generated random uuid
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)

    #to create these as  a class we need to use 
    class meta:
            abstract=True


