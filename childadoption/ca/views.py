from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.views.generic import View
from django.views.generic import UpdateView,ListView,DetailView,TemplateView,CreateView
from ca.models import UserCust,AdoptionRequest,AdoptionFormView,ChildDetails,ConformChild,SponserTable
from ca.forms import UserRegisterForm,LoginForm,DonateForm,UserUpdateForm,SponsorForm
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

from django.core.mail import send_mail




def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            return redirect("login")
    return wrapper


class HomeView(View):
    def get(self,request,*args,**kwargs):
        # user=self.request.user.id
        # print(user) 
        
        return render(request,"home.html")
    

     
class RegisterView(View):
    def get(self,request,*args, **kwargs):
        form=UserRegisterForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.instance.user_type = 'User'
            form.save()
            form=UserRegisterForm()
            
            return redirect('login')
        else:
            return render(request,'register.html',{"form":form})


class LoginView(View):
    def get(self,request,*args,**kwargs):
        form = LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            username=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(request,username=username,password=pwd)
            if user_obj:
                print("VALID CREDENTIALS")
                login(request,user_obj)
                return redirect("home")
            else:
                print("INVALID")
                return render(request,"login.html",{"form":form})


class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("home")


# class SponserView(View):
#     def get(self,request,*args, **kwargs):
#         return render(request,"sponser.html")

    


class DonationView(View):
    def get(self,request,*args,**kwargs):
        
        return render(request,"donation.html")

@method_decorator(signin_required,name="dispatch")
class PrivacyView(View):
    def get(self,request,*args, **kwargs):
        return render(request,"privacy.html")


    
class DonatePayment(View):
    def get(self, request, *args, **kwargs):
        form = DonateForm()
        return render(request, "donatepayment.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = DonateForm(request.POST)
        if form.is_valid():
            user_id=request.user.id
            user_obj=UserCust.objects.get(id=user_id)
            form.instance.personal_details=user_obj
            form.save() 
            form = DonateForm()
            # Add a success message
            messages.success(request, 'Payment received')

            # Redirect to 'home' with success message
            return redirect('home')
        else:
            return render(request, 'donatepayment.html', {"form": form})
    
# class UserProfileEdit(View):
#     def get(self,request,*args, **kwargs):
#         id=self.request.user.id
#         res=UserCust.objects.filter(id=id)
#         form=UserUpdateForm(res)
#         return render(request,"userprofileedit.html",{"form":form})
    
    
#     def post(self,request,*args,**kwargs):
#         id=self.request.user.id
#         res=UserCust.objects.get(id=id)
#         form=UserUpdateForm(request.POST,instance=res)
   
        
#         if form.is_valid():
#             form.save()
#             return redirect("login")
#         return render(request,"userprofileedit.html",{"form":form})

# class UserProfileEdit(View):
#     def get(self, request, *args, **kwargs):
#         user_instance = request.user
#         form = UserUpdateForm(instance=user_instance)

#         return render(request, "userprofileedit.html", {"form": form})
    
#     def post(self, request, *args, **kwargs):
#         user_instance = self.request.user.id
#         form = UserUpdateForm(request.POST, instance=user_instance)
        
#         if form.is_valid():
#             form.save()
#             return redirect("home")
        
#         return render(request, "userprofileedit.html", {"form": form})

class UserProfileEdit(UpdateView):
    template_name="userprofileedit.html"
    form_class=UserUpdateForm
    model=UserCust
    success_url=reverse_lazy("home")


class UserProfile(DetailView):
    template_name="userprofile.html"
    form_class=UserUpdateForm
    model=UserCust
    context_object_name="user"
    
    
class AdoptionRequestView(View):
    
    def get(self, request, *args, **kwargs):
        
        
        return render(request, "adoption.html")
    
    def post(self, request, *args, **kwargs):
        subject = request.POST.get('subject')
        user_id=request.user.id
        user_obj=UserCust.objects.get(id=user_id)
        AdoptionRequest.objects.create(personal_details=user_obj,subject=subject)
        return redirect('home')


# class MessageView(ListView):
#     template_name="messages.html"
#     model=AdoptionRequest
#     context_object_name="message"



class MessageView(TemplateView):
    template_name = 'messages.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Fetch adoption requests and approved messages for the current user
        context['messages'] = AdoptionRequest.objects.filter(personal_details=user)
        context['approved_messages'] = context['messages'].filter(isapproved=True)
        
        # Fetch child detail requests for the current user
        context['childdetailrequests'] = AdoptionFormView.objects.filter(personal_details=user)
        
        # Filter approved requests and requests with feedback
        context['approved_request'] = context['childdetailrequests'].filter(isaccepted=True)
        context['rejected_request'] = context['childdetailrequests'].filter(isaccepted=False, feedback__isnull=False)
        
        # Fetch all child details for display
        context['child_details'] = ChildDetails.objects.all()
        
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     messages = AdoptionRequest.objects.filter(personal_details=user)
    #     approved_messages = messages.filter(isapproved=True)
    #     context['messages'] = messages
    #     context['approved_messages'] = approved_messages
        
    # #THIS IS FOR CHILDDETAILS DISPLAY FOR USER
    #     childdetailrequests = AdoptionFormView.objects.filter(personal_details=user)
    #     approved_request = childdetailrequests.filter(isaccepted=True)
    #     context['childdetailrequests'] = childdetailrequests
    #     context['approved_request'] = approved_request
        
    
    
    #     childrens_list =ChildDetails.objects.all()
    #     context['child_details'] = childrens_list
        
    #     return context
    

    def post(self, request, *args, **kwargs):
        # Handle form submission if needed
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        age = request.POST.get('age')
        marital_status = request.POST.get('marital_status')
        occupation = request.POST.get('occupation')
        income = request.POST.get('income')
        criminal_history = request.POST.get('criminal_history') == 'yes'
        additional_comments = request.POST.get('additional_comments')
        id_proof_file = request.FILES.get('id_proof')
        user_id=request.user.id
        user_obj=UserCust.objects.get(id=user_id)

        # Save the form data to the AdoptionRequest model
        adoption_request = AdoptionFormView(
            personal_details = user_obj,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            age=age,
            marital_status=marital_status,
            occupation=occupation,
            income=income,
            criminal_history=criminal_history,
            additional_comments=additional_comments,
            id_proof=id_proof_file
        )
        adoption_request.save()
        return HttpResponseRedirect(reverse('home'))
        # return super().post(request, *args, **kwargs)
        
# class SelectChild(View):

#     def post(self,request,*args,**kwargs):
#         id=kwargs.get("pk")
#         child_obj=ChildDetails.objects.get(id=id)
#         user=request.user.id
#         user_obj=UserCust.objects.get(id=user)
#         ConformChild.objects.create(child=child_obj,user=user_obj)
#         return redirect("messages")
    
    
       
class SaveModelView(View):
    def save_model(self, request, obj, form, change):
        if change:  
            original_obj = ConformChild.objects.get(pk=obj.pk)
            if not original_obj.isapproved and obj.isapproved:
                user_email = obj.user.email 
                subject = "Child Adoption"
                message = (
                    f"Dear Parents,\n\n"
                    "We are thrilled to inform you that your adoption request has been approved! On behalf of Child Adoption Organization, we extend our warmest congratulations to you and your family."
                    "Your decision to open your heart and home to a child means the world to us and, most importantly, to them. Your kindness and generosity will forever change their life's trajectory, offering them a safe and loving environment to thrive and grow."
                    "As you embark on this incredible journey of parenthood, we want to assure you that our team is here to support you every step of the way. Should you have any questions or need assistance, please don't hesitate to reach out to us."
                    "Once again, congratulations! We look forward to witnessing the beautiful bond that will undoubtedly blossom between you and your new family member."
                    "Best regards,\n"
                    "Child Adoption"
                )
                email_from = "adoptionchild@example.com"
                send_mail(subject, message, email_from, [user_email])

        super().save_model(request, obj, form, change)

class SelectChild(View):
    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        child_obj = ChildDetails.objects.get(id=id)
        user = request.user.id
        user_obj = UserCust.objects.get(id=user)
        conform_child = ConformChild.objects.create(child=child_obj, user=user_obj)
        # Assuming you have a field isapproved in ConformChild model
        if conform_child.isapproved:
            # If the adoption request is approved, send an email to the user
            user_email = user_obj.email
            
            subject = "Child Adoption"
            message = (
                "Your adoption request for the child has been received. "
                "We will review your request and notify you once it's approved."
            )
            email_from = "adoptionchild@example.com"
            send_mail(subject, message, email_from, [user_email])
        return redirect("messages")
    
    
# class SponsorChildView(CreateView):
#     template_name = 'sponser.html'
#     form_class = SponsorForm
#     success_url = reverse_lazy('success_url')

# class SponsorChildView(TemplateView):
#     template_name = 'sponser.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['children'] = ChildDetails.objects.all()
#         return context

#     def post(self, request, *args, **kwargs):
#         child_id = request.POST.get('child_id')
#         sponsor_type = request.POST.get('sponsor_type')
#         amount = request.POST.get('amount')
        
#         if amount:
#             try:
#                 amount = int(amount)
#             except ValueError:
#                 # Handle invalid input for amount
#                 pass
#         else:
#             # Handle case where amount is not provided
#             pass
        
#         if child_id and sponsor_type and amount:
#             child = ChildDetails.objects.get(pk=child_id)
#             user = request.user  # Assuming the user is authenticated

#             # Save sponsorship details to the database
#             SponserTable.objects.create(
#                 user=user,
#                 child=child,
#                 sponsor_type=sponsor_type,
#                 budget=amount
#             )

#         return self.render_to_response(self.get_context_data())
    

    
    
class SponsorChildView(LoginRequiredMixin, TemplateView):
    template_name = 'sponser.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['children'] = ChildDetails.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        child_id = request.POST.get('child_id')
        sponsor_type = request.POST.get('sponsor_type')
        amount = request.POST.get('budget')
        credit_cardno = request.POST.get('credit_cardno')
        exp = request.POST.get('exp')
        ccv = request.POST.get('ccv')

        # Debugging output to inspect the received values
        print("Received data:")
        print(f"child_id: {child_id}, sponsor_type: {sponsor_type}, amount: {amount}, credit_cardno: {credit_cardno}, exp: {exp}, ccv: {ccv}")

        try:
            # Get the child instance
            child = ChildDetails.objects.get(pk=child_id)

            # Get the authenticated user
            user = UserCust.objects.get(pk=request.user)        
            print(user)
            
            sponsorship = SponserTable.objects.create(
                user=user,
                child=child,
                sponsor_type=sponsor_type,
                credit_cardno=credit_cardno,
                exp=exp,
                ccv=ccv,
                budget=amount
            )

            print("Sponsorship saved successfully:", sponsorship)

            # Redirect to a success page or display a success message
            return redirect('sponsor_success')

        except Exception as e:
            print("Error occurred while saving sponsorship:", e)

            # Handle case where form data is incomplete or invalid
            return render(request, self.template_name, {'children': ChildDetails.objects.all()})
        

        
class success_sponcer(TemplateView):
    template_name="sponsor_success.html"    
