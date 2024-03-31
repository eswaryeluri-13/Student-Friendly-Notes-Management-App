from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import StForm
from NotesApp.models import *
from NotesManagement import settings
from django.core.mail import send_mail
import os

def landing(request):
	return render(request,'landingpage.html')

def login(request):
	if request.method=="POST":
		try:
			g=Student.objects.get(email=request.POST['email'])
			if request.POST['Pass']==g.password:
				print("Successssss")
				return redirect('/mainpage/'+str(g.id))
		except:
			print("Faileddd")

	return render(request,'login.html')

def register(request):
	if request.method=="POST":
		g=StForm(request.POST)
		if g.is_valid():
			g.save()
			return redirect('/')
		else:
			print(g.errors)
	g=StForm()
	return render(request,'register.html',{'form':g})

def mainpage(request,id):
	return render(request,'mainpage.html',{'ID':id})

def home(request,n_id):
	z=Student.objects.get(id=n_id)
	return render(request,'home.html',{'note':z,'ID':n_id})

def createnote(request, id):
    if request.method == 'POST':
        st_id = id
        s_sbj = request.POST['sb']
        s_note = request.POST['note']
        w = Notes.objects.create(sid=st_id, sub=s_sbj, note=s_note, like=0, dislike=0)
        # return redirect('/mainpage/'+str(st_id))   
        n = Notes.objects.last()
        if 'file_upload' in request.FILES:
            file = request.FILES['file_upload']
            file_folder = r"D:\Django\NotesManagement\NotesApp\static\all_files"
            file_type = f'{n.id}.{file.name.split(".")[-1]}'
            file_path2 = os.path.join(file_folder, file_type)
            with open(file_path2, 'wb+') as des:
                for c in file.chunks():
                    des.write(c)
        return render(request, 'createnote.html', {'ID': id})

    return render(request, 'createnote.html', {'ID': id})


def displaynote(request,id):
	c=Student.objects.all()
	d=Notes.objects.all()
	e=Student.objects.get(id=id)
	return render(request,'displaynote.html',{'ID':id,'notes':d,'ids':e,'users':c})

def viewnote(request, id, nid):
    if request.method == 'POST':
        selected_students = request.POST.getlist('selected_students[]')
        for i in selected_students:
            q = Notes.objects.get(id=nid)
            w = Accepted.objects.create(rid=i, nid=nid, s_sub=q.sub, s_note=q.note)

        print(selected_students)
    e = Student.objects.exclude(id=id)
    d = Notes.objects.get(id=nid)
    f = Accepted.objects.filter(nid=nid)
    l = [i.rid for i in f]
    l1 = [i for i in e if i.id not in l]

    pdf = None  # Initialize pdf as None
    files = os.listdir(r"D:\Django\NotesManagement\NotesApp\static\all_files")
    for i in files:
        if str(nid) == i.split('.')[0]:
            type1 = i.split('.')[1]
            file_name = d.sub + '.' + type1
            pdf = i
    print(pdf)
    return render(request, 'viewnote.html', {'ID': id, 'notes': d, 'all': l1, 'users': l, 'PDF': pdf})

def access(request,id):
	a=Notes.objects.filter(sid=id)
	l = [i.id for i in a if i.sid == id]
	l1=[]
	nlist,rlist,slist,plist=[],[],[],[]
	b=Accepted.objects.all()
	for i in b:
		if i.nid in l:
			nlist.append(i.nid)
			rlist.append(i.rid)
	for i in nlist:
		c=Notes.objects.get(id=i)
		slist.append(c)
	for i in rlist:
		c=Student.objects.get(id=i)
		plist.append(c)
	zipped_lists = zip(slist, plist)
	print
	return render(request,'accessing.html',{'ID':id,'lists':zipped_lists})

def updatenote(request, id, nid):
    z = Notes.objects.get(id=nid)
    file_name = None  # Initialize file_name as None

    files = os.listdir(r"D:\Django\NotesManagement\NotesApp\static\all_files")

    pdf = None  # Initialize pdf as None
    for i in files:
        if str(nid) == i.split('.')[0]:
            type1 = i.split('.')[1]
            file_name = z.sub + '.' + type1
            pdf = i
    print(pdf)  # Moved outside the loop to print the final value of pdf

    if request.method == 'POST':
        z.sub = request.POST['s_sub']
        z.note = request.POST['s_note']
        
        if 'file_upload' in request.FILES:
            file = request.FILES['file_upload']
            
            file_folder = r"D:\Django\NotesManagement\NotesApp\static\all_files"

            file_type = f'{nid}.{file.name.split(".")[-1]}'
            file_path2= os.path.join(file_folder,file_type)

            with open(file_path2,'wb+') as des:
                 for c in file.chunks():
                      des.write(c)
        z.save()
        return redirect('/display/' + str(id))
    
    return render(request, 'updatenote.html', {'ID': id, 'notes': z, 'file_name': file_name,'PDF':pdf})

def deletenote(request, id, nid):
    z = Notes.objects.get(id=nid)
    y = Accepted.objects.filter(nid=nid)
    if request.method == "POST":
        z.delete()
        for i in y:
            i.delete()
        try:
            file_folder = r"D:\Django\NotesManagement\NotesApp\static\all_files"
            pdf = None  # Initialize pdf as None
            files = os.listdir(file_folder)
            for i in files:
                if str(nid) == i.split('.')[0]:
                    type1 = i.split('.')[1]
                    file_name = z.sub + '.' + type1
                    pdf = i
            print(pdf)
            os.remove(os.path.join(file_folder, pdf))
        except Exception as e:
            print("An error occurred during file deletion:", e)
        return redirect('/display/' + str(id))
    return render(request, 'deletenote.html', {'ID': id, 'notes': z})


def othernote(request,id):
	d=Notes.objects.all()
	e=Requests.objects.filter(rid=id)
	e1=Accepted.objects.filter(rid=id)
	values_list = [ obj.ntid for obj in e]
	values_list1 = [ obj.nid for obj in e1]
	#print(values_list)
	return render(request,'othernote.html',{'ID':id,'notes':d,'req':values_list,'req1':values_list1})

def requestnote(request,id,sid,nid,s_sub,s_note):
	g=Student.objects.get(id=id)
	g1=Student.objects.get(id=sid)
	w=Requests.objects.create(sname=g.name,rid=id,sub=s_sub,atid=sid,ntid=nid)
	sbj="Request from Notes Management App"
	file_content = open(r"D:\Django\request_mail_sending.txt").read()
	file_content = file_content.replace("[Student's Name]",g.name)
	file_content = file_content.replace("[Subject Name]",s_sub)
	m=file_content
	t=settings.EMAIL_HOST_USER

	b=send_mail(sbj,m,t,[g1.email])
	return redirect('/mainpage/'+str(id))

def reqpage(request,id):
	e=Requests.objects.filter(atid=id)
	return render(request,'requestnote.html',{'ID':id,'requests':e})

def reqdpage(request,id):
	e=Requests.objects.filter(rid=id)
	g=Student.objects.all()
	return render(request,'requestednote.html',{'ID':id,'requests':e,'all':g})

def accepted(request,id,rid,atid,nid):
	q=Notes.objects.get(id=nid)
	g1=Student.objects.get(id=atid)
	g2=Student.objects.get(id=rid)
	r = Requests.objects.filter(rid=rid, ntid=nid).first()
	r.delete()
	w=Accepted.objects.create(rid=rid,nid=nid,s_sub=q.sub,s_note=q.note)
	sbj="Accepted Request from Notes Management App"
	file_content = open(r"D:\Django\accepted_mail_sending.txt").read()
	file_content = file_content.replace("[Req Student's Name]",g2.name)
	file_content = file_content.replace("[Student's Name]",g1.name)
	file_content = file_content.replace("[Subject Name]",q.sub)
	m=file_content
	t=settings.EMAIL_HOST_USER

	b=send_mail(sbj,m,t,[g2.email])
	e=Requests.objects.filter(atid=id)
	return render(request,'requestnote.html',{'ID':id,'requests':e})

def declined(request,id,rid,atid,nid):
	q=Notes.objects.get(id=nid)
	g1=Student.objects.get(id=atid)
	g2=Student.objects.get(id=rid)
	r = Requests.objects.filter(rid=rid, ntid=nid).first()
	r.delete()
	sbj="Declined Request from Notes Management App"
	file_content = open(r"D:\Django\declined_mail_sending.txt").read()
	file_content = file_content.replace("[Req Student's Name]",g2.name)
	file_content = file_content.replace("[Student's Name]",g1.name)
	file_content = file_content.replace("[Subject Name]",q.sub)
	m=file_content
	t=settings.EMAIL_HOST_USER

	b=send_mail(sbj,m,t,[g2.email])
	# return redirect('/mainpage/'+str(id))
	e=Requests.objects.filter(atid=id)
	return render(request,'requestnote.html',{'ID':id,'requests':e})

def acceptednotes(request,id):
	e=Accepted.objects.filter(rid=id)
	l=[i.nid for i in e]
	print(l)
	f=Notes.objects.all()
	l1=[i for i in f if i.id in l	]
	print(l1)
	return render(request,'acceptednote.html',{'ID':id,'requests':l1})

def viewreqnote(request, id, nid):
    d = Notes.objects.get(id=nid)
    pdf = None  # Initialize pdf as None
    files = os.listdir(r"D:\Django\NotesManagement\NotesApp\static\all_files")
    for i in files:
        if str(nid) == i.split('.')[0]:
            type1 = i.split('.')[1]
            file_name = d.sub + '.' + type1
            pdf = i
    print(pdf)
    return render(request, 'viewreqnote.html', {'ID': id, 'notes': d, 'PDF': pdf})

def likebutton(request,id,nid):
	d=Notes.objects.get(id=nid)
	d.like+=1
	d.save()
	e=Accepted.objects.filter(rid=id)
	return render(request,'acceptednote.html',{'ID':id,'requests':e})

def dislikebutton(request,id,nid):
	d=Notes.objects.get(id=nid)
	d.dislike+=1
	d.save()
	e=Accepted.objects.filter(rid=id)
	return render(request,'acceptednote.html',{'ID':id,'requests':e})

def newaccept(request,id):
	d=Student.objects.all()

def serve_pdf(request, path):
    pdf_file = os.path.join(settings.MEDIA_ROOT, pdf_path)
    response = FileResponse(open(pdf_file, 'rb'), content_type='application/pdf')
    return response

def revoke(request,id,nid,sid):
	c=Accepted.objects.filter(nid=nid,rid=sid).first().delete()
	return redirect('/access/'+str(id))

def create_remainder(request,id):
    if request.method == 'POST':
        time = request.POST.get('time')
        note = request.POST.get('note')
        Remainder.objects.create(time=time, note=note)
        # You might add further logic here, like redirecting to a confirmation page.
    remainders = Remainder.objects.all()
    return render(request, 'remainder.html', {'ID':id,'remainders': remainders})

def delete_remainder(request,id):
    remainder = Remainder.objects.get(id=id)
    remainder.delete()
    # You might add further logic here, like redirecting to a confirmation page.
    return redirect(f'http://127.0.0.1:8000/remainder/{id}')  # Assuming your URL name for create_remainder is 'create_remainder'