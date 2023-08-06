from django import dispatch
from django.db.models.signals import post_save , pre_save , post_delete

from .middleware import get_current_user
from .models import States, TransitionManager, workevents, workflowitems , states
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
        states = States.objects.get(id = 1)
        wf = workflowitems.objects.create(transitionmanager = manager , event_user = get_current_user() , initial_state = states.description , final_state = states.description)
        we = workevents.objects.create(workflowitems = wf , event_user = get_current_user() , initial_state = states.description , final_state = states.description)
        wf.save()
        we.save()
        manager.save()

