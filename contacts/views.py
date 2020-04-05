from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Contact

def contact(request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        user_id = request.POST['user_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        realtor_email = request.POST['realtor_email']

        contact = Contact(listing_id=listing_id,listing=listing, email=email, user_id=user_id, name=name,
                         phone=phone, message=message)

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)

            if has_contacted:
                messages.error(request, "You have already made an enquiry about this listing")
                return redirect('/listings/'+ listing_id)

        contact.save()

        send_mail(
            "Property Listing Inquiry",
            "Theres is an enquiry for listing "+listing+".Sign in to admin panel for more info.",
            "officialsherpa@gmail.com",
            [realtor_email, "officialsherp@gmail.com"],
            fail_silently=False
        )

        messages.success(request, "Your enquiry has been sent successfully!")

        return redirect('/listings/' + listing_id)
