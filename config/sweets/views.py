from rest_framework import viewsets, permissions
from .models import Sweet
from .serializers import SweetSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SweetForm

User = get_user_model()



class IsAdminOrReadCreateOnly(permissions.BasePermission):
    """
    Allow authenticated users to GET, POST, PUT, PATCH.
    Allow DELETE only for staff/admin users.
    """
    def has_permission(self, request, view):
        if request.method in ["GET", "POST", "PUT", "PATCH"]:
            return request.user and request.user.is_authenticated
        elif request.method == "DELETE":
            return request.user and request.user.is_staff
        return False


class SweetViewSet(viewsets.ModelViewSet):
    queryset = Sweet.objects.all()
    serializer_class = SweetSerializer
    permission_classes = [IsAdminOrReadCreateOnly]



from django.urls import reverse

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)

            return redirect("dashboard")  # URL NAME, not path
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "auth/login.html")



def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if username and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, "Account created. Please login.")
                return redirect("login")
        else:
            messages.error(request, "Username and password are required")
    return render(request, "auth/register.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    sweets = Sweet.objects.all()
    in_stock = sweets.filter(quantity__gt=0).count()
    out_of_stock = sweets.filter(quantity=0).count()
    categories = sweets.values_list('category', flat=True).distinct().count()
    
    paginator = Paginator(sweets, 12)
    page = request.GET.get('page', 1)
    
    try:
        sweets_page = paginator.page(page)
    except PageNotAnInteger:
        sweets_page = paginator.page(1)
    except EmptyPage:
        sweets_page = paginator.page(paginator.num_pages)
    
    return render(request, "sweets/dashboard.html", {
        "sweets": sweets_page,
        "total_sweets": sweets.count(),
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "categories_count": categories,
        "paginator": paginator,
    })


@login_required
def purchase_sweet(request, id):
    """Legacy purchase - redirects to add to cart"""
    from .cart_views import add_to_cart
    return add_to_cart(request, id)



def admin_check(user):
    return user.is_staff


def home(request):
    """Home page showing featured sweets"""
    featured_sweets = Sweet.objects.filter(quantity__gt=0)[:6]
    categories = sorted(set(Sweet.objects.values_list('category', flat=True)))
    return render(request, "sweets/home.html", {
        "featured_sweets": featured_sweets,
        "categories": categories
    })


def sweets_list(request):
    """List all sweets with filtering and pagination"""
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    
    sweets = Sweet.objects.all()
    
    if category_filter:
        sweets = sweets.filter(category__icontains=category_filter)
    
    if search_query:
        sweets = sweets.filter(name__icontains=search_query)
    
    categories = sorted(set(Sweet.objects.values_list('category', flat=True)))

    paginator = Paginator(sweets, 12)
    page = request.GET.get('page', 1)
    
    try:
        sweets_page = paginator.page(page)
    except PageNotAnInteger:
        sweets_page = paginator.page(1)
    except EmptyPage:
        sweets_page = paginator.page(paginator.num_pages)
    
    return render(request, "sweets/sweets_list.html", {
        "sweets": sweets_page,
        "categories": categories,
        "selected_category": category_filter,
        "search_query": search_query,
        "paginator": paginator,
    })


def sweet_detail(request, id):
    """Detail view for a single sweet"""
    sweet = get_object_or_404(Sweet, id=id)
    related_sweets = Sweet.objects.filter(category=sweet.category).exclude(id=sweet.id)[:4]
    return render(request, "sweets/sweet_detail.html", {
        "sweet": sweet,
        "related_sweets": related_sweets
    })


@login_required
@user_passes_test(admin_check)
def add_sweet(request):
    if request.method == "POST":
        form = SweetForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Sweet added successfully")
                return redirect("sweets_list")
            except Exception as e:
                messages.error(request, f"Error saving sweet: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SweetForm()
    return render(request, "sweets/sweet_form.html", {"form": form, "title": "Add Sweet"})


@login_required
@user_passes_test(admin_check)
def update_sweet(request, id):
    sweet = get_object_or_404(Sweet, id=id)
    if request.method == "POST":
        form = SweetForm(request.POST, request.FILES, instance=sweet)
        if form.is_valid():
            form.save()
            messages.success(request, "Sweet updated successfully")
            return redirect("sweet_detail", id=sweet.id)
    else:
        form = SweetForm(instance=sweet)
    return render(request, "sweets/sweet_form.html", {"form": form, "title": "Update Sweet", "sweet": sweet})


@login_required
@user_passes_test(admin_check)
def delete_sweet(request, id):
    sweet = get_object_or_404(Sweet, id=id)
    sweet.delete()
    messages.success(request, "Sweet deleted successfully")
    return redirect("sweets_list")
