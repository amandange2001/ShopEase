from django.shortcuts import render

def index(req):
    return render(req, "index.html")

def userlogout(req):
    logout(req)
    return redirect("/")


def loginuser(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        context = {}
        if uname == "" or upass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "loginuser.html", context)
        else:
            username = uname
            userdata = authenticate(username=uname, password=upass)
            context = {"username": username}
            if userdata is not None:
                login(req, userdata)
                return redirect("/")
                # return render(req, "index.html", context)
            else:
                context["errmsg"] = "Invalid username and password"
                return render(req, "loginuser.html", context)
    else:
        return render(req, "loginuser.html")


def registeruser(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}
        if uname == "" or upass == "" or ucpass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "registeruser.html", context)
        elif upass != ucpass:
            context["errmsg"] = "Password and Confirm Password doesn't match"
            return render(req, "registeruser.html", context)
        else:
            try:
                userdata = User.objects.create(username=uname, password=upass)
                userdata.set_password(upass)
                userdata.save()
                return redirect("/")
            except Exception:
                context["errmsg"] = "User Already Exists"
                return render(req, "registeruser.html", context)
    else:
        return render(req, "registeruser.html")


def aboutus(req):
    if req.user.is_authenticated:
        user = req.user
        context = {"username": user}
        return render(req, "aboutus.html", context)
    else:
        return render(req, "aboutus.html")


def contactus(req):
    if req.user.is_authenticated:
        user = req.user
        context = {"username": user}
        return render(req, "contactus.html", context)
    else:
        return render(req, "contactus.html")