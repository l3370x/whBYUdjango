from django.db import models
from student.models import *

class Request(models.Model):
	fk_student = models.ForeignKey(Student, editable=False)
	fk_team = models.ForeignKey(Team,editable=False)
