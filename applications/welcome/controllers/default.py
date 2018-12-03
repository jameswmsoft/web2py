# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    return dict(email=T(""), password=T(""))

def register():
    return dict(form=T(""))

@auth.requires_login(URL('index'))
def home():
    return dict()

def do_register():
    username = request.post_vars['username']
    firstname = request.post_vars['firstname']
    lastname = request.post_vars['lastname']
    email = request.post_vars['email']
    password = request.post_vars['password']

    db.auth_user.insert(
        username = username,
        first_name=firstname,
        last_name=lastname,
        email=email,
        # password=db.auth_user.password.requires[0](password)[0]
        password= hash(password)
    )
    redirect(URL('index'))

def do_login():
    username = request.post_vars['username']
    password = request.post_vars['password']

    passp = str(hash(password))
    if auth.login_bare(username, passp):
        redirect(URL('home'))
    else:
        response.view = 'default/index.html'
        return dict(email=T(""),password=T(""))

def logout():
    auth.logout()
    redirect(URL('index'))
# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[welcome]/default/user/login
    http://..../[welcome]/default/user/logout
    http://..../[welcome]/default/user/register
    http://..../[welcome]/default/user/profile
    http://..../[welcome]/default/user/retrieve_password
    http://..../[welcome]/default/user/change_password
    http://..../[welcome]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[welcome]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[welcome]/default/download/[filename]
    """
    return response.download(request, db)
