from django import dispatch
from django.db.models.signals import post_save , pre_save , post_delete

from .middleware import get_current_user
from .models import TransitionManager, workevents, workflowitems , Action
from django.conf import settings




# CUSTOM MULTIPLE RECEIVER SIGNALS 


def finflo_receiver(signal, senders ,  **kwargs):
    def decorator(receiver_func):
        for sender in senders:
            if isinstance(signal, (list, tuple)):
                for s in signal:
                    s.connect(receiver_func, sender=sender, **kwargs)
            else:
                signal.connect(receiver_func, sender=sender,**kwargs)

        return receiver_func

    return decorator

# 



# MAIN SIGNAL RECEIVER FOR TRANSITION HANDLING - 4/8/2022 by anand


a = [ite for ite in settings.FINFLO['WORK_MODEL']]
@finflo_receiver(post_save, senders = a)
def create(sender, instance, **kwargs):
        a = str(sender)
        remove_characters = ["class", "models.","'","<",">"," "]
        for i in remove_characters:
            a = a.replace(i,"")
        manager = TransitionManager.objects.create(
            type = a.lower() , t_id = instance.id
        )
        action = Action.objects.get(model__description = a.lower())
        wf = workflowitems.objects.create(transitionmanager = manager , event_user = get_current_user() , initial_state = action.from_state.description , final_state = action.to_state.description)
        we = workevents.objects.create(workflowitems = wf , event_user = get_current_user() , initial_state = action.from_state.description , final_state = action.to_state.description)
        wf.save()
        we.save()
        manager.save()

