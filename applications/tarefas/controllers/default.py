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

#### estes códigos vão no final abaixo da função call() e devem substituir os que foram feitos até agora.

## Cadastrar uma nova tarefa
@auth.requires_login()
def nova():
    form = SQLFORM(Tarefa)
    if form.process().accepted:
        session.flash = 'Formulário aceito!'
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Preencha o formulário!'
    return dict(form=form)

## Listar as tarefas do usuário cadastrado
@auth.requires_login()
def tarefas():
    user_id = auth.user.id
    tar = db(Tarefa.created_by == user_id).select()
    return dict(tar=tar)

## Ver os detalhes de uma tarefa especifica
@auth.requires_login()
def detalhar():
    tarefa = db(Tarefa.id == request.args(0)).select()
    return dict(tarefa=tarefa)

## Editar os detalhes de uma tarefa especifica
@auth.requires_login()
def editar():
    form = SQLFORM(Tarefa, request.args(0))
    if form.process().accepted:
        session.flash = 'Tarefa atualizada: %s' % form.vars.nome
        redirect(URL('tarefas'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

## Formulário de contato
def contato():
    form = SQLFORM.factory(
        Field('nome', requires=IS_NOT_EMPTY()),
        Field('email', requires=IS_EMAIL(), label='E-mail'),
        Field('mensagem', 'text', requires=IS_NOT_EMPTY()))
    if form.process().accepted:
        mail.send(
            to=['meu@email.com.br'],
            subject='Contato pelo site por %s' % form.vars.nome,
            reply_to = form.vars.email,
            message=form.vars.mensagem)
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)


