from django.http import HttpResponse
from .models import SignList, States, TransitionManager , Action, workevents, workflowitems , Flowmodel
from .serializer import TransitionManagerserializer , Actionseriaizer, Workitemserializer, workeventslistserializer, workflowitemslistserializer
from .middleware import get_current_user
from rest_framework.generics import ListAPIView , ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .exception import ModelNotFound, SignaturesNotMatching, TransitionNotAllowed
from django.db.models import Q
from rest_framework.exceptions import APIException
from django.conf import settings
from collections import deque

####################################################
#############       CORE     #######################
####################################################


## slice the interim state in wf_itemds







class FinFlotransition:


    def __init__(self, returns , next_value):
        self.returns = returns
        self.next_value = next_value
        super().__init__(returns , next_value)

    @property
    def returns_name(self):
        return self.returns.__name__


    def gets_default_return_action():
        qs = Action.objects.get(id = 1)
        return qs.description

    

    def gets_wf_item(gets_model):
        ws = workflowitems.objects.get(transitionmanager=gets_model.id)
        return ws

    # initiate a special function for reverse transition

    def return_transition():
        return None 

    # interim action for the transition handling
    def intermediator_transition_handler(self, type, action, t_id):
        try:
            gets_model = TransitionManager.objects.get(type=type.upper() , t_id = t_id)
            gets_flows = Flowmodel.objects.get(description  = type.lower())
            gets_action = Action.objects.get(description=action,model = gets_flows.id)
            gets_wf  = FinFlotransition.gets_wf_item(gets_model)
            sign_lists = []
            sub_action = []
            for item in SignList.objects.all():
                sign_lists.append(item.name)
                sub_action.append(item.sub_name)
                if item.name == gets_action.stage_required.name:
                    break
        except:
            raise ModelNotFound()

        
        # in-transition for return action  - can be customizable
        if action == FinFlotransition.gets_default_return_action().lower():


            wf = workflowitems.objects.update_or_create( transitionmanager=gets_model or gets_model.id, defaults= {"initial_state" : gets_wf.initial_state, "interim_state" : gets_action.to_state.description ,
                "final_state" : gets_action.to_state.description, "action" : action, "subaction" : FinFlotransition.FinFlotransition.sign_list[1 + gets_model.sub_sign], "model_type" : type.upper(), "event_user" : get_current_user() , "current_from_party" : gets_action.from_party , "current_to_party" : gets_action.to_party})
            workevents.objects.create(workflowitems=wf, event_user=get_current_user(),  initial_state=gets_wf.initial_state,final_value = True , 
                    interim_state = gets_action.to_state.description, final_state=gets_action.to_state.description, action=action, subaction=FinFlotransition.sub_action[0], type=type.upper(), from_party = gets_action.from_party , to_party = gets_action.to_party)
                        


        # len action and sub_sign
        
        elif gets_model.sub_sign <= gets_action.sign_required:
            def Transition_Handler():
                    gets_sign = gets_action.sign_required
                    
                    
                    if len(FinFlotransition.sign_lists)-1 != gets_model.sub_sign:
                        ws = workflowitems.objects.update_or_create( transitionmanager=gets_model or gets_model.id, defaults= {"initial_state" : gets_action.from_state.description, "interim_state" :  FinFlotransition.sign_lists[1 + gets_model.sub_sign], 
                            "final_state" : gets_action.to_state.description, "action" : action, "subaction" : FinFlotransition.sign_list[1 + gets_model.sub_sign], "model_type" : type.upper(), "event_user" : get_current_user() , "current_from_party" : gets_action.from_party , "current_to_party" : gets_action.to_party})
                        we = workevents.objects.create(workflowitems=gets_wf, event_user=get_current_user(),  initial_state=gets_action.from_state.description,
                                                  interim_state = FinFlotransition.sign_lists[1 + gets_model.sub_sign], final_state=gets_action.to_state.description, action=action, subaction=FinFlotransition.sub_action[0], type=type.upper(), from_party = gets_action.from_party , to_party = gets_action.to_party)
                        gets_model.sub_sign += 1
                        gets_model.save()

                    elif len(FinFlotransition.sign_lists)-1 == int(gets_model.sub_sign):
                        ws = workflowitems.objects.update_or_create( transitionmanager=gets_model or gets_model.id, defaults= {"initial_state" : gets_action.from_state.description, "interim_state" : gets_action.to_state.description ,
                            "final_state" : gets_action.to_state.description, "action" : action, "subaction" : FinFlotransition.sign_list[1 + gets_model.sub_sign], "model_type" : type.upper(), "event_user" : get_current_user() , "current_from_party" : gets_action.from_party , "current_to_party" : gets_action.to_party})
                        workevents.objects.create(workflowitems=gets_wf, event_user=get_current_user(),  initial_state=gets_action.from_state.description,final_value = True , 
                                                  interim_state = gets_action.to_state.description, final_state=gets_action.to_state.description, action=action, subaction=FinFlotransition.sub_action[0], type=type.upper(), from_party = gets_action.from_party , to_party = gets_action.to_party)
                        gets_model.sub_sign = 0
                        gets_model.save()
            return Transition_Handler()   
            
        else:
            raise TransitionNotAllowed()
        

    
    # core transition handler 
    def transition(self, type, action, t_id):
        try:
            gets_model = TransitionManager.objects.get(type=type.upper() , t_id = t_id)
            gets_flows = Flowmodel.objects.get(description  = type.lower())
            gets_action = Action.objects.get(description=action,model = gets_flows.id)
            gets_wf  = FinFlotransition.gets_wf_item(gets_model)
            sign_lists = []
            sub_action = []
            for item in SignList.objects.all():
                sign_lists.append(item.name)
                sub_action.append(item.sub_name)
                if item.name == gets_action.stage_required.name:
                    break
        except:
            raise ModelNotFound()


        # in-transition for return action  - can be customizable
        if action == FinFlotransition.gets_default_return_action().lower():


            wf = workflowitems.objects.update_or_create( transitionmanager=gets_model or gets_model.id, defaults= {"initial_state" : gets_wf.initial_state, "interim_state" : gets_action.to_state.description ,
                "final_state" : gets_action.to_state.description, "action" : action, "subaction" : FinFlotransition.sign_list[1 + gets_model.sub_sign], "model_type" : type.upper(), "event_user" : get_current_user() , "current_from_party" : gets_action.from_party , "current_to_party" : gets_action.to_party})
            workevents.objects.create(workflowitems=wf, event_user=get_current_user(),  initial_state=gets_wf.initial_state,final_value = True , 
                    interim_state = gets_action.to_state.description, final_state=gets_action.to_state.description, action=action, subaction=FinFlotransition.sub_action[0], type=type.upper(), from_party = gets_action.from_party , to_party = gets_action.to_party)
                        


        # len action and sub_sign
        
        elif gets_model.sub_sign <= gets_action.sign_required:
            def Transition_Handler():
                    gets_sign = gets_action.sign_required
                    
                    
                    if len(FinFlotransition.sign_lists)-1 != gets_model.sub_sign:
                        ws = workflowitems.objects.update_or_create( transitionmanager=gets_model or gets_model.id, defaults= {"initial_state" : gets_action.from_state.description, "interim_state" :  FinFlotransition.sign_lists[1 + gets_model.sub_sign], 
                            "final_state" : gets_action.to_state.description, "action" : action, "subaction" : FinFlotransition.sign_list[1 + gets_model.sub_sign], "model_type" : type.upper(), "event_user" : get_current_user() , "current_from_party" : gets_action.from_party , "current_to_party" : gets_action.to_party})
                        we = workevents.objects.create(workflowitems=gets_wf, event_user=get_current_user(),  initial_state=gets_action.from_state.description,
                                                  interim_state = FinFlotransition.sign_lists[1 + gets_model.sub_sign], final_state=gets_action.to_state.description, action=action, subaction=FinFlotransition.sub_action[0], type=type.upper(), from_party = gets_action.from_party , to_party = gets_action.to_party)
                        gets_model.sub_sign += 1
                        gets_model.save()

                    elif len(FinFlotransition.sign_lists)-1 == int(gets_model.sub_sign):
                        ws = workflowitems.objects.update_or_create( transitionmanager=gets_model or gets_model.id, defaults= {"initial_state" : gets_action.from_state.description, "interim_state" : gets_action.to_state.description ,
                            "final_state" : gets_action.to_state.description, "action" : action, "subaction" : FinFlotransition.sign_list[1 + gets_model.sub_sign], "model_type" : type.upper(), "event_user" : get_current_user() , "current_from_party" : gets_action.from_party , "current_to_party" : gets_action.to_party})
                        workevents.objects.create(workflowitems=gets_wf, event_user=get_current_user(),  initial_state=gets_action.from_state.description,final_value = True , 
                                                  interim_state = gets_action.to_state.description, final_state=gets_action.to_state.description, action=action, subaction=FinFlotransition.sub_action[0], type=type.upper(), from_party = gets_action.from_party , to_party = gets_action.to_party)
                        gets_model.sub_sign = 0
                        gets_model.save()
            return Transition_Handler()   
            
        else:
            raise TransitionNotAllowed()






####################################################
################      API       ####################
####################################################



#  ALL WORK_MODEL TRANSITION LIST 


class DetailsListApiView(ListAPIView):
    queryset = TransitionManager.objects.all()
    serializer_class = TransitionManagerserializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        type = self.request.query_params.get('type',None)
        t_id = self.request.query_params.get('t_id',None)
        if t_id and type is not None :
            queryset = TransitionManager.objects.filter(type__icontains = type , t_id = int(t_id))
        elif type is not None and t_id is None:
            queryset = TransitionManager.objects.filter(type__icontains = type)
        else:
            queryset = TransitionManager.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = TransitionManagerserializer(queryset, many=True)
        return Response({"status": "success", "type" : settings.FINFLO['WORK_MODEL'] , "data": serializer.data}, status=status.HTTP_200_OK)



# WORFLOW API 

class WorkFlowitemsListApi(ListAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = workflowitems.objects.all()
        serializer = Workitemserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)




# WORKEVENTS API 


class WorkEventsListApi(ListAPIView):
    queryset = workevents.objects.all()
    serializer_class = workeventslistserializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = workevents.objects.all()
        serializer = workeventslistserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)



# ACTION CREATE AND LIST API 


class ActionListApi(ListCreateAPIView):
    queryset = Action.objects.all()
    serializer_class = Actionseriaizer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Action.objects.all()
        serializer = Actionseriaizer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = Actionseriaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors},status=status.HTTP_204_NO_CONTENT)





