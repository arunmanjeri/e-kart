from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import Account,User_otp,UserProfile,UserFeedback
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
import random
from .forms import UserProfileForm,UserForm
from django.core.mail import EmailMessage
from kart.models import CartItem
from kart.views import cart_id_gen
from django.http import HttpResponseRedirect
from whishlist.models import Whishlist
from whishlist.views import whishlist_id_gen
from payment.models import Order,OrderProduct,Payment

def otp_generator(user):
    try:
        otp=str(random.randint(100000,999999))
        if User_otp.objects.filter(user=user):
            otp_gen=User_otp.objects.get(user=user)
            otp_gen.otp=otp
            otp_gen.save()
        else:
            otp_gen=User_otp(user=user, otp=otp)
            otp_gen.save()
        try:
            mail_subject='Welcome Ekart, Please Activate Account'
            message='Hi '+user.first_name+user.last_name+' welcome to eshop. Your otp for account activation is '+otp+' Please ignore this message, if it is not you!'
            to_email=user.email
            send_mail=EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()
        except:
            pass
    except:
        pass

def  register_user(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        repeat_password=request.POST['repeat_password']
        phone_number=request.POST['phone_number']
        username=email
        try:
            if Account.objects.filter(email=email).exists():
                messages.error(request,'User is exists, Please login')
                return redirect('login_user')
            else:
                if password == repeat_password:
                    user=Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                    user.phone_number=phone_number
                    user.save()
                    otp_generator(user)
                    messages.success(request,'Please enter otp, sent to your registered email')
                    return redirect('verify_user')
                else:
                    messages.error(request,'Password mis-match')
                    return redirect('register_user')
        except:
            pass
    return render(request,'accounts/register_user.html')

def  login_user(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        if Account.objects.filter(email=email, is_active=True).exists():
            user=auth.authenticate(email=email, password=password)
            if user is not None:
                try:
                #cart add user
                    obj=CartItem.objects.filter(cart_id=cart_id_gen(request))
                    for i in obj:
                        i.user=user
                        i.save()
                except:
                    pass

                try:
                #whishlist add user
                    obj=Whishlist.objects.filter(whishlist_id=whishlist_id_gen(request))
                    for i in obj:
                        i.user=user
                        i.save()
                except:
                    pass

                auth.login(request, user)
                url=request.META.get('HTTP_REFERER')
                if 'login' in url:
                    return redirect('dashboard')
                return HttpResponseRedirect(url)
            else:
                messages.error(request,'Invalid login credential')
                return redirect('login_user')
        elif Account.objects.filter(email=email, is_active=False).exists():
            user=Account.objects.get(email=email)
            otp_generator(user)
            messages.success(request,'PLease activate your account, we sent an otp to your mail')
            return redirect('verify_user')
        else:
            messages.error(request,'User not exists, please signup')
            return redirect('login_user')
    return render(request,'accounts/login_user.html')

@login_required(login_url='login_user')
def  logout_user(request):
    auth.logout(request)
    messages.success(request,'You are logged out')
    return redirect('login_user')

def  verify_user(request):
    if request.method == 'POST':
        email=request.POST['email']
        otp=request.POST['otp']
        user=Account.objects.get(email=email)

        if User_otp.objects.filter(user=user, otp=otp).exists():
            user.is_active=True
            user.save()
            try:
                messages.success(request,'Activation success, Please login')
                mail_subject='Welcome Ekart, Please make your purchase'
                message='Hi '+user.first_name+user.last_name+' welcome to eshop. Your account is activated, Please ignore this message, if it is not you!'
                to_email=user.email
                send_mail=EmailMessage(mail_subject,message,to=[to_email])
                send_mail.send()
            except:
                pass
            return redirect('login_user')
    return render(request,'accounts/verify_user.html')


def forgotpassword(request):
    if request.method == 'POST':
        email=request.POST['email']
        user=Account.objects.get(email=email)
        otp=str(random.randint(100000,999999))
        if User_otp.objects.filter(user=user).exists():
            otp_gen=User_otp.objects.get(user=user)
            otp_gen.otp=otp
            otp_gen.save()
        else:
            otp_gen=User_otp(user=user, otp=otp)
            otp_gen.save()
        try:
            mail_subject='Welcome Ekart, forgot password'
            message='Hi '+user.first_name+user.last_name+' welcome to eshop. Your otp for Resetpassword is '+otp+' Please ignore this message, if it is not you!'
            to_email=user.email
            send_mail=EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()
        except:
            pass
        messages.success(request,'Please check your mail for otp')
        context={
            'user':user,
        }
        return render(request,'accounts/resetpassword.html',context)
    return render(request,'accounts/forgotpassword.html')

def reset_password(request):
    if request.method == 'POST':
        otp=request.POST['otp']
        email=request.POST['email']
        password=request.POST['password']
        repeatpassword=request.POST['repeatpassword']
        user=Account.objects.get(email=email)
        if password == repeatpassword:
            if User_otp.objects.filter(user=user, otp=otp).exists():
                user.set_password(password)
                user.save()
                mail_subject='Welcome Ekart, Success'
                message='Hi '+user.first_name+user.last_name+' welcome to eshop. Your Resetpassword Is successful, now you can login, Please ignore this message, if it is not you!'
                to_email=user.email
                send_mail=EmailMessage(mail_subject,message,to=[to_email])
                send_mail.send()
                messages.success(request,'Password reset success, Please login')
                return redirect('login_user')
        else:
            messages.warning(request,'Password mismatch')
            return redirect('reset_password')

    return render(request,'accounts/resetpassword.html')

@login_required(login_url='login_user')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders_count=orders.count()
    try:
        userprofile=UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        userprofile=UserProfile(user_id=request.user.id)
        userprofile.save()
    context={
        'orders_count':orders_count,
        'userprofile':userprofile,
    }
    return render(request,'accounts/dashboard.html',context)
@login_required(login_url='login_user')
def my_orders(request):
    orders=Order.objects.filter(user=request.user.id,is_ordered=True).order_by('-created_at')
    return render(request,'accounts/my_orders.html',{'orders':orders})

@login_required(login_url='login_user')
def edit_profile(request):
    userprofile=get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form=UserForm(request.POST, instance=request.user)
        profile_form=UserProfileForm(request.POST, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile has been updated')
            return redirect('edit_profile')
    else:
        user_form=UserForm(instance=request.user)
        profile_form=UserProfileForm(instance=userprofile)
        context={
            'user_form':user_form,
            'profile_form':profile_form,
            'userprofile':userprofile,
        }
    return render(request,'accounts/edit_profile.html',context)

@login_required(login_url='login_user')
def change_password(request):
    if request.method == 'POST':
        current_password=request.POST['currentpassword']
        new_password=request.POST['newpassword']
        confirm_password=request.POST['confirmpassword']
        user=Account.objects.get(username__exact=request.user.username)

        if new_password==confirm_password:
            success=user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                mail_subject='Welcome Ekart,  Success'
                message='Hi '+user.first_name+user.last_name+' welcome to eshop. Your Changing password Is successful, now you can login, Please ignore this message, if it is not you!'
                to_email=user.email
                send_mail=EmailMessage(mail_subject,message,to=[to_email])
                send_mail.send()
                messages.success(request,'Password Updated Successfully')
                return redirect('login_user')
            else:
                messages.warning(request,'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.warning(request,'Password does not match')
            return redirect('change_password')
    return render(request,'accounts/change_password.html')

@login_required(login_url='login_user')
def order_detail(request,order_id):
     order_detail=OrderProduct.objects.filter(order__order_number=order_id)
     order=Order.objects.get(order_number=order_id)
     subtotal=0
     for i in order_detail:
         subtotal += i.product_price * i.quantity
     context={
         'order_detail':order_detail,
         'order':order,
         'subtotal':subtotal
     }
     return render(request,'accounts/order_detail.html',context)

def session_id_gen(request):
    sessionid=request.session.session_key
    if not sessionid:
        carting=request.session.create()
    return sessionid

def user_feedback(request):
    try:
        if request.method == 'POST':
            data=request.POST['user_feedback']
            if request.user.is_authenticated:
                user_data=UserFeedback(user=request.user,session_id=session_id_gen(request),user_feedback=data)
                user_data.save()
                user=request.user
                mail_subject='Welcome Ekart, Feedback'
                message='From '+user.first_name+user.last_name+' Feedback : '+data+', Please ignore this message, if it is not you!'
                to_email='xxxxxxxxxxxxx'
                send_mail=EmailMessage(mail_subject,message,to=[to_email])
                send_mail.send()
            else:
                user_data=UserFeedback(session_id=session_id_gen(request),user_feedback=data)
                user_data.save()
                mail_subject='Welcome Ekart, Feedback'
                message='From Gust User Feedback : '+data+', Please ignore this message, if it is not you!'
                to_email='xxxxxxxxxxxx'
                send_mail=EmailMessage(mail_subject,message,to=[to_email])
                send_mail.send()
    except:
        pass
    url=request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(url)
