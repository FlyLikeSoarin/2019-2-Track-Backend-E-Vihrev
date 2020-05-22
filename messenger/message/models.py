from django.db import models


class Message(models.Model):
    chat = models.ForeignKey('chat.Chat', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    text = models.TextField(null=False)
    created = models.TimeField(auto_now_add=True)
    last_modified = models.TimeField(auto_now=True)

    def get_last_message(chat_id):
        pass

# class DialogMessage(models.Model):
#     dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def get_last_message(chat_id):
#         pass
