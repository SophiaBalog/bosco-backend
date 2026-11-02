import time


class RequestTimingMiddleware:
    """Пише в консоль: метод, шлях, користувача і час обробки;
    додає заголовок X-Response-Time."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        elapsed_ms = (time.perf_counter() - start) * 1000

        user = getattr(request, "user", None)
        username = user.username if user is not None and user.is_authenticated else "anonymous"

        print(f"[{request.method}] {request.path} user={username} {elapsed_ms:.1f} ms", flush=True)
        response["X-Response-Time"] = f"{elapsed_ms:.1f}ms"
        return response