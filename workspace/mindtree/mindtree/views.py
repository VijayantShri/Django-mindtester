from django.shortcuts import render
#from mindtree.models import Exam
from mindtree.models import NewStudent
from mindtree.models import NewTeacher
from mindtree.models import Questions
from mindtree.models import Record
from django.contrib import messages
from django.core.paginator import Paginator

lst = []
anslist = []
answer = Questions.objects.all()

for i in answer:
	anslist.append(i.correct_ans)


def index(request):
	return render(request, 'main.html')

def newStudent(request):
	if request.method == "POST":
		if request.POST.get("sname") and request.POST.get("semail") and request.POST.get("spass"):
			query = NewStudent()
			query.sname = request.POST['sname']
			query.semail = request.POST['semail']
			query.spass = request.POST['spass']
			query.save()
			messages.success(request, "Register Successfully...")
			return render(request, 'registerMsg.html', {"Name":request.POST.get("sname"), "Email": request.POST.get("semail")})
	else:
		return render(request, 'studentReg.html')

def newTeacher(request):
	if request.method == "POST":
		if request.POST.get("tname") and request.POST.get("temail") and request.POST.get("tpass"):
			tname = request.POST.get('tname')
			temail = request.POST.get('temail')
			tpass = request.POST.get('tpass')
			query = NewTeacher(tname=tname, temail=temail, tpass=tpass)
			query.save()
			messages.success(request, "Register Successfully...")
			return render(request, 'registerMsg.html', {"Name":request.POST.get("tname"), "Email": request.POST.get("temail")})
	else:
		return render(request, 'teacherReg.html')

def distinctQuiz():
	quizes = Questions.objects.raw("Select * from quizOnline")
	quizSet = set()
	for i in quizes:
		quizSet.add(i.title)
	return list(quizSet)

title = ''
page = 0
name = ''

def studentIn(request):
	global title
	global page
	page = 0
	title = None
	lst.clear()
	if request.method=="POST":
		try:
			studentDetail = NewStudent.objects.get(semail=request.POST['semail'], spass=request.POST['spass'])
			request.session['id']=studentDetail.id
			name = studentDetail.sname
			result = Record.objects.get(student_id=studentDetail.id)
			return render(request, 'studentDashboard.html', {"Name":name, "quizes": distinctQuiz()})
		except NewStudent.DoesNotExist as e:
			messages.success(request, "Username / Password is invalid.")
	del request.session['title']
	return render(request, 'studentLogin.html')

def teacherIn(request):
	x=""
	if request.method=="POST":
		try:
			teacherDetail = NewTeacher.objects.get(temail=request.POST['temail'], tpass=request.POST['tpass'])
			request.session['id']=teacherDetail.id
			name = teacherDetail.tname
			return render(request, 'teacherDashboard.html', {"Name":name})
		except NewStudent.DoesNotExist as e:
			messages.success(request, "Username / Password is invalid.")
	return render(request, 'teacherLogin.html', {"msg":x})


def studentOut(request):
	try:
		del request.session['id']
	except:
		return render(request, 'main.html')
	return render(request, 'main.html')

def teacherOut(request):
	try:
		del request.session['id']
	except:
		return render(request, 'main.html')
	return render(request, 'main.html')

def quizTime(request):
	global title
	global page

	if page==0:
		if request.POST['Start']:
			title = request.POST['title']
			request.session['title'] = title

	questions = Questions.objects.raw("Select * from quizOnline where title= %s", [request.session['title']])
	paginator = Paginator(questions, 1)
	try:
		page=int(request.GET.get('page', '1'))
	except:
		page=1
	try:
		ques = paginator.page(page)
	except(EmptyPage, InvalidPage):
		ques = paginator.page(paginator.num_page)
	return render(request, 'Question.html', {'questions': questions, 'ques':ques, 'title':title, "page": page})

def quizEnd(request):
	global page
	page = 0
	student = NewStudent.objects.get(id=request.session['id'])
	return render(request, 'studentDashboard.html', {"Name":student.sname, "quizes": distinctQuiz()})

def result(request):
	score = 0
	for i in range(len(lst)):
		if lst[i] == anslist[i]:
			score+=1
	inc = 10 - score
	record = Record(student_id=request.session['id'], quiz_title=request.session["title"], result=score)
	record.save()
	del request.session['title']
	return render(request, "result.html", {'score':score, 'inc':inc})


def saveAns(request):
	ans = request.GET['ans']
	lst.append(ans)