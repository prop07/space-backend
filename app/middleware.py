import datetime

server_start_time = datetime.datetime.now()

class ServerRuntimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def get_server_runtime():
        current_time = datetime.datetime.now()
        formatted_start_date = server_start_time.strftime("%Y/%m/%d %H:%M:%S")
        active_time =str(current_time - server_start_time)
        formatted_time = active_time.split(".")[0]
        return {
        "uptime": formatted_time,
        "timestamp": formatted_start_date,
    }