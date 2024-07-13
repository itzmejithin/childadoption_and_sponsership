from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ca.models import CustomUser, SuperAdmin, UserCust,Donate,AdoptionRequest,AdoptionFormView,ChildDetails,ConformChild,SponserTable
from django.db.models import Sum
#THIS IS FOR MAIL
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class UserCustAdmin(admin.ModelAdmin):
    list_display = ('username', 'fname', 'lname', 'emailaddress', 'gender', 'location', 'addresss', 'phone_number')
    search_fields = ('username', 'fname', 'lname', 'emailaddress', 'gender', 'location', 'addresss', 'phone_number')

    def has_add_permission(self, request):
        # Disable the ability to add UserCust instances
        return False

    def has_change_permission(self, request, obj=None):
        # Disable the ability to change UserCust instances
        return False

    # def has_delete_permission(self, request, obj=None):
    #     # Disable the ability to delete UserCust instances
    #     return False

admin.site.register(UserCust, UserCustAdmin)


class DonateAdmin(admin.ModelAdmin):
    list_display = ('personal_details', 'credict_cardno', 'exp', 'amount')
    search_fields = ('personal_details__username', 'credict_cardno')
    readonly_fields = ('credict_cardno', 'exp', 'ccv', 'amount')  # Make fields read-only

    def has_add_permission(self, request):
        # Disable the ability to add Donate instances
        return False

    def has_change_permission(self, request, obj=None):
        # Only superusers can view Donate instances
        return request.user.is_superuser

    # def has_delete_permission(self, request, obj=None):
    #     # Disable the ability to delete Donate instances
    #     return False

admin.site.register(Donate, DonateAdmin)
# Change verbose name for the model
Donate._meta.verbose_name_plural = 'Donations'


# class UserCustAdmin(admin.ModelAdmin):
#     list_display = ('username', 'total_donation')

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         queryset = queryset.annotate(total_donation=Sum('donate__amount'))
#         return queryset

#     def total_donation(self, obj):
#         return obj.total_donation

#     total_donation.admin_order_field = 'total_donation'


class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('personal_details', 'subject')  # Corrected list_display
    search_fields = ('personal_details__username', 'subject')
    readonly_fields = ('personal_details', 'subject')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    # def has_delete_permission(self, request, obj=None):
    #     return False

admin.site.register(AdoptionRequest, AdoptionRequestAdmin)


class AdoptionFormViewAdmin(admin.ModelAdmin):
    list_display = ('personal_details', 'full_name', 'email', 'phone', 'address', 'age', 'marital_status', 'occupation', 'income', 'criminal_history', 'additional_comments', 'id_proof', 'isaccepted','feedback')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('personal_details', 'full_name', 'email', 'phone', 'address', 'age', 'marital_status', 'occupation', 'income', 'criminal_history', 'additional_comments', 'id_proof')  # Fields you want to be read-only
    list_filter = ('feedback','isaccepted')
    def has_add_permission(self, request):
        # Disable the ability to add instances
        return False

    def has_change_permission(self, request, obj=None):
        # Only superusers can view instances
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        # Disable the ability to delete instances
        return False

admin.site.register(AdoptionFormView, AdoptionFormViewAdmin)
AdoptionFormView._meta.verbose_name_plural = 'Adoption Form Requests'




admin.site.register(ChildDetails)


class ChildRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'child', 'isapproved')
    search_fields = ('user__username', 'child__name')  
    readonly_fields = ('user', 'child')
    list_filter = ('isapproved',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if change:  
            original_obj = ConformChild.objects.get(pk=obj.pk)
            print("orginal",original_obj)
            if not original_obj.isapproved and obj.isapproved:
                user_email = original_obj.user.emailaddress 
                print("user",user_email)    
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
                email_from = "adoptionchild7@gmail.com"
                email_to = user_email
                print("to email",email_to)
                send_mail(subject, message, email_from, [email_to])
        super().save_model(request, obj, form, change)

admin.site.register(ConformChild, ChildRequestAdmin)
ConformChild._meta.verbose_name_plural = 'Child Requests'




# admin.site.register(SponserTable)
class SponserTableAdmin(admin.ModelAdmin):
    list_display = ('user', 'child', 'sponsor_type', 'credit_cardno', 'exp', 'ccv', 'budget')
    search_fields = ('user', 'child', 'sponsor_type', 'credit_cardno', 'exp', 'ccv', 'budget')

    def has_add_permission(self, request):
        # Disable the ability to add UserCust instances
        return False

    def has_change_permission(self, request, obj=None):
        # Disable the ability to change UserCust instances
        return False

    def has_delete_permission(self, request, obj=None):
        # Disable the ability to delete UserCust instances
        return False

admin.site.register(SponserTable, SponserTableAdmin)
