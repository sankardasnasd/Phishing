import base64
from datetime import datetime


from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.


import numpy as np
import pandas as pd
# import feature_extraction
from sklearn import feature_extraction
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from myapp.models import *


def login(request):
    return render(request,'loginindex.html')



def login_post(request):
    a=request.POST['username']
    b=request.POST['password']
    result=Login.objects.filter(username=a,password=b)
    if result.exists():
        result2=Login.objects.get(username=a,password=b)
        request.session['lid']=result2.id
        if result2.type=='admin':
            return HttpResponse('''<script>alert('Admin login success fully');window.location='/myapp/home/'</script>''')


        elif result2.type=='manufacture':
            return HttpResponse('''<script>alert('Manufacture login success fully');window.location='/myapp/manufacture_home/'</script>''')


        else:
            return HttpResponse(
                '''<script>alert('invalid');window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse(
            '''<script>alert('invalid');window.location='/myapp/login/'</script>''')

def logout(request):
    request.session['lid']=''
    return HttpResponse('''<script>alert('Logout');window.location='/myapp/login/'</script>''')


def home(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')
    return render(request,'admin/adminindex.html')


def admin_change_password(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    return render(request,'admin/Admin_change_password.html')


def admin_change_password_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    old = request.POST['old_password']
    new = request.POST['new_password']
    confirm = request.POST['con_password']
    result=Login.objects.filter(id=request.session['lid'],password=old)
    if result.exists():
        if new==confirm:
            Login.objects.filter(id=request.session['lid']).update(password=confirm)
            return HttpResponse('''<script>alert('Successfully changed');window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid');window.location='/myapp/admin_home/'</script>''')
    else:
        return HttpResponse('''<script>alert('Invalid');window.location='/myapp/admin_home/'</script>''')




def view_user(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=User.objects.all()
    return render(request,'admin/view__user.html',{'data':var})

def view_user_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    search = request.POST['search']
    var = User.objects.filter(name__icontains=search)
    return render(request,'admin/view__user.html',{'data':var})

def view_complaint(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Complaint.objects.all()
    return render(request, 'admin/View_complaint.html',{'var':var})



def view_complaint_post(request, ):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    fromD=request.POST['f']
    to=request.POST['t']
    var=Complaint.objects.filter(date__range=[fromD,to])

    return render(request, 'admin/View_complaint.html', {'var': var})


def view_feedback(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Feedback.objects.all()
    return render(request, 'admin/View_feedback.html',{'var':var})

def view_feedback_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    fromD = request.POST['f']
    to = request.POST['t']
    var = Feedback.objects.filter(date__range=[fromD, to])

    return render(request, 'admin/View_feedback.html',{'var':var})




def view_manufacture(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Manufacture.objects.filter(status='pending')
    return render(request,'admin/admin_view_manufacture.html',{'data':var})



def view_manufacture_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    search = request.POST['searching']
    var = Manufacture.objects.filter(name__icontains=search)
    return render(request,'admin/admin_view_manufacture.html',{'data':var})



def aproving_manufacture(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    Manufacture.objects.filter(LOGIN_id=id).update(status='approved')
    Login.objects.filter(id=id).update(type='manufacture')


    return HttpResponse('''<script>alert('Manufature Approved');window.location='/myapp/view_aproved_manufacture/'</script>''')


def reject_Manufacture(request,id):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    Manufacture.objects.filter(LOGIN_id=id).update(status='rejected')
    Login.objects.filter(id=id).update(type='pending')

    return HttpResponse('''<script>alert('Manufacture Reject');window.location='/myapp/view_reject_manufacture/'</script>''')



def view_aproved_manufacture(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Manufacture.objects.filter(status='approved')
    return render(request,'admin/admin_view_aproved_manufacture.html',{'data':var})


def view_aproved_manufacture_post(request):
    search=request.POST['searching']
    var=Manufacture.objects.filter(name__icontains=search,status='approved')
    return render(request,'admin/admin_view_aproved_manufacture.html',{'data':var})




def view_reject_manufacture(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    var=Manufacture.objects.filter(status='rejected')
    return render(request,'admin/admin_view_reject_manufacture.html',{'data':var})

def view_reject_manufacture_post(request):
    search=request.POST['searching']
    var=Manufacture.objects.filter(name__icontains=search,status='rejected')
    return render(request,'admin/admin_view_reject_manufacture.html',{'data':var})


def send_reply(request,id):
    var=Complaint.objects.get(id=id)
    return render(request,'admin/send_reply.html',{'data':var})



def send_reply_post(request):
    reply=request.POST['reply']
    id=request.POST['id']
    date=datetime.now().date().today()

    var=Complaint.objects.get(id=id)
    var.date=date
    var.status='Replied'
    var.reply=reply
    var.save()

    return HttpResponse('''<script>alert(' Reply SuccessFully Sent');window.location='/myapp/view_complaint/'</script>''')

# manufacture

def manufacture(request):
    return render(request,'manufacture/manufature.html')





def manufacture_post(request):


    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    pin=request.POST['pin']
    post=request.POST['post']
    password=request.POST['password']
    confirm=request.POST['confirm']

    if password==confirm:
        log = Login()
        log.username = email
        log.password = confirm
        log.type = 'pending'
        log.save()

        image = request.FILES['image']
        date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'

        fs = FileSystemStorage()
        fs.save(date, image)
        path = fs.url(date)

        var = Manufacture()
        var.LOGIN = log
        var.name = name
        var.email = email
        var.phone = phone
        var.pin = pin
        var.post = post
        var.place = place
        var.image = path
        var.status='pending'
        var.save()
        return HttpResponse('''<script>alert(' Register Successfull');window.location='/myapp/login'</script>''')


    else:

        return HttpResponse('''<script>alert(' innvalid ');window.location='/myapp/login'</script>''')

def manufacture_home(request):
    return render(request, 'manufacture/manufavture_home.html')

def manufacture_profile(request):
    var=Manufacture.objects.get(LOGIN_id=request.session['lid'])

    return render(request, 'manufacture/manufactureptofile.html',{'data':var})

def edit_manu(request,id):

    var=Manufacture.objects.get(id=id)
    return render(request,'manufacture/edit_manufacture.html',{'data':var})

def edit_manu_post(request):
    id=request.POST['id']
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    pin=request.POST['pin']
    post=request.POST['post']






    var=Manufacture.objects.get(id=id)
    var.name=name
    var.email=email
    var.phone=phone
    var.pin=pin
    var.post=post
    var.place=place

    if 'image' in request.FILES:
        image = request.FILES['image']
        date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'

        fs = FileSystemStorage()
        fs.save(date, image)
        path = fs.url(date)
        var.image=path
    var.save()


    return HttpResponse('''<script>alert('  Successfull');window.location='/myapp/manufacture_profile/'</script>''')


def manu_change_password(request):
    # if request.session['lid']=="":
    #     return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    return render(request,'manufacture/manu_change_password.html')

def manu_change_password_post(request):
    # if request.session['lid'] == "":
    #     return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    old = request.POST['old_password']
    new = request.POST['new_password']
    confirm = request.POST['con_password']
    result=Login.objects.filter(id=request.session['lid'],password=old)
    if result.exists():
        if new==confirm:
            Login.objects.filter(id=request.session['lid']).update(password=confirm)
            return HttpResponse('''<script>alert('Successfully changed');window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid');window.location='/myapp/manufacture_home/'</script>''')
    else:
        return HttpResponse('''<script>alert('Invalid');window.location='/myapp/manufacture_home/'</script>''')





def category(request):
    return render(request,'manufacture/add_category.html')
def category_post(request):
    category=request.POST['category']
    var=Category()
    var.MANUFACTURE=Manufacture.objects.get(LOGIN_id=request.session['lid'])
    var.category_name=category
    var.save()
    return HttpResponse('''<script>alert('Success');window.location='/myapp/category/'</script>''')

def view_category(request):
    var=Category.objects.filter(MANUFACTURE__LOGIN_id=request.session['lid'])
    return render(request,'manufacture/view_category.html',{'data':var})


def view_category_post(request):
    search=request.POST['category']
    var=Category.objects.filter(category_name__icontains=search,MANUFACTURE__LOGIN_id=request.session['lid'])
    return render(request,'manufacture/view_category.html',{'data':var})

def edit_category(request,id):
    var=Category.objects.get(id=id)
    return render(request,'manufacture/edit_category.html',{'data':var})



def edit_category_post(request):
    id=request.POST['id']
    category=request.POST['category']
    var=Category.objects.get(id=id)
    var.MANUFACTURE=Manufacture.objects.get(LOGIN_id=request.session['lid'])
    var.category_name=category
    var.save()
    return HttpResponse('''<script>alert('Success');window.location='/myapp/view_category/'</script>''')

def delete_category(request,id):
    var=Category.objects.get(id=id)
    var.delete()

    return HttpResponse('''<script>alert('Success');window.location='/myapp/view_category/'</script>''')



def add_product(request):
    var=Category.objects.all()
    return render(request,'manufacture/add_product.html',{'data':var})


def add_product_post(request):
    category=request.POST['select']
    product=request.POST['product']
    price=request.POST['price']
    desc=request.POST['desc']

    var=Product()
    var.MANUFACTURE=Manufacture.objects.get(LOGIN_id=request.session['lid'])
    var.CATEGORY=Category.objects.get(id=category)
    var.price=price
    var.name=product
    var.description=desc

    var.save()
    return HttpResponse('''<script>alert('Success');window.location='/myapp/view_product/'</script>''')




def view_product(request):
    var=Product.objects.filter(MANUFACTURE__LOGIN_id=request.session['lid'])
    return render(request,'manufacture/view_product.html',{'data':var})


def view_product_post(request):
    search=request.POST['category']
    var=Product.objects.filter(name__icontains=search,MANUFACTURE__LOGIN_id=request.session['lid'])
    return render(request,'manufacture/view_product.html',{'data':var})

def delete_product(request,id):
    var=Product.objects.get(id=id)
    var.delete()
    return HttpResponse('''<script>alert('Success');window.location='/myapp/view_product/'</script>''')


def edit_product(request,id):
    var=Category.objects.all()

    var2=Product.objects.get(id=id)
    return render(request,'manufacture/edit_product.html',{'data':var,'data2':var2})



def edit_product_post(request):
    id=request.POST['id']
    category=request.POST['select']
    product=request.POST['product']
    price=request.POST['price']
    desc=request.POST['desc']

    var=Product.objects.get(id=id)
    var.MANUFACTURE=Manufacture.objects.get(LOGIN_id=request.session['lid'])
    var.CATEGORY=Category.objects.get(id=category)
    var.price=price
    var.name=product
    var.description=desc

    var.save()
    return HttpResponse('''<script>alert('Success');window.location='/myapp/view_product/'</script>''')







# user

def user(request):
    return render(request,'user.html')





def user_post(request):


    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    pin=request.POST['pin']
    post=request.POST['post']
    password=request.POST['password']
    confirm=request.POST['confirm']

    log=Login()
    log.username=email
    log.password=confirm
    log.type='user'
    log.save()


    image=request.FILES['image']
    date=datetime.now().strftime('%Y%m%d-%H%M%S')+'.jpg'

    fs=FileSystemStorage()
    fs.save(date,image)
    path=fs.url(date)


    var=User()
    var.LOGIN=log
    var.name=name
    var.email=email
    var.phone=phone
    var.pin=pin
    var.post=post
    var.place=place
    var.image=path
    var.save()


    return HttpResponse('''<script>alert(' Register Successfull');window.location='/myapp/login'</script>''')


def user_home(request):
    return render(request,'user/user_home.html')


def user_change_password(request):
    # if request.session['lid']=="":
    #     return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    return render(request,'user/user_change_password.html')



def user_change_password_post(request):
    # if request.session['lid'] == "":
    #     return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    old = request.POST['old_password']
    new = request.POST['new_password']
    confirm = request.POST['con_password']
    result=Login.objects.filter(id=request.session['lid'],password=old)
    if result.exists():
        if new==confirm:
            Login.objects.filter(id=request.session['lid']).update(password=confirm)
            return HttpResponse('''<script>alert('Successfully changed');window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid');window.location='/myapp/user_home/'</script>''')
    else:
        return HttpResponse('''<script>alert('Invalid');window.location='/myapp/user_home/'</script>''')

def user_profile(request):
    var=User.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'user/userptofile.html',{'data':var})


def edit_profile(request,id):
    var=User.objects.get(id=id)
    return render(request,'user/edit_profile.html',{'data':var})

def edit_profile_post(request):
    id=request.POST['id']
    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    gender=request.POST['gender']
    age=request.POST['age']
    place=request.POST['place']
    pin=request.POST['pin']
    post=request.POST['post']






    var=User.objects.get(id=id)
    var.name=name
    var.email=email
    var.phone=phone
    var.pin=pin
    var.post=post
    var.age=age
    var.place=place
    var.gender=gender

    if 'image' in request.FILES:
        image = request.FILES['image']
        date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'

        fs = FileSystemStorage()
        fs.save(date, image)
        path = fs.url(date)
        var.image=path
    var.save()


    return HttpResponse('''<script>alert('  Successfull');window.location='/myapp/user_profile/'</script>''')

def send_complaint(request):
    return render(request,'user/send_complaint.html')

def send_complaint_post(request):
    comp=request.POST['complaint']
    var=Complaint()
    var.USER=User.objects.get(LOGIN_id=request.session['lid'])
    var.date=datetime.now().date().today()
    var.complaint=comp
    var.status='pending'
    var.save()
    return HttpResponse('''<script>alert('  Successfull');window.location='/myapp/send_complaint/'</script>''')

def userview_complaint(request):
    var=Complaint.objects.filter(USER__LOGIN_id=request.session['lid'])
    return render(request,'user/view_complaint.html',{'data':var})

def userview_complaint_post(request):
    datef=request.POST['datef']
    datet=request.POST['datet']
    var=Complaint.objects.filter(date__range=[datef,datet])
    return render(request,'user/view_complaint.html',{'data':var})










def sendfeedbackrating(request):
   return render(request, 'user/SENT_REVIEW.html')




def send_feedback_post(request):
    rev=request.POST['textarea']
    rating=request.POST['rating']
    # id=request.POST['aid']
    from datetime import datetime
    robj=Feedback()
    robj.feedback=rev
    robj.rating=rating
    robj.date=datetime.now().strftime("%Y-%m-%d")
    robj.USER=User.objects.get(LOGIN_id=request.session['lid'])
    robj.save()
    return HttpResponse('''<script>alert("successfully send");window.location="/myapp/user_home/"</script>''')

























def login2(request):
    a = request.POST['uname']
    b = request.POST['psw']
    result = Login.objects.filter(username=a, password=b)
    if result.exists():
        result2 = Login.objects.get(username=a, password=b)
        if result2.type == 'user':
            lid=result2.id
            usr=User.objects.get(LOGIN_id=lid)
            # return JsonResponse({'status':"ok",'lid':str(lid)})
            return JsonResponse({'status':"ok",'lid':str(lid),'type':'user','photo':usr.image,'name':usr.name})

        else:
            return JsonResponse({'status': 'not Ok'})
    else:
        return JsonResponse({'status': 'not Ok'})





def user_post_new(request):

    name=request.POST['name']
    phone=request.POST['phone']
    email=request.POST['email']
    gender=request.POST['gender']
    place=request.POST['place']
    pin=request.POST['pin']
    post=request.POST['post']
    age=request.POST['age']
    password=request.POST['password']
    conf=request.POST['confirm']

    if password==conf:
        image = request.POST['image']
        fs1 = base64.b64decode(image)
        date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        open(r'C:\Users\GAYATHRI\PycharmProjects\phishingd\media\user\\' + date1, 'wb').write(fs1)

        path1 = "/media/user/" + date1

        var = Login()
        var.username = email
        var.password = password


        var.type = 'user'
        var.save()

        result = User()
        result.LOGIN = var
        result.name = name
        result.email = email
        result.gender = gender
        result.phone = phone
        result.age=age
        result.pin=pin
        result.post=post
        result.place=place

        result.image=path1
        result.save()
        return JsonResponse({'status': "ok"})
    else:
        return JsonResponse({'status': "Not Ok"})


def user_profile_new(request):

    lid=request.POST['lid']
    var=User.objects.get(LOGIN_id=lid)
    return JsonResponse({'status': "ok",'name':var.name,'email':var.email,'phone':var.phone,'gender':var.gender,'image':var.image,'age':var.age,'place':var.place,'post':var.post,'pin':var.pin})


def edit_userprofile(request):

    lid = request.POST['loginid']
    name = request.POST['name']
    phone = request.POST['phone']
    email = request.POST['email']
    gender = request.POST['gender']
    image = request.POST['image']
    place = request.POST['place']
    pin = request.POST['pin']
    post = request.POST['post']
    age = request.POST['age']

    result = User.objects.get(LOGIN_id=lid)
    result.name = name
    result.email = email
    result.phone=phone
    result.place=place
    result.pin=pin
    result.post=post
    result.age=age

    result.gender = gender

    if len(image) > 1:
        fs1 = base64.b64decode(image)
        date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        open(r'C:\Users\GAYATHRI\PycharmProjects\phishingd\media\user\\' + date1, 'wb').write(fs1)
        path1 = "/media/user/" + date1
        result.image = path1

    result.save()
    return JsonResponse({'status': "ok"})



def user_view_complaints(request):
    var=request.POST['lid']
    var2=User.objects.get(LOGIN=var)
    result=Complaint.objects.filter(USER=var2)
    l =[]
    for i in result:
        l.append({'id':i.id, 'complaint':i.complaint,'date':i.date,'reply':i.reply,'status':i.status})
    return JsonResponse({'status': "ok", 'data':l})

def user_complaint_post(request):
    var=request.POST['comp']
    lid=request.POST['lid']
    date=datetime.now().date().today()

    c_obj=Complaint()
    c_obj.complaint=var
    c_obj.date=date
    uid=User.objects.get(LOGIN_id=lid)
    c_obj.USER=uid
    c_obj.save()

    return JsonResponse({'status': "ok"})



def user_changepassword(request):
    lid = request.POST['lid']
    old = request.POST['old']
    newpass = request.POST['new']
    confirm = request.POST['confirm']

    var = Login.objects.filter(id=lid, password=old)
    if var.exists():
        if newpass == confirm:
            var2 = Login.objects.filter(id=lid).update(password=confirm)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'Not ok'})
    else:
        return JsonResponse({'status': 'NoT Ok'})

def user_feedback_post(request):
    var=request.POST['feed']
    var2=request.POST['rate']
    lid=request.POST['lid']
    date=datetime.now().date().today()


    c_obj=Feedback()
    c_obj.feedback=var
    c_obj.rating=var2
    c_obj.date=date
    uid=User.objects.get(LOGIN_id=lid)
    c_obj.USER=uid
    c_obj.save()

    return JsonResponse({'status': "ok"})






# phishing

def detect(request):
    # lid=request.POST['lid']
    url=request.POST['detect']


    print(url,"-----------------------------------------")
    #Importing dataset
    data = pd.read_csv('C:\\Users\\GAYATHRI\\PycharmProjects\\phishingd\\myapp\\static\\dataset.csv',delimiter=",")

    #Seperating features and labels
    X = np.array(data.iloc[: , :-1])
    y = np.array(data.iloc[: , -1])

    print(type(X))
    #Seperating training features, testing features, training labels & testing labels
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
   # classifier = RandomForestClassifier()
    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    score = score*100
    print(score,"::::::::::::score")

    X_new = []

    from .import feature_extraction

    X_input = url
    X_new=feature_extraction.generate_data_set(X_input)
    X_new = np.array(X_new).reshape(1,-1)

    analysis_result = ""

    try:
        prediction = classifier.predict(X_new)
        print(prediction)
        if prediction == -1:
            analysis_result = "Phishing URL"
        elif prediction == 0:
            analysis_result = "This website has been detected as Suspecious"
        else:
            analysis_result = "This website has been detected as Legitimate URL"
    except Exception as a:
        print(a)
        analysis_result = "This website has been detected as Phishing URL"
        print('result',analysis_result)
        print(a)




    return JsonResponse({'status':'ok','data':analysis_result})

    # result_of_analysis = """<section class="iq-about overview-block-pt iq-hide">
    #                                 <div class="container">
    #                                     <div class="row align-items-end">
    #                                         <div class="col-lg-8 col-md-12">
    #                                             <div class="about-content">
    #                                                 <h1 class="text-about iq-tw-6">Result of Your URL : <span class="iq-font-green iq-fw-8">"""+url+"""</span></h1>
    #                                                 <ul class="listing-mark iq-mtb-20 iq-tw-6 iq-font-black">
    #                                                     <li class="good">"""+analysis_result+"""</li>
    #                                                 </ul>
    #                                                 <h5 class="iq-mt-20 iq-mb-20" style="color: #65d972;font-size: 16px;">Accuracy : """+str(score)+"""div>
    #                                         </div>
    #                                     </div></h5>
    #                                             </
    #                                 </div>
    #                             </section>
    #                             """
    # print(result_of_analysis,"resssssssssssssssssssssult")
    # return result_of_analysis



