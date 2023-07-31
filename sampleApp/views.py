from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book, User, Category
from .forms import BookForm, LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import BookIssue
from datetime import timedelta
from datetime import date
import pytz
from django.utils import timezone
import random

# Create your views here.

def update1(request, book_id, user_id):
    print("h5")
    book = get_object_or_404(Book, pk=book_id)
    user = get_object_or_404(User, pk=user_id)
    issued_at=timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))
    returned_at = issued_at + timedelta(days=30)

    
    # Check if the book is available
    if book.availability > 0:
        # Calculate the issue and return dates in Indian Standard Time (IST)
        tz = pytz.timezone('Asia/Kolkata')
        issued_at = timezone.now().astimezone(tz)
        returned_at = issued_at + timedelta(days=30)

        # Create a new BookIssue record and set the issued_at and returned_at timestamps
        issue = BookIssue(user=user, book=book, issued_at=issued_at, returned_at=returned_at)
        issue.save()

        # Update the availability of the book and save it
        book.availability -= 1
        book.save()

        # Get all issued books for rendering in the template
        issued_books = BookIssue.objects.select_related('book', 'user').all()

        # Get the referring URL (current page)
        referring_url = request.META.get('HTTP_REFERER', '/')
        

        # Redirect the user back to the current page with the updated issued books list
    
        return redirect('/book/'+book_id)
    else:
        # Book is not available, handle this case as needed (e.g., show an error message)
        print("No books available")
        # You can also pass an error message to the template if you wish:
        return redirect('/book/'+book_id)



def index(request):
    users = User.objects.all()
    books = Book.objects.all()  # Fetch all book objects from the database
    categories = Category.objects.all()
    booksrand = []
    for i in range(5):
        rand = random.choice(books)
        while(rand in booksrand):
            rand = random.choice(books)
        booksrand.append(rand)
    
    dict={}
    for user in users:
        issued_books = BookIssue.objects.select_related('book').filter(user=user).count()
        print(issued_books)
        dict[user.id]=issued_books
        
    
    sorted_list=[key for key,value in sorted(dict.items() ,key=lambda x : x[1],reverse=True) ]

    # top_users=User.objects.filter(id__in=sorted_list[0:3])
    top_users=User.objects.filter(id__in=sorted_list[0:3])
    print(top_users)

    return render(request, 'index.html', {'books': booksrand, 'all_categories': categories[4:], 'categories': categories[0:4], 'top_users':top_users})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        print("wow")
        if form.is_valid():
            form.save()
            print("hi")
            # Replace 'book_list' with the name of your view to display the book list.
            return redirect('index')
    else:
        print("bye")
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})


def register(request):
    if request.method == 'POST':
        print("h2")
        form = RegistrationForm(request.POST,request.FILES)
        print("h3")
        print(form.errors)
        if form.is_valid():
            print("h1")
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            email = form.cleaned_data['email']
            user.email = email
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print("hi")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)

                # Replace 'index' with your desired homepage URL
                return redirect('index')

            else:
                messages.error(
                    request, 'Invalid credentials. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def update(request, book_id, user_id):

    book = Book.objects.get(pk=book_id)
    user = User.objects.get(pk=user_id)
    if (book.availability >= 0):
        book.availability -= 1
    else:
        print("No books available")

    book.save()
    user.cart_books.add(book)
    return redirect('index')


def update_user(request, user_id):
    print(user_id)



def view_book(request,book_id):
    book = Book.objects.get(pk=book_id)
    user_id=request.user.id
    user=User.objects.get(pk=user_id)
    issued_books = BookIssue.objects.filter(user=user,book=book).count()
    print(issued_books)

    # You can pass the `book` object to the template or perform any other actions as needed

    return render(request, 'book.html', {'book': book , 'issued_books':issued_books,'count':issued_books})


def profile(request):
    user = request.user
    issued_books = BookIssue.objects.select_related('book').filter(user=user)
    return render(request, 'profile.html',{'user': user, 'issued_books':issued_books})

def category(request, categoryid):
    category = Category.objects.get(id=categoryid)
    books = Book.objects.filter(categories=category)
    return render(request, 'books.html', {'books': books, 'category': category})

def logout(request):
    auth_logout(request)
    return redirect('login')
