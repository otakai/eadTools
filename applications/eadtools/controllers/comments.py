@auth.requires_login()
def post():
	form = SQLFORM(db.comment_post).process()
	comments = db(db.comment_post).select()
	return dict(form = form, comments = comments)