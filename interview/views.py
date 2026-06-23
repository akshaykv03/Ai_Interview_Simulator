from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .ai_utils import *
# Create your views here.

def index(request):
    return render(request, 'index.html')

def userReg(request):

    form = UserRegForm()
    if request.method == "POST":
        form = UserRegForm(
            request.POST, request.FILES
        )

        if form.is_valid():
            password = form.cleaned_data['password']

            user = CustomUser.objects.create_user(
                username = form.cleaned_data['email'],
                email = form.cleaned_data['email'],
                password = password,
                userType = 'User')
            
            profile =form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "Registration successful. Please login to continue.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")

    return render(request, 'userReg.html', {'form': form})

def login_view(request):
    
    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user is not None:

                # LOGIN SESSION
                login(request, user)

                # ROLE BASED REDIRECT
                if user.is_superuser:

                    return redirect('adminhome')



                elif user.userType == "User":

                    return redirect('uhome')

                else:

                    messages.error(
                        request,
                        "Invalid user role."
                    )

            else:

                messages.error(
                    request,
                    "Invalid email or password."
                )

    return render(request,
                  'login.html',
                  {'form': form})


def adminhome(request):
    return render(request, 'admin/adminhome.html')




def add_question(request):

    form = QuestionForm()

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Question Added Successfully"
            )

    return render(request,
                  'admin/add_question.html',
                  {'form': form})


def uhome(request):
    return render(request, 'user/uhome.html')

def select_category(request):

    categories = Category.objects.filter(
        question__isnull=False
    ).distinct()

    category_data = []

    for cat in categories:

        req = InterviewRequest.objects.filter(

            user=request.user,

            category=cat

        ).first()

        status = None

        if req:

            status = req.status

        category_data.append({

            'category': cat,

            'status': status
        })

    return render(
        request,
        'user/select_category.html',
        {
            'category_data': category_data
        }
    )




# def start_interview(request, cid):

#     category = Category.objects.get(id=cid)

#     questions = Question.objects.filter(
#         category=category
#     )

#     if request.method == "POST":

#         for q in questions:

#             ans = request.POST.get(
#                 f'answer_{q.id}'
#             )

#             print("ANSWER:", ans)

#             # REMOVE EMPTY SPACES
#             if ans and ans.strip():

#                 similarity = calculate_similarity(
#                     q.correct_answer,
#                     ans
#                 )

#                 marks = calculate_marks(
#                     similarity,
#                     q.marks
#                 )

#                 print("Correct Answer:",
#                       q.correct_answer)

#                 print("User Answer:",
#                       ans)

#                 print("Similarity:",
#                       similarity)

#                 print("Marks:",
#                       marks)

#                 UserAnswer.objects.create(

#                     user=request.user,

#                     question=q,

#                     answer=ans,

#                     similarity_score=similarity,

#                     obtained_marks=marks
#                 )

#         return HttpResponse(
#             "Interview Submitted Successfully"
#         )

#     return render(
#         request,
#         'user/start_interview.html',
#         {
#             'questions': questions,
#             'category': category
#         }
#     )



def start_interview(request, cid):

    category = Category.objects.get(id=cid)

    # BLOCK REATTEMPT
    check_result = InterviewResult.objects.filter(

        user=request.user,

        category=category

    ).first()


    if check_result:

        if check_result.status == 'Malpractice':

            messages.error(request,"Malpractice Detected in this interview. You cannot attempt again.")
            return redirect('/select-category/')

        elif check_result.status == 'Completed':

           messages.info(request,"You have already completed this interview.")
           return redirect('/select-category/')


    questions = Question.objects.filter(
        category=category
    )


    # CREATE RESULT ENTRY
    result, created = InterviewResult.objects.get_or_create(

        user=request.user,

        category=category,

        defaults={

            'status': 'Pending'
        }
    )


    if request.method == "POST":

        total_marks = 0

        obtained_marks = 0

        for q in questions:

            ans = request.POST.get(
                f'answer_{q.id}'
            )

            print("ANSWER:", ans)

            if ans and ans.strip():

                similarity = calculate_similarity(

                    q.correct_answer,

                    ans
                )

                marks = calculate_marks(

                    similarity,

                    q.marks
                )

                total_marks += q.marks

                obtained_marks += marks


                UserAnswer.objects.create(

                    user=request.user,

                    question=q,

                    answer=ans,

                    similarity_score=similarity,

                    obtained_marks=marks
                )


        # SAVE RESULT
        result.total_marks = total_marks

        result.obtained_marks = obtained_marks

        result.status = 'Completed'

        result.save()

        messages.success(
            request,
            "Interview Submitted Successfully"
        )
        return redirect('/select_category')



    return render(

        request,

        'user/start_interview.html',

        {

            'questions': questions,

            'category': category
        }
    )

import cv2
import numpy as np
import base64


from django.http import JsonResponse


def detect_face(request):

    if request.method == "POST":

        image_data =request.POST.get('image')

        image_data =image_data.split(',')[1]

        image_bytes =base64.b64decode(image_data)

        np_arr =np.frombuffer(
                image_bytes,
                np.uint8
            )

        img =cv2.imdecode(
                np_arr,
                cv2.IMREAD_COLOR
            )

        gray =cv2.cvtColor(
                img,
                cv2.COLOR_BGR2GRAY
            )

        face_cascade =cv2.CascadeClassifier(
                'interview/haarcascade_frontalface_default.xml'
            )

        faces =face_cascade.detectMultiScale(
                gray,
                1.1,
                4
            )

        count = len(faces)

        issue = ""

        if count == 0:

            issue = "No Face Detected"

        elif count > 1:

            issue = "Multiple Faces Detected"


        return JsonResponse({

            'face_count': count,
            'issue': issue
        })
    

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def malpractice_detected(request):

    if request.method == "POST":

        cid = request.POST.get(
            'category_id'
        )

        category = Category.objects.get(
            id=cid
        )

        result, created = InterviewResult.objects.get_or_create(

            user=request.user,

            category=category
        )

        # GET ANSWERS
        answers = UserAnswer.objects.filter(

            user=request.user,

            question__category=category
        )

        total = 0

        obtained = 0

        for a in answers:

            total += a.question.marks

            obtained += a.obtained_marks


        result.total_marks = total

        result.obtained_marks = obtained

        result.status = 'Malpractice'

        result.save()


        return JsonResponse({

            'message':
            'Malpractice Saved'
        })


def malpractice(request):

    return render(
        request,
        'user/malpractice.html'
    )


def request_interview(request, cid):

    category = Category.objects.get(id=cid)

    # prevent duplicate request
    exists = InterviewRequest.objects.filter(
        user=request.user,
        category=category
    ).exists()

    if not exists:

        InterviewRequest.objects.create(

            user=request.user,

            category=category,

            status='Pending'
        )

    return redirect('/select-category/')


def view_requests(request):

    requests = InterviewRequest.objects.filter(
        category__question__isnull=False
    ).distinct()

    

    return render(
        request,
        'admin/view_requests.html',
        {
            'requests': requests
        }
    )


def view_results(request):

    results = InterviewResult.objects.filter(
        category__question__isnull=False
    ).distinct()

    return render(
        request,
        'admin/view_results.html',
        {
            'results': results
        }
    )

 

def approve_request(request, req_id):

    req = InterviewRequest.objects.get(id=req_id)

    req.status = 'Approved'

    req.save()

    return redirect('view_requests')


def reject_request(request, req_id):

    req = InterviewRequest.objects.get(id=req_id)

    req.status = 'Rejected'

    req.save()
 
    return redirect('view_requests')


def user_view_results(request):

    results = InterviewResult.objects.filter(
        user=request.user,
        category__question__isnull=False
    ).distinct()

    return render(
        request,
        'user/view_results.html',
        {
            'results': results
        }
    )
 