from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Users, Product

# --- LOGIN ---
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = Users.objects.get(username=username, password=password)
            request.session["username"] = user.username
            request.session["role"] = user.role
            return redirect("products")
        except Users.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


# --- LOGOUT ---
def logout_view(request):
    request.session.flush()
    return redirect("login")


# --- VIEW PRODUCTS ---
def product_list(request):
    if "username" not in request.session:
        return redirect("login")

    username = request.session["username"]
    role = request.session["role"]
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products, "username": username, "role": role})


def product_detail(request, id):
    if "username" not in request.session:
        return redirect("login")

    product = get_object_or_404(Product, id=id)
    return render(request, "product_detail.html", {"product": product, "username": request.session["username"], "role": request.session["role"]})


# --- ADMIN ONLY ACTIONS ---
def product_add(request):
    if request.session.get("role") != "admin":
        return HttpResponse("<h3>Access Denied</h3>")

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        desc = request.POST.get("description")
        image = request.POST.get("image")
        Product.objects.create(name=name, price=price, description=desc, image=image)
        return redirect("products")

    return render(request, "product_form.html", {"action": "Add"})


def product_edit(request, id):
    if request.session.get("role") != "admin":
        return HttpResponse("<h3>Access Denied</h3>")

    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.description = request.POST.get("description")
        product.image = request.POST.get("image")
        product.save()
        return redirect("products")

    return render(request, "product_form.html", {"action": "Edit", "product": product})


def product_delete(request, id):
    if request.session.get("role") != "admin":
        return HttpResponse("<h3>Access Denied</h3>")

    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect("products")
