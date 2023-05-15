from users.models import User


class UserAndGroupMiddleware:
    def __init__(self, get_response):
            self.get_response = get_response

    def __call__(self, request):
        # Получаем всех пользователей 
        users = User.objects.all()
        # Текущий пользователь
        current_user = request.user
        
        # Добавляем данные в атрибут request
        request.users = users
        print(request.users, current_user)
        response = self.get_response(request)
        
        return response
    
    def process_template_response(self, request, response):
        print('Users process template response')
        response.context_data['current_user'] = request.user
        return response