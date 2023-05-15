from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import Signer


def home(request):
    """
    Выполняет рендеринг шаблона 'home.html', используя предоставленный запрос.

    :param request: (HttpRequest): Объект запроса, отправленный пользователем.
    :return: HttpResponse (HttpResponse): Объект HTTP-ответа с отрисованным шаблоном.
    """
    return render(request, "sessions/home.html")


def set_cookie(request):
    """
    Устанавливает cookie с именем 'my_cookie' и значением 'my_value' в объект
    ответа созданном при рендеринге шаблона 'sessions/set_cookie.html'.

    param request: (HttpRequest): Объект, содержащий детали текущего запроса.
    return: HttpResponse (HttpResponse): HTTP-ответ, содержащий отрисованный
    шаблон 'sessions/set_cookie.html'и файл cookie с именем 'my_cookie' и
    значением 'my_value'.
    """
    response = render(request, "sessions/set_cookie.html")
    response.set_cookie("my_cookie", "my_value")

    response.set_cookie('count', )
    return response


def get_cookie(request):
    """
    Извлекает значение cookie с именем 'my_cookie' из объекта запроса и выводит
    его в виде сообщения об успехе используя фреймворк сообщений Django.
    Если cookie не найден, вместо него выводится сообщение об ошибке.
    Наконец, функция перенаправляет пользователя на 'домашнюю' страницу.

    :param request: Объект HTTP-запроса.
    :return: Ответ перенаправления на 'домашнюю' страницу.
    """
    my_cookie = request.COOKIES.get("my_cookie", None)
    if my_cookie is not None:
        messages.success(request, f"Cookie value: {my_cookie}")
    else:
        messages.error(request, "Cookie not found")
    return redirect("home")


def delete_cookie(request):
    """
    Удаляет cookie с именем 'my_cookie' из объекта запроса.
    """
    response = redirect("home")
    response.delete_cookie("my_cookie")
    return response


def set_session(request):
    """
    Устанавливает значение "my_key" в сессии на "my_value" и перенаправляет на
    главную страницу.

    :param request: Объект запроса.
    :return: Перенаправление на главную страницу.
    """
    request.session["my_key"] = "my_value"

    messages.success(request, "Session value set")
    return redirect("home")


def get_session(request):
    """
    Извлекает значение из сессии с ключом "my_key".
    Если значение не равно None, сообщение об успехе добавляется к сообщениям
    запроса вместе со значением сессии.
    В противном случае к сообщениям запроса добавляется сообщение об ошибке
    сообщения с текстом "Значение сессии не найдено".
    Наконец, функция возвращает перенаправление на "домашний" URL.

    :param request: Объект запроса, содержащий сессию.
    :return: Перенаправление на "домашний" URL.
    """
    my_value = request.session.get("my_key", None)
    if my_value is not None:
        messages.success(request, f"Session value: {my_value}")
    else:
        messages.error(request, "Session value not found")
    return redirect("home")


def delete_session(request):
    """
    Удаляет сессию с ключом "my_key".
    """
    request.session.pop("my_key", None)
    messages.success(request, "Session value deleted")
    return redirect("home")


def sign_data(request):
    """
    Подписывает данные с помощью объекта Django Signer и отправляет
    пользователю сообщение об успехе.

    param request: request (HttpRequest): Объект запроса, переданный в
    функцию представления.
    return: HttpResponseRedirect: Перенаправление на главную страницу.
    """
    my_data = {"foo": "bar"}
    signer = Signer()
    # Если необходимо подписать list, tuple, dict
    signed_data = signer.sign_object(my_data) 
    messages.success(request, f"Signed data: {signed_data}")
    return redirect("home")


def verify_data(request):
    """
    Проверка данных путем отмены подписи подписанных данных с помощью класса
    Signer. Если подпись действительна, выводится выводится сообщение об
    успехе.
    В противном случае выводится сообщение об ошибке.
    Перенаправляет на домашнюю страницу.

    param request: объект HttpRequest, представляющий текущий запрос.
    return: Объект HttpResponseRedirect, перенаправляющий на домашнюю страницу.
    """

    signed_data = "eyJmb28iOiJiYXIifQ:2msWcv4c-keQ1yWaJul-mArRJY4AcjfMLvKGSYv78Dk"
    signer = Signer()
    try:
        my_data = signer.unsign_object(signed_data)
        messages.success(request, f"Unsigned data: {my_data}")
    except signer.BadSignature:
        messages.error(request, "Invalid signature")
    return redirect("home")


class ClassBasedSessionsView(View):
    success_message = "Data signed successfully!"

    def get(self, request):
        # Получаем значение из Cookie
        my_cookie = request.COOKIES.get("my_cookie")

        if my_cookie is not None:
            # Если Cookie существует,  получаем значение и пытаемся проверить
            # подпись
            try:
                my_data = Signer().unsign(my_cookie)
                messages.success(request, f"Unsigned data: {my_data}")
                messages.add_message(request, messages.SUCCESS, self.success_message)
            except Signer.BadSignature:
                messages.error(request, "Invalid signature")
                redirect("home")
            # Рендерим шаблон и передаем значение Cookie в контекст
            context = {
                "my_cookie_value": my_data,
                "my_cookie": my_cookie,
            }
            return render(request, "sessions/for_class_template.html", context=context)
        else:
            # Если Cookie не существует, устанавливаем новое значение и перенаправляем на GET-запрос
            response = redirect("home")
            messages.error(request, "Cookie not found")
            return response


class ClassBasedSignView(View):
    def get(self, request):
        # Получаем значение из Cookie
        my_cookie = request.COOKIES.get("my_cookie")
        if my_cookie is not None:
            signed_data = Signer().sign("my_cookie_value")
            # Если Cookie существует, декодируем его значение
            response = redirect("home")
            response.set_cookie("my_cookie", signed_data)
            messages.success(request, f"Signed data: {signed_data}")
            return response
        else:
            # Создаём собственный message
            CRITICAL = 50
            messages.add_message(
                request, CRITICAL, "Something wrong... Cookie not found "
            )
            messages.error(request, "Cookie not found")
            return redirect("home")
