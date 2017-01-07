db.define_table('comment_post',
   Field('body','text',label='Your comment'),
   auth.signature)