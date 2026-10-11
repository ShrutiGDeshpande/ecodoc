from django.shortcuts import render, HttpResponse, redirect
from pyrebase import*
import firebase_admin
from firebase_admin import credentials, auth, storage
from django.http import JsonResponse, HttpResponse
import json
import datetime

config = {
  "apiKey": "AIzaSyABZy-3mRT_t6IlqJU6b0bE6ui4A6Mee9E",
  "authDomain": "documents-b43fb.firebaseapp.com",
  "databaseURL": "https://documents-b43fb-default-rtdb.firebaseio.com",
  "projectId": "documents-b43fb",
  "storageBucket": "documents-b43fb.appspot.com",
  "messagingSenderId": "863812795401",
  "appId": "1:863812795401:web:2c8e58f2b1cc1c23ea8cd8",
  "serviceAccount":"ecodoc/key.json"
};

firebase = pyrebase.initialize_app(config)
service_account_key_path = "ecodoc/key.json"
cred = credentials.Certificate(service_account_key_path)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'storageBucket': 'documents-b43fb.appspot.com'})
else:
    default_app = firebase_admin.get_app()

storage_client = storage.bucket(app=default_app)
db=firebase.database()
Auth = firebase.auth()


#user-login
def login_view(request):
    email = ""
    password = ""
    invalid = ""
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        try:
            auth_user = Auth.sign_in_with_email_and_password(email, password)
            if auth_user:
                print(auth_user)
            # If authentication successful, store user ID in session
                request.session['user_id'] = auth_user['localId'] 
                employee_data = db.child("Employee").order_by_child("email").equal_to(email).get()
                if employee_data.each():
                    employee_id = list(employee_data.val().keys())[0]
                    role = employee_data.val()[employee_id].get("role")
                    print(role)
                    if role.lower()=="admin":
                        database_link="https://console.firebase.google.com/project/documents-b43fb/overview"
                        drive_link="https://drive.google.com/drive/my-drive"
                        return render(request, "admin_dash.html", {"database_link":database_link, "drive_link":drive_link})
                    elif role=="user":
                        return redirect('profile')             
        except:
            invalid="Invalid password"
    return render(request, 'login.html', {'alert_message': invalid})

def add_employee(request):
    selected_projects=[]
    if request.method == "POST":
        id=request.POST.get('ID')
        name=request.POST.get('name')
        email = request.POST.get('email')
        designation=request.POST.get('designation')
        phone_no=request.POST.get('Phone_no')
        password = request.POST.get('password')
        role=request.POST.get('role')
        print(phone_no)
        selected_projects = request.POST.getlist('projects[]')
        selected_projects = [project for project in selected_projects if project]
        data=db.child("Employee").get()
        if (data.pyres is not None) and (str(id) in data.val()):
            return HttpResponse("ID already exists")
        else:        
            info={"id":id,"name":name,'email': email, 'designation': designation, 'phone':phone_no, 'projects':selected_projects, "role":role}
            db.child("Employee").child(id).set(info)
            user_properties = {
            "email": email,
            "password": password,
            "display_name": email
        }
            user = auth.create_user(**user_properties)
            alert_message="Registration successful"      
            return render(request, 'addemp.html',{'alert_message':alert_message})
    else:
        return render(request,'addemp.html')
    
def add_project(request):
    if request.method == "POST":
        id=request.POST.get('ID')
        name=request.POST.get('name')
        password = request.POST.get('password')
        link=request.POST.get('link')
        data=db.child("Projects").get()
        if (data.pyres is not None) and (str(id) in data.val()):
            return HttpResponse("Project already exists")
        else:
            info={"id":id,"name":name,'password': password, 'doclink': link}
            db.child("Projects").child(name).set(info)
            return HttpResponse("Project added")
    else:
        return render(request,'addpro.html')

def session(request):
    user_id = request.session.get('user_id')
    user = auth.get_user(request.session['user_id'])
    username = user.email
    return username

def logout_view(request):
    request.session.clear()
    return redirect('login_view')

def profile_view(request):
    user_id = request.session.get('user_id')
    user = auth.get_user(request.session['user_id'])
    username = user.email
    print(username)
    white_board_link1 = "https://miro.com/app/board/uXjVNlJwQD4=/"
    return render(request, 'profile.html', {"username": username, "white_board_link1": white_board_link1})

def profile(request):
    return render(request,'profile.html')

def collab(request):
    white_board_link="https://app.mural.co/t/ecodoc9200/m/ecodoc9200/1709483836580/acc6b70858e95eb2c80756b7e369c91a32cf7934?sender=u50a55feed624d224102a3292"
    return render(request, 'collab.html',{"white_board_link":white_board_link})

def sch(request):
    return render(request, 'sch.html')

def home(request):
    return render(request, 'home.html')

def todo(request):
    return render(request, 'todo.html')

def kanban_board(request):
    return render(request, 'kanban.html')




#profile-information    
def view_employee(request):
    userid=session(request)
    print(userid) 
    data = db.child("Employee").order_by_child("email").equal_to(userid).get()

    if data.pyres is not None and data.val():
        employee_data = list(data.val().values())[0]
        return render(request, 'user_profile.html', {'employee_data': employee_data})
    else:
        return HttpResponse("Employee not found")
    
def add_achievements(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        userid=session(request)
        print(userid)
        employee_data = db.child("Employee").order_by_child("email").equal_to(userid).get()
        
        if employee_data.each():
            employee_id = list(employee_data.val().keys())[0]
            existing_achievements = employee_data.val()[employee_id].get("achievements", {})
        else:
            return HttpResponse("Employee not found")
        
        existing_achievements[name] = {
            "name": name,
            "description": description
        }
 
        db.child("Employee").child(employee_id).child("achievements").update(existing_achievements)
        mes="Successfully added"
        return render(request, 'add_achievements.html',{'alert_message':mes})       
    else:
        return render(request, 'add_achievements.html')
    
def add_workhistory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        userid=session(request)
        print(userid)
        employee_data = db.child("Employee").order_by_child("email").equal_to(userid).get()
        
        if employee_data.each():
            employee_id = list(employee_data.val().keys())[0]
            existing_history = employee_data.val()[employee_id].get("work_history", {})
        else:
            return HttpResponse("Employee not found")

        existing_history[name] = {
            "name": name,
            "description": description
        }
        
        db.child("Employee").child(employee_id).child("work_history").update(existing_history)
        mes="Successfully added"
        return render(request, 'add_workhistory.html',{'alert_message':mes})       
    else:
        return render(request, 'add_workhistory.html')
    
def add_skills(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        userid=session(request)
        print(userid)
        employee_data = db.child("Employee").order_by_child("email").equal_to(userid).get()
        
        if employee_data.each():
            employee_id = list(employee_data.val().keys())[0]
            existing_skills = employee_data.val()[employee_id].get("skills", {})
        else:
            return HttpResponse("Employee not found")
        
        existing_skills[name] = {
            "name": name,
            "description": description
        }
        
        db.child("Employee").child(employee_id).child("skills").update(existing_skills)
        mes="Successfully added"
        return render(request, 'add_skills.html',{'alert_message':mes})       
    else:
        return render(request, 'add_skills.html')

#project-login-logout
def project_login(request):
    invalid = ""
    if request.method == 'POST':
        name = request.POST.get('pro_name')
        password = request.POST.get('password')
        data = db.child("Projects").child(name).get()

        if data.each():
            project_data = data.each()[0].val()
            if data.val().get("password") == password:
                request.session['project_name'] = name
                google_drive_link=data.val().get("doclink")
                return render(request, 'project.html', {'google_drive_link': google_drive_link})
            else:
                invalid = "Invalid password"
        else:
            invalid = "Project not found"

    return render(request, 'pro_login.html', {'alert_message': invalid})

def logout(request):
    request.session.pop('project_name', None)
    return redirect('project_login')

#employee-directory
def employee_directory(request):
    project_name1 = request.session.get('project_name')
    print(project_name1)
    project_name=project_name1.capitalize()
    data = db.child("Employee").get()

    employees = []
    if data.each():
        for employee in data.each():
            employee_data = employee.val()
            projects = employee_data.get("projects", [])
            if project_name in projects:
                employees.append(employee_data)
        if employees:
            return render(request, 'empdir.html', {'employees': employees})
        else:
            return HttpResponse("No employees associated with project: {}".format(project_name))
    else:
        return HttpResponse("No employees found")
    
def view_empadmin(request):
    if request.method == 'POST': 
        project_name1 = request.POST.get('project')
        if project_name1:
            project_name = project_name1.capitalize()
            data = db.child("Employee").get()

            employees = []
            if data.each():
                for employee in data.each():
                    employee_data = employee.val()
                    projects = employee_data.get("projects", [])
                    if project_name in projects:
                        employees.append(employee_data)
                    print(employees)
                if employees:
                    return render(request, 'view_employee.html', {'employees': employees})
                else:
                    return HttpResponse("No employees associated with project: {}".format(project_name))
            else:
                return HttpResponse("No employees found")
        else:
            return HttpResponse("Please provide a project name")
    return render(request, "view_employee.html")

    
def view_proadmin(request):
        data = db.child("Projects").get()

        projects = []
        if data.each():
            for project in data.each():
                employee_data = project.val()
                projects.append(employee_data)
                print(projects)
            if project:
                return render(request, 'view_projects.html', {'employees': projects})
        else:
            return HttpResponse("No employees found")

def create_zoom_meeting(request):
    zoom_create_meeting_url = "https://zoom.us/meeting/create"
    return redirect(zoom_create_meeting_url)

#kanban-board
def save_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_name = request.session.get('project_name')
            print(project_name)
            task_name = data.get('name')
            description = data.get('description')
            deadline = data.get('deadline')
            print(task_name, description, deadline)
            project_data = db.child('Projects').order_by_child("name").equal_to(project_name).get()
            if project_data.each():
                print(project_data.val())
                existing_tasks = project_data.val().get("kanban", {})

                existing_tasks[task_name] = {
                    "name": task_name,
                    "description": description,
                    "deadline": deadline,
                    "status":"To Do"
                }
                db.child("Projects").child(project_name).child("kanban").update(existing_tasks)
                return JsonResponse({'message': 'Task saved successfully'})
            else:
                return HttpResponse("Employee not found")
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

def delete_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_name = request.session.get('project_name')
            print(project_name) 
            task_name = data.get('taskName')
            print(task_name) 
            project_data = db.child("Projects").order_by_child("name").equal_to(project_name).get()
            if project_data.each():
                employee_id = list(project_data.val().keys())[0]
                existing_tasks = project_data.val()[employee_id].get("kanban", {})           
                if task_name in existing_tasks:
                    existing_tasks.pop(task_name)
                    db.child("Projects").child(employee_id).child("kanban").set(existing_tasks)
                    return JsonResponse({'message': 'Task deleted successfully'})
                else:
                    return HttpResponse("Task not found", status=404)
            else:
                return HttpResponse("Employee not found", status=404)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

   
def move_task_to_column(request):
    if request.method == 'POST':
        data = request.POST
        task_id = data.get('taskName')
        new_column = data.get('newColumn')
        print(task_id)
        project_name = request.session.get('project_name')
        task_data = db.child('Projects').child(project_name).child('kanban').child(task_id)
        task_data.update({'status': new_column})
        return JsonResponse({'message': 'Task status updated'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)



def get_tasks_from_firebase(request):
    if request.method == 'GET':
        project_name = request.session.get('project_name')
        print(project_name)
        tasks = []
        project_data = db.child('Projects').child(project_name).get()
        if project_data.each():
                tasks_data = project_data.val().get("kanban", {})
                print(tasks_data)
                if tasks_data is not None:
                    for task_id, task_data in tasks_data.items():
                        task = {'name': task_id}
                        task.update(task_data)
                        tasks.append(task)
                        print(tasks)
                
                return JsonResponse(tasks, safe=False, status=200)
        
        return JsonResponse({'error': 'No tasks found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

#notification-reminders
def notifications(request):
    tasks = retrieve_tasks_from_firebase(request)
    print(tasks)

    current_date = datetime.datetime.now().date()

    today_tasks = []
    past_due_tasks = []
    two_days_tasks = []

    for task in tasks:
        if (task['status']!="done"):
            deadline = datetime.datetime.strptime(task['deadline'], '%Y-%m-%d').date()
            if deadline == current_date:
                today_tasks.append(task)
            elif deadline < current_date:
                past_due_tasks.append(task)
            elif deadline <= current_date + datetime.timedelta(days=2):
                two_days_tasks.append(task)
    return render(request, 'notify.html', {
        'today_tasks': today_tasks,
        'past_due_tasks': past_due_tasks,
        'two_days_tasks': two_days_tasks
    })

def retrieve_tasks_from_firebase(request):
            userid=session(request)
            print(userid)
            employee_data = db.child("Employee").order_by_child("email").equal_to(userid).get()
            existing_tasks = []
            if employee_data.each():
                employee_id = list(employee_data.val().keys())[0]
                projects_list= employee_data.val()[employee_id].get("projects", {}) 
                print(projects_list)              
                for project in projects_list:
                    project_name = project
                    project_data = db.child('Projects').child(project_name).get()
                    print(project_data)
                    if project_data.each():
                        tasks_data = project_data.val().get("kanban", {})
                        print(tasks_data)
                        if tasks_data is not None:
                            for task_id, task_data in tasks_data.items():
                                task = {
                            "project_name":project_name,
                            "id": task_id,
                            "name": task_data["name"],
                            "description": task_data["description"],
                            "deadline": task_data["deadline"],
                            "status":task_data["status"]
                        }
                                existing_tasks.append(task)
                                print(existing_tasks)
            return existing_tasks

def add_task_todo(request):
    try:
        if request.method == 'POST':
            user_id=session(request)
            print(user_id)
            data = json.loads(request.body)
            task_text = data.get('taskText', '')
            print(task_text)
            existing_tasks=[]
            employee_data = db.child('Employee').order_by_child("email").equal_to(user_id).get()
            if employee_data.each():
                print(employee_data.val())
                employee_id = list(employee_data.val().keys())[0]
                existing_tasks = employee_data.val()[employee_id].get("todo_list", {})
                print(existing_tasks)
                existing_tasks[task_text] = {
                    "name": task_text,
                }
                print(existing_tasks)
                db.child("Employee").child(employee_id).child("todo_list").update(existing_tasks)
                return JsonResponse({'message': 'Task added successfully'})
            else:
                return HttpResponse("Employee not found")
        else:
            return JsonResponse({'error': 'Task text is empty'}, status=400)
    except Exception as e:
        return JsonResponse({'error': "hello"}, status=500)
    
def load_tasks_todo(request):
    if request.method == 'GET':
        user_id=session(request)
        print(user_id)
        tasks = []
        employee_data = db.child('Employee').order_by_child("email").equal_to(user_id).get()
        if employee_data.each():
                print(employee_data.val())
                employee_id = list(employee_data.val().keys())[0]
                task_data = employee_data.val()[employee_id].get("todo_list", {})
                print(task_data)
                if task_data is not None:
                    for task_name, task_data in task_data.items():
                        task = task_name
                        tasks.append(task)
                        print(tasks)
                
                return JsonResponse({'tasks': tasks}, status=200)
        
        return JsonResponse({'error': 'No tasks found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    
def delete_task_todo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id=session(request)
            print(user_id) 
            task_name = data.get('taskText')
            print(task_name) 
            employee_data = db.child("Employee").order_by_child("email").equal_to(user_id).get()
            if employee_data.each():
                employee_id = list(employee_data.val().keys())[0]
                existing_tasks = employee_data.val()[employee_id].get("todo_list", {})           
                if task_name in existing_tasks:
                    existing_tasks.pop(task_name)
                    db.child("Employee").child(employee_id).child("todo_list").set(existing_tasks)
                    return JsonResponse({'message': 'Task deleted successfully'})
                else:
                    return HttpResponse("Task not found", status=404)
            else:
                return HttpResponse("Employee not found", status=404)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    
    
            

                
                
            




















    


    




            
