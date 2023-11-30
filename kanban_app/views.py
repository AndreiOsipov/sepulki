from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render, redirect 
from django.contrib.auth.views import LoginView
# from django.contrib.auth.models import User

class LoginRedirectView(LoginView):
    
    template_name = 'kanban_login/login.html'
    # form_class = LoginForm
    
    def get_redirect_url(self) -> str:
        user_id = self.request.user.id
        # db_user = User.objects.get(id=user_id)
        if hasattr(self.request.user, 'shmurdik'):
            self.next_page = reverse('shmurdik')
        elif hasattr(self.request.user, 'grymzik'):
            self.next_page = reverse('grymzik')
        elif hasattr(self.request.user, 'fufelnitsa'):
            self.next_page = reverse('fufelnitsa')
        
        # print(f"shmurdik? {hasattr(db_user, 'shmurdik')}")
        # print(f"grymzik? {hasattr(db_user, 'grymzik')}")
        # # print(f'url: {self.next_page} id: {user_id}')
        # print(db_user)
        # print(db_user.shmurdik)
        # print(db_user.grymzik)
        return super().get_redirect_url()

class ShmurdickView(View):
    template_name = 'kanban_app/shmurdik_kanban.html'

    def get(self, request):
        return render(request, self.template_name)

class GrymzickView(View):

    template_name = 'kanban_app/grymzick_kanban.html'
    def get(self, request):
        return render(request, self.template_name)
    
class FufelnitsaView(View):

    template_name = 'kanban_app/fufelnitsa_kanban.html'
    def get(self, request):
        return render(request, self.template_name)
    
# def index(request):
#     return render(request, "kanban_app/index.html")

# def room(request, room_name):
#     return render(request, "kanban_app/room.html", {"room_name": room_name})