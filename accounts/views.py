from django.shortcuts import render, redirect
from .forms import UserRegistrationForm


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # 1. Create the User object but don't save to DB yet
            new_user = form.save(commit=False)

            # 2. HASH THE PASSWORD (The missing link!)
            new_user.set_password(form.cleaned_data.get("password"))

            # 3. Now save the User to the database
            new_user.save()

            # 4. Update the Profile fields
            # Since your signal (likely) created the profile, we update it here
            profile = new_user.userprofile
            profile.phone_number = form.cleaned_data.get("phone_number")
            profile.location = form.cleaned_data.get("location")
            profile.save()

            return render(
                request, "accounts/register_done.html", {"new_user": new_user}
            )
    else:
        form = UserRegistrationForm()

    return render(request, "registration/register.html", {"form": form})

def login_success(request):
    """
    Redirects users based on their role after a successful login.
    """
    if request.user.is_superuser or request.user.is_staff:
        # Redirect YOU and the Client (Admins/Staff) to the Merchant Dashboard
        return redirect("orders:merchant_dashboard")
    else:
        # Redirect normal customers to the Shop Home
        return redirect("shop:product_list")
