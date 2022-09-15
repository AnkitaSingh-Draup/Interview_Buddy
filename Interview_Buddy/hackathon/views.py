from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Job
# Create your views here.


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_job_skill_role(request):
    response = {'status': 'success', 'result': {}, 'errors': []}
    try:
        if request.method == 'GET':
            data = Job.objects.filter().values()

            response['result'] = data
    except Exception as e:
        response['errors'] = e
        response['status'] = 'fail'
    return Response(response)
