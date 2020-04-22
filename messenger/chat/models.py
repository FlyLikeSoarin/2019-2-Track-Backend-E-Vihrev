from django.db import models
from django.db.models import Q

#
# class Dialog(models.Model):
#     first_user = models.ForeignKey(User, models.CASCADE, related_name='first_user_in_dialog')
#     second_user = models.ForeignKey(User, models.CASCADE, related_name='second_user_in_dialog')
#
#     def create_dialog(first_user, second_user):
#         already_exist = Dialog.objects.filter(
#             (Q(first_user=first_user) & Q(second_user=second_user))
#             | (Q(first_user=second_user) & Q(second_user=first_user))
#         ).exists()
#         if (already_exist):
#             pass
#         else:
#             Dialog.objects.create(first_user=User.get_by_id(first_user), second_user=User.get_by_id(second_user))
#
#     def get_dialogs(id):
#         return Dialog.objects.filter(Q(first_user=id) | Q(second_user=id)).all()


class Chat(models.Model):
    creator = models.ForeignKey('user.User', models.CASCADE)
    chat_label = models.CharField(max_length=128, null=True)
    icon = models.CharField(max_length=100, null=True)

    def create_chat(self, creator, char_label, icon=None):
        if icon is None:
            new_chat = Chat.objects.create(creator=creator, chat_label=chat_label)
        else:
            new_chat = Chat.objects.create(creator=creator, chat_label=chat_label)

    def get_chats(id):
        chat_ids = [int(entry.chat.id) for entry in Member.objects.filter(user__exact=id).all()]
        return Chat.objects.filter(id__in=chat_ids).all()


class Member(models.Model):
    user = models.ForeignKey('user.User', models.CASCADE)
    chat = models.ForeignKey('chat.Chat', models.CASCADE)
    last_unseen = models.IntegerField(null=True)
