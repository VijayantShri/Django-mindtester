from django.db import models

class NewStudent(models.Model):
	sname = models.CharField(max_length=100)
	semail = models.CharField(max_length=100)
	spass = models.CharField(max_length=100)
	class Meta:
		db_table = "student_registeration"

class NewTeacher(models.Model):
	tname = models.CharField(max_length=100)
	temail = models.CharField(max_length=100)
	tpass = models.CharField(max_length=100)
	class Meta:
		db_table = "teacher_registeration"

class Questions(models.Model):
	question = models.CharField(max_length=300)
	title = models.CharField(max_length=100)
	option1 = models.CharField(max_length=100)
	option2 = models.CharField(max_length=100)
	option3 = models.CharField(max_length=100)
	option4 = models.CharField(max_length=100)
	correct_ans = models.CharField(max_length=100)

	description = models.CharField(max_length=100)

	class Meta:
		db_table = "quizOnline"

class Record(models.Model):
	student_id = models.IntegerField(max_length=11)
	quiz_title = models.CharField(max_length=10)
	result = models.IntegerField(max_length=10)
	class Meta:
		db_table = "record"