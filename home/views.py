import contextvars
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import userprofile,posts,Message
from django.contrib.auth import authenticate ,logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date,datetime
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def signup(request):
    return render(request,'home/loginpage.html')

def register(request):
    return render(request,'home/register.html')

def handleSignup(request):
    if request.method =='POST':
            # get the post parameters
            uname = request.POST["uname"]
            fname=request.POST["fname"]
            lname=request.POST["lname"]
            email = request.POST["email"]
            pass1 = request.POST["pass1"]
            pass2 = request.POST["pass2"]
            gender = request.POST["gender"]
            dob = request.POST["dob"]
            dp = request.FILES["dp"]
            profile = userprofile()
            
            # check for errors in input
            if request.method == 'POST':
                try:
                    user_exists = User.objects.get(username=request.POST['uname'])
                    messages.error(request," Username already taken, Try something else!!!")
                    return redirect("/")    
                except User.DoesNotExist:
                    if pass1!=pass2:
                        messages.error(request," password missmatch")
                        return redirect("/")
                    if len(uname)>15:
                        messages.error(request," Username must be max 15 characters, Please try again")
                        return redirect("/")
            
                    if not uname.isalnum():
                        messages.error(request," Username should only contain letters and numbers, Please try again")
                        return redirect("/")
                    todays = datetime.today().strftime('%Y-%m-%d')
                    todays = datetime.strptime(todays,'%Y-%m-%d')
                    times = datetime.strptime(dob,'%Y-%m-%d')
                    print(times)
                    print(todays)
                    res = (todays-times).days/365.25
                    print(res)
                    if res <18:
                        messages.error(request," Age should greater than 18.")
                        return redirect("/")
            #times = datetime.strptime(dob,'%Y-%m-%d')
            # create the user
            user = User.objects.create_user(uname, email, pass1)
            user.username = uname
            user.first_name=fname
            user.last_name=lname
            user.email = email
            user.gender = gender
            user.save()
            profile.dp = dp
            #profile.dob = datetime.strptime(dob,'%Y-%m-%d')
            profile.user = user
            profile.save()
            messages.success(request," Your account has been successfully created")
            return redirect("/")
    else:
        return HttpResponse('404 - NOT FOUND ')

def handlelogin(request):
    if request.method =='POST':
        # get the post parameters
        loginuname = request.POST["loginuname"]
        loginpassword1=request.POST["loginpassword1"]
        user = authenticate(username=loginuname, password=loginpassword1)
        if user is not None:
            dj_login(request, user)
            request.session['is_logged'] = True
            user = request.user.id 
            request.session["user_id"] = user
            return redirect('/')
        else:
            messages.error(request," Invalid Credentials, Please try again")  
            return redirect("/")  
    return HttpResponse('404-not found')

def handlelogout(request):
        del request.session['is_logged']
        del request.session["user_id"] 
        logout(request)
        messages.success(request, " Successfully logged out")
        return redirect('/')

def follow(request,id):
    x = userprofile.objects.get(user=request.user)
    print(x)
    y = userprofile.objects.get(user=id)
    print(y)
    if request.user in y.followers.all():
        print("exists")
        x.following.remove(id)
        y.followers.remove(request.user)
        y.total_followers-=1
        x.total_followings-=1
    else:
        print("not exists")
        x.following.add(id)
        y.followers.add(request.user)
        y.total_followers+=1
        x.total_followings+=1
    x.save()
    y.save()
    return redirect('/profile/'+id)

def post_picture(request):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user_id = request.session["user_id"]
            user1 = userprofile.objects.get(user=user_id)
            #post = posts.objects.filter(post_by=user1)
            pic = request.FILES["pic"]
            caption = request.POST["caption"]
            add = posts()
            add.post_by = user1
            add.pic=pic
            add.post_date = date.today()
            add.caption = caption
            add.save()
            #return redirect(home)
    return redirect('/')


def likepost(request,id):
    x = posts.objects.get(post_id=id)
    if request.user in x.liked_by.all():
        x.liked_by.remove(request.user)
        x.likes-=1  
          
    else:
        x.liked_by.add(request.user)
        x.likes+=1
        
    x.save()
    return redirect('/dashboard/')

def comment(request):
    x = posts.objects.get(post_id = request.POST["post_id"])
    x.comments = request.POST["comment"]
    x.save()

def explore(request):
    x = posts.objects.all()
    context = {
        "post":x
    }
    return render(request,"home/explore.html",context)

def dashboard(request):
    if request.session.has_key('is_logged'):
        x = userprofile.objects.get(user = request.user)
        print(x,"user")
        all = []
        #active_user = []
        #a_c = userprofile.objects.filter(last_login=now()-timedelta(minutes=1))
        data = x.following.all()
        # if a_c in data:
        #     active_user.append(a_c)
        foll = []
        print(data,"data following")
        if data:
            for t in data:
                user1 = userprofile.objects.get(user=t)
                foll.append(user1)
                y=posts.objects.filter(post_by = user1).order_by('-post_date')
                print(y,"posts")
                for v in y:
                    print(v.pic,"picture_url")
                    all.append(v)
        
        print(all,"list context")
        context = {
            "data":all,
            "me":x,
            "foll": foll ,
        }
        return render(request,'home/socio.html',context)
    else:
        return render(request,'home/loginpage.html')


@login_required
def inbox(request):
    msguser = request.user
    ins = userprofile.objects.get(user=request.user)
    messages = Message.get_message(user=ins)
    active_direct = None
    directs = None
    profile = get_object_or_404(userprofile, user=msguser)

    if messages:
        message = messages[0]
        active_direct = message['user'].user.username
        reciever = userprofile.objects.get(user=message['user'].user)
        sender = userprofile.objects.get(user=request.user)
        directs = Message.objects.filter(msguser=sender, reciepient=reciever)
        directs.update(is_read=True)
        ans = []
        for message in messages:
            if message['user'].user.username == active_direct:
                message['unread'] = 0
            a = User.objects.get(username = message['user'].user.username)
            print(a)
            tele = userprofile.objects.get(user=a)
            ans.append(tele)
    context = {
        'directs':directs,
        'messages': messages,
        'active_direct': active_direct,
        'profile': profile,
        'ans':ans
    }
    return render(request, 'home/direct.html', context)


@login_required
def Directs(request, username):
    user  = userprofile.objects.get(user=request.user)
    print(user)
    messages = Message.get_message(user=user)
    print(messages)
    au = User.objects.get(username=username)
    active_direct = userprofile.objects.get(user=au)
    directs = Message.objects.filter(msguser=user, reciepient=active_direct)  
    directs.update(is_read=True)
    
    for message in messages:
            if message['user'].user.username == username:
                message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }
    return render(request, 'home/direct.html', context)

def profile(request,id):
    x = userprofile.objects.get(user=id)
    y = posts.objects.filter(post_by=x)
    t = y.count()
    context = {
        "data":x,
        "post":y,
        "t":t
    }
    return render(request,"home/profile.html",context)


def SendDirect(request):
    from_user = userprofile.objects.get(user=request.user)
    to_user_username = request.POST['to_user']
    body = request.POST['body']
    if request.method == "POST":
        ac = User.objects.get(username=to_user_username)
        to_user = userprofile.objects.get(user=ac)
        Message.sender_message(from_user, to_user, body)
    return redirect('/direct/'+str(to_user_username))
    

def NewConversation(request, username):
    from_user = request.user
    body = ''
    try:
        to_user = userprofile.objects.get(user=username)
    except Exception as e:
        return redirect('/')
    if from_user != to_user:
        Message.sender_message(from_user, to_user, body)
        return redirect('inbox/')


def search(request):
    query = request.GET.get('q')
    context = {}
    if query:
        users = userprofile.objects.filter(Q(user__username__icontains=query))
        # for i in users:
        # # Paginator
        #     print(i.dp.url)
        context = {
            'users': users,
            }

    return render(request, 'home/search.html', context)
