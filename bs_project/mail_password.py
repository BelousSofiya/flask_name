# from flask_mail import Mail
# import random
# import string
#
#
# # def send_email(app, msg):
# #     with app.app_context():
# #         mail.send(msg)
#
# # def send_email(user):
# #     token = user.get_reset_token()
# #     msg = Message()
# #     msg.subject = "Flask App Password Reset"
# #     msg.sender = os.getenv('MAIL_USERNAME')
# #     msg.recipients = [user.email]
# #     msg.html = render_template('reset_email.html',
# #                                 user=user,
# #                                 token=token)
# #     mail.send(msg)
#
# def password_generator(length):
#     characters = string.ascii_letters + string.digits + string.punctuation
#     return ''.join(random.choice(characters) for _ in range(length))
