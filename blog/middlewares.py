from django.contrib import messages
from django.http import Http404, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from .models import Post

class BlogMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        print('process request')
        if request.GET and 'p' in request.GET.keys() :
            return HttpResponse('This is blog posts')
        return None
    
    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     print('process view')
    #     if 'posts/1/' in request.path:
    #         return HttpResponse('This is posts')
    #     return None
    
    # def process_exception(self, request, exception):
    #     print('process exception')

    #     print(exception.__class__.__name__)
    #     # print(exception.message)
    #     if exception:
    #         return HttpResponse(f'Exeption is: {exception.__class__.__name__} {exception}') 
    #     return None
    

    def process_template_response(self, request, response):
        print('process template response')
        req_page_counter_coockie = request.COOKIES.get("page_counter", None)

        if req_page_counter_coockie:
            page_counter = int(request.COOKIES.get("page_counter", None))
        else:
            page_counter = 0
        
        response.set_cookie("page_counter", page_counter+1)

        messages.success(request=request, message=f'Счётчик страниц: {page_counter}')
        response.context_data['mid_posts_claass'] = Post.objects.all()
        return response

class FirstMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("FirstMiddleware before")
        response = self.get_response(request)
        print("FirstMiddleware after")
        return response

class SecondMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("SecondMiddleware before")
        response = self.get_response(request)
        print("SecondMiddleware after")
        return response

# Это обрабработчик контента
def mid_posts(request):
    return {'mid_posts': Post.objects.all()}