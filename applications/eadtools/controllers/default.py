# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


def is_professor():
    return db((db.auth_membership.user_id == auth.user.id)
              & (db.auth_membership.group_id == db.auth_group.id)).select(db.auth_group.role).first().role == 'Professor'

@auth.requires_login()
def nova_disciplina():
    form = None
    if is_professor():
        form = SQLFORM(Disciplina)
        if form.process().accepted:
            session.flash = 'Formulário aceito!'
        elif form.errors:
            response.flash = 'Erros no formulário!'
        else:
            response.flash = 'Preencha o formulário!'
    else:
        sem_permissao = 'Você não tem permissão para criar uma disciplina!'
        response.flash = sem_permissao
    return dict(form=form)


@auth.requires_login()
def novo_planodeentrega():
    form = None
    if is_professor():
        filtro = db(auth.user.id == Disciplina.created_by)
        PlanoDeEntrega.disciplina.requires = IS_IN_DB(
            filtro, 'disciplina.id', '%(nome)s')
        form = SQLFORM(PlanoDeEntrega)
        if form.process().accepted:
            session.flash = 'Formulário aceito!'
        elif form.errors:
            response.flash = 'Erros no formulário!'
        else:
            response.flash = 'Preencha o formulário!'
    else:
        sem_permissao = 'Você não tem permissão para criar uma disciplina!'
        response.flash = sem_permissao
    return dict(form=form)


@auth.requires_login()
def nova_entrega():
    filtro = db((auth.user.id == Disciplina.created_by) &
                (PlanoDeEntrega.disciplina == Disciplina.id))
    Entrega.planodeentrega.requires = IS_IN_DB(
        filtro, 'disciplina.id', '%(nome)s')
    form = SQLFORM(Entrega)
    if form.process().accepted:
        session.flash = 'Formulário aceito!'
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Preencha o formulário!'
    return dict(form=form)


@auth.requires_login()
def planosdeentrega():
    nome_disciplina = db(Disciplina.id == request.args(0)).select().first().nome
    grid = SQLFORM.grid(PlanoDeEntrega.disciplina == request.args(0),
                        fields=[PlanoDeEntrega.id, PlanoDeEntrega.tipo, PlanoDeEntrega.descricao,
                                PlanoDeEntrega.datainicial, PlanoDeEntrega.datafinal],
                        user_signature=False, csv=False, details=False, maxtextlength=40, deletable=False, editable=False, create=False)
    return dict(nome_disciplina=nome_disciplina, grid=grid)


@auth.requires_login()
def disciplinas():
    grid = SQLFORM.grid(db(Disciplina.created_by == Usuario.id),
                        fields=[Disciplina.id,
                                Usuario.first_name, Disciplina.nome],
                        links=[lambda row: A('Entregas', _href=URL(
                            'planosdeentrega', args=[row.disciplina.id]))],
                        csv=False, details=False, maxtextlength=40, deletable=False, editable=False, create=False)
    return dict(grid=grid)
