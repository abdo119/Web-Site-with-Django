from threading import Timer

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, auth


# Create your views here.

def login(request):
    if not request.session.has_key('email'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        flag = False
        for obj in User.objects.all():
            if obj.email == email and obj.check_password(password):
                name = obj.username
                for o in Client.objects.all():
                    if o.email == email:
                        o.active = True
                        break
                flag = True
                break
        if flag:
            request.session['email'] = email
            request.session['name'] = name
            request.session['password'] = password
            if email == 'admin@gmail.com':
                return redirect('adminHome')
            else:
                return redirect('home')
        else:
            if email is not None or password is not None:
                messages.error(request, 'This email Notfound')
    else:
        return redirect('home')

    return render(request, 'pages/logIn.html')


def logOut(request):
    username = "default"
    if request.session.has_key('email'):
        username = request.session['email']
        for obj in User.objects.all():
            if obj.email == username:
                if request.session['email'] != 'admin@gmail.com':
                    for o in Client.objects.all():
                        if o.email == request.session['email']:
                            o.active = False
                            o.save()
                            break
                    obj.is_active = False
                    obj.save()

        request.session.modified = True
        del request.session['email']
    else:
        return render(request, 'pages/getStart.html')
    return render(request, 'pages/getStart.html')


def home(request):
    e = 'default'
    if request.session.has_key('email'):
        e = request.session['email']
    if request.session.has_key('email') and not e.__contains__("@admin.com"):
        username = request.session['name']
    else:
        if request.session.has_key('email') and e.__contains__("@admin.com"):
            return redirect('adminHome')
        else:
            return redirect('getStart')

    return render(request, 'pages/userHome.html', {"x": username})


def adminHome(request):
    e = 'default'
    if request.session.has_key('email'):
        e = request.session['email']
    if request.session.has_key('email') and e.__contains__("@admin.com"):
        username = request.session['name']
    else:
        if request.session.has_key('email'):
            return redirect('home')
        else:

            return redirect('getStart')

    return render(request, 'pages/adminHome.html', {"x": username})


def signUp(request):
    if not request.session.has_key('email'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('secondPassword')
        if confirm == password:
            flag = True
            for obj in User.objects.all():
                if obj.email == email:
                    flag = False
                    break
            if flag:
                if name is not None or email is not None or password is not None:
                    data = Client(name=name, password=password, email=email)
                    data.active = True
                    data.save()
                    user = User.objects.create_user(name, email, password)
                    user.is_active = True
                    request.session['email'] = email
                    request.session['name'] = name
                    user.save()
                    return redirect('home')

            else:
                messages.error(request, 'This email already exist!!')
        else:
            messages.error(request, 'Password and confirm Password not same!')
    else:
        return redirect('home')
    return render(request, 'pages/signUp.html')


def getStart(request):
    if request.session.has_key('email'):
        e = request.session['email']
        if e.__contains__("@admin.com"):
            return redirect('adminHome')
        else:
            return redirect('home')
    return render(request, 'pages/getStart.html')


def updateUser(request):
    e = 'default'
    if request.session.has_key('email'):
        e = request.session['email']
    if request.session.has_key('email') and not e.__contains__("@admin.com"):
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if name is not None or email is not None or password is not None:
            for obj in User.objects.all():
                if obj.email == request.session['email']:
                    obj.set_password(password)
                    obj.email = email
                    obj.username = name
                    obj.save()
            for obj in Client.objects.all():
                if obj.email == request.session['email']:
                    obj.email = email
                    obj.name = name
                    obj.password = password
                    obj.active = True
                    obj.save()
            request.session.modified = True
            request.session['email'] = email
            request.session['name'] = name
            request.session['password'] = password
            return redirect('home')
    else:
        if e.__contains__("@admin.com"):
            return redirect('adminHome')
        else:
            return redirect('getStart')

    return render(request, 'pages/updateUser.html')


def updateBook(request):
    e = 'default'
    if request.session.has_key('email'):
        e = request.session['email']
    if request.session.has_key('email') and e.__contains__("@admin.com"):
        curIsbn = request.POST.get('oldIsbn')
        newIsbn = request.POST.get('newIsbn')
        date = request.POST.get('date')
        author = request.POST.get('author')
        if curIsbn is not None:
            for obj in Books.objects.all():
                if curIsbn == obj.ISBN:
                    obj.ISBN = newIsbn
                    obj.publishedYear = date
                    obj.author = author
                    obj.save()
                    return redirect('adminHome')
    else:
        if request.session.has_key('email'):
            return redirect('home')
        else:

            return redirect('getStart')
    return render(request, 'pages/updateBook.html')


def borrowBook(request):
    e = 'default'
    if request.session.has_key('email'):
        e = request.session['email']
    if request.session.has_key('email') and not e.__contains__("@admin.com"):
        isbn = request.POST.get('isbn')
        time = request.POST.get('time')
        if isbn is not None:
            data = Borrow(ISBN=isbn, time=time, user=Client.objects.get(email=request.session['email']),
                          img=Books.objects.get(ISBN=isbn).img)
            data.save()
            book = Books.objects.get(ISBN=isbn)
            book.user = Client.objects.get(email=request.session['email'])
            book.active = False
            book.save()
            return redirect('home')
        return render(request, 'pages/borrowBook.html', {'x': Books.objects.all()})
    elif request.session.has_key('email') and e.__contains__("@admin.com"):
        return redirect('adminHome')
    else:
        return redirect('getStart')


def addBook(request):
    e = 'default'
    if request.session.has_key('email'):
        e = request.session['email']
    if request.session.has_key('email') and e.__contains__("@admin.com"):
        isbn = request.POST.get('isbn')
        date = request.POST.get('date')
        img = request.POST.get('image')
        author = request.POST.get('author')
        if isbn is not None:
            book = Books(ISBN=isbn, publishedYear=date, img=img, author=author)
            book.save()
            return redirect('adminHome')
    elif request.session.has_key('email') and not e.__contains__("@admin.com"):
        return redirect('home')
    else:
        return redirect('getStart')
    return render(request, 'pages/addBook.html')


def backBook(request):
    e = 'default'
    if request.session.has_key('email'):
        e = request.session['email']
    user = request.session['email']
    isbn = request.POST.get('isbn')
    time = request.POST.get('time')
    if request.session.has_key('email') and not e.__contains__("@admin.com"):
        if time is not None:
            book = Borrow.objects.get(ISBN=isbn)
            book.time += int(time)
            book.save()
            return redirect('home')
        return render(request, 'pages/myBook.html', {'x': Borrow.objects.all(), 'email': user})

    elif request.session.has_key('email') and e.__contains__("@admin.com"):
        return redirect('adminHome')
    else:
        return redirect('getStart')


def back(request):
    e = 'default'
    if request.session.has_key('email'):
        e = request.session['email']
    if request.session.has_key('email') and not e.__contains__("@admin.com"):
        isbn = request.GET.get('isbn')
        if isbn is not None:
            book = Books.objects.get(ISBN=isbn)
            book.user = None
            book.active = True
            book.save()
            bor = Borrow.objects.get(ISBN=isbn)
            bor.delete()
            return redirect('home')

    elif request.session.has_key('email') and e.__contains__("@admin.com"):
        return redirect('adminHome')
    else:
        return redirect('getStart')


def extend(request):
    e = 'default'
    if request.session.has_key('email'):
        e = request.session['email']
    if request.session.has_key('email') and not e.__contains__("@admin.com"):
        time = request.GET.get('time')
        isbn = request.GET.get('isbn')
        if time is not None:
            book = Borrow.objects.get(ISBN=isbn)
            book.time += int(time)
            book.save()
    elif request.session.has_key('email') and e.__contains__("@admin.com"):
        return redirect('adminHome')
    else:
        return redirect('getStart')


def browsingAdmin(request):
    e = 'default'
    if request.session.has_key('email'):
        e = request.session['email']
    if request.session.has_key('email') and e.__contains__("@admin.com"):
        curIsbn = request.POST.get('oldIsbn')
        newIsbn = request.POST.get('newIsbn')
        date = request.POST.get('date')
        author = request.POST.get('author')
        if curIsbn is not None:
            for obj in Books.objects.all():
                if curIsbn == obj.ISBN:
                    obj.ISBN = newIsbn
                    obj.publishedYear = date
                    obj.author = author
                    obj.save()
                    return redirect('adminHome')
    else:
        if request.session.has_key('email'):
            return redirect('home')
        else:
            return redirect('getStart')
    return render(request, 'pages/adminBrowsing.html', {'x': Books.objects.all()})


def about(request):
    if request.session.has_key('email'):
        return render(request, 'pages/about.html')
    else:
        return redirect('login')
