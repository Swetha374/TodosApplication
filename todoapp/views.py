from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView
from django.contrib.auth.models import User
from todoapp import forms
from django.contrib.auth import authenticate,login,logout
from todoapp.models import Todos
from django.contrib import messages

#class based view for small tasks we can use function based view
#here no serialization and deserialization ,django server is serving html templates
class SignUpView(CreateView):
    model = User
    form_class = forms.RegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"Your account has been created")
        return super().form_valid(form)

    #rendered the form instance in get
    # def get(self,request,*args,**kwargs):
    #     form=forms.RegistrationForm()
    #     return render(request,"registration.html",{"form":form})
    #
    # def post(self,request,*args,**kwargs):  #csrf token sould use wile submitting
    #     #like serializer use form instead of serializer
    #     form=forms.RegistrationForm(request.POST)
    #     """initialized the form using request.POST,instead of request.data.if we didn't gave it the form will be blank
    #         we should save the data send by the user that's we we use request.POST
    #     """
    #     if form.is_valid():#checked is there any errors in the form and what should we do if there is no error
    #         """form.save()   save method can only call if it is model form,form.save will use create method(normal orm query) to save (user.objects.create)
    #         so password will not hashed
    #         we should hash password so we cant use form.save,we should use create_user"""
    #         """**form koduthilel fname,lname baaki ella detailsum elam usernamil keri varum"""
    #         User.objects.create_user(**form.cleaned_data) #here we use cleaned data instead of validated data to create user,cleaned data:data after validation
    #         messages.success(request,"your account has been created")
    #         return redirect("signin") #redirect:which page to redirect(add name given in the path) redirect is in same place of render.loginview->get will work
    #     else: #there is possibility to get errors in the form in that case what to do?
    #         messages.error(request,"registration failed")
    #         return render(request,"registration.html",{"form":form})
    """we need reg page with form not blank page,
        so we should pass context of form then will return the form with data given by user+error message"""

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=forms.LoginForm()
        return render(request,"login.html",{"form":form})

    #uname &pwd edukanam
    def post(self,request,*args,**kwargs):
        #form submitting by user is loginform
        form=forms.LoginForm(request.POST)
        if form.is_valid(): #if form is valid,we need to take values inside uname &pwd using key
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            # check user exist with this credentials passed by the user ,store the user in user bu calling authenticate fn
            user=authenticate(request,username=uname,password=pwd)
            #if user instance is valid go to home
            if user:
                """
                 #if given credentials are true we should store user in a session until logout,django already defined this function as login(request,user)
                 in django side to get logged user we should call login fn login(request,user)
                 """
                login(request,user)
                print("login success")# if login success go to home page
                return redirect("index")
            else: #user not exist go back to login form
                messages.error(request,"invalid username or password")
                print("invalid credentials")
                return render(request, "login.html",{"form":form})
        return render(request,"login.html")

class IndexView(TemplateView): #used for serve a template home
    template_name = "home.html"  #eth templatilekaan render cheyende kodukua
    # ivide e oru template mathram render cheyunnulu.namuk extra context ndhelum add cheyanel get_context_data override cheythamathy
    def get_context_data(self, **kwargs):
      context=super().get_context_data(**kwargs)   #parentil ulla get context data call cheythu
      context["todos"]=Todos.objects.filter(user=self.request.user,status=False)
      #contextilek kurach dict add cheyanam kry todos ayi set cheythu=ndhaaan work cheyenda orm query
      return context

    # def get(self,request,*args,**kwargs):  #this is lowest level(inheriting from view )
    #     return render(request,"home.html")

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request) #remove the authenticated users id from the request and flush their session
        return redirect("signin")
    #in html signout <a href="{%url 'signout'%}">Logout</a> (url+name given in path should gave in href)

class TodoAddView(CreateView):
    model=Todos
    template_name = "add-todo.html"
    form_class =forms.TodoForm            #form render cheyan,createview,updateview il formine render cheyanam
    success_url =reverse_lazy("todolist")       #oru to-do successfully save cheythal save cheyth kazhinjal ndhaan cheyende

    #form save cheyanel userinte instanceilek userne add cheyanam def post method use cheyam.but it will makes the code lengthy do we can override
    #form_valid:form save cheyana munb athinte instancilek ndhelum add cheyan ith override cheythamathy

    def form_valid(self, form):
        form.instance.user=self.request.user #e form aan return super().form_valid(form) ile form
        messages.success(self.request, "todo has been added")
        return super().form_valid(form)

    #ivide formil user und #super().form_valid: call cheyumbo ithinde parent work aavum,avideyaan form.save


    # def get(self, request, *args, **kwargs):
    #     form = forms.TodoForm()
    #     return render(request, "add-todo.html", {"form": form})
    # """ithinu vendi form creayte cheyenda avashyamilla.html pageil form action="{%url 'add-todo'%}" method=post ingane koduthal mathy"""
    # def post(self,request,*args,**kwargs):
    #     form=forms.TodoForm(request.POST)
    #     if form.is_valid():
    #         form.instance.user=request.user
    #         """form save cheyana munb userne edukanam forminte instance(to do) todonte user enna fieldilek logged userine add cheyanam
    #         form should be model form,ennale form.instance kodukkan patu"""
    #         form.save()
    #         """or normal form aanel ithaan kodukende  Todos.objects.create(**form.cleaned_data,user=request.user),form instance ,
    #         for.save add cheyan patathapol"""
    #         messages.success(request,"todo added")
    #         return redirect("index")
    #     else:
    #         messages.error(request,"failed to add")
    #         return render(request, "add-todo.html", {"form": form})

class TodoListView(ListView):
    model=Todos  #which modelinnan list eduth tharande
    context_object_name = "todos"  #contextinte (object name) key ndha kodukende enn django object_list ennan default aayi kodukua,ath override cheyth namuk ishtamullath kodukanam ivide
    template_name = "todolist.html"  #django excepting:modelname_list.html,so namuk ishtamulla name override cheyth kodukam,nammadethaaya template render cheyan template_name override cheythalmaty
#get_queryset: default queryset alathe aha querysetil ndhelum change cheyanel over ride this
    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)
    """
    login cheythitulla userde todos mathram edukan get queryset override cheyanam.get_queryset work cheyumbo default aayit modelname.objects.all() 
    aan work aavua.get_queryset override cheythale namuk filter cheyth login cheytha userinte todos mathram kitu.
    get_queryset override cheyendath custom method orm query work cheyanamenkil.querysetine override cheyanel ingane cheythamathy
    """
    # def get(self, request, *args, **kwargs): #ithelam listviewil predefined aan
    #   all_todos=Todos.objects.filter(user=request.user) #login cheythitulla userinte todos mathram edukan
    #   return render(request, "todolist.html", {"todos": all_todos})   #display cheyan


    """
                {%for todo in todos%}  #for loop is complex task so wrap it on{%%},oro todosine edukan iterate cheyanam todos=contextile key
                <div>{{todo.task_name}}  #display cheyendath
                {{todo.user}}
                {{todo.status}}</div>
            {%endfor%}  #in django template lang start cheythitulla for loop end cheyanam
    """
#function based view
#localhost:8000/todos/remove/<int:id>
def delete_todo(request,*args,**kwargs):
    id=kwargs.get("id")
    todo=Todos.objects.get(id=id).delete()
    return redirect("todolist")

#to get details
class TodoDetailView(DetailView):
    model=Todos
    context_object_name = "todo"
    template_name = "todo-detail.html"
    pk_url_kwarg = "id"  #id pk or slug enn thanne kodukkanam default aayi pk aan,pk namuk  guess cheyan patum slug patilla random ayirikum.
    # so pk override cheyth id koduthal namuk<int:id> ,"id" kodukam



    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     todo=Todos.objects.get(id=id)
    #     return render(request,"todo-detail.html",{"todo":todo})

#update
class TodoEditView(UpdateView):
    model=Todos
    form_class = forms.TodoChangeForm
    template_name = "todo-edit.html"
    pk_url_kwarg = "id"
    success_url =reverse_lazy("todolist")

    def form_valid(self, form):
        messages.success(self.request, "todo has been changed")
        return super().form_valid(form)
    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     todo=Todos.objects.get(id=id)
    #     form=forms.TodoChangeForm(instance=todo) #blank form alla eth todonte instance vachano form initialize cheyende ath
    #     return render(request,"todo-edit.html",{"form":form})
    # def post(self,request,*args,**kwargs):
    #     id= kwargs.get("id")
    #     todo = Todos.objects.get(id=id)
    #     form=forms.TodoChangeForm(request.POST,instance=todo) #update aanenkil mention cheyanam instance
    #     if form.is_valid():
    #         form.save()
    #         msg="todo has been changed"
    #         messages.success(request,msg) #to show messages  messages.add_message(request,msg content)
    #         return redirect("todolist")
    #     else:
    #         msg="todo update failed"
    #         messages.error(request,msg)
    #         return render(request, "todo-edit.html", {"form": form})

 #boiler plate code :code duplication

 #create view:
"""view for creating a new object,with a response rendered by a template.
template_name override cheyanam else django expect name_form.html
as template_name"""
 #edit
 #delete
 #list
 #detail