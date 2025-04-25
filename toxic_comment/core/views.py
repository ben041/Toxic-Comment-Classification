from django.shortcuts import render
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline
from .forms import ToxicCommentForm

# Load the model and tokenizer
MODEL_PATH = "core/models"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer)

def engine_view(request):
    result = None
    analyzed_comment = None
    if request.method == "POST":
        analyzed_comment = request.POST.get("comment")  # Get the user input
        result = pipeline(analyzed_comment)  # Perform the analysis

    return render(request, "engine.html", {"result": result, "analyzed_comment": analyzed_comment})


def word_by_word(request):
    result = None
    word_analysis = []
    analyzed_comment = None
    if request.method == "POST":
        analyzed_comment = request.POST.get("comment")  # Get the user input
        words = analyzed_comment.split()  # Split input into words

        # Analyze each word
        for word in words:
            analysis = pipeline(word)  # Perform analysis on the word
            word_analysis.append({
                "word": word,
                "label": analysis[0]["label"],
                "score": analysis[0]["score"]
            })
    
    return render(request, "word.html", {
        "analyzed_comment": analyzed_comment,
        "word_analysis": word_analysis
    })

def landing_page(request):
    return render(request, 'dashboard.html')

def about(request):
    return render(request, 'about.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Register View
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')  # Changed to match template's password1 field
        
        # Add validation for empty fields
        if not (username and email and password):
            messages.error(request, "All fields are required!")
            return render(request, 'register.html')
            
        # Check if the username or email is already in use
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
        else:
            try:
                # Create a new user with cleaned data
                user = User.objects.create_user(
                    username=username.strip(),
                    email=email.strip(),
                    password=password
                )
                messages.success(request, "Account created successfully!")
                # Log the user in immediately after registration
                login(request, user)
                return redirect('landing_page')
            except Exception as e:
                messages.error(request, "An error occurred during registration.")
                
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Add validation for empty fields
        if not (username and password):
            messages.error(request, "Both username and password are required!")
            return render(request, 'login.html')
            
        # Clean the username input
        username = username.strip()
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('landing_page')
        else:
            messages.error(request, "Invalid username or password!")
            
    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


