from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import *
import json
# Create your views here.


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_candidate_details(request):
    response = {'status': 'success', 'result': {}, 'errors': []}
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            data_list = JobCandidateMapping.objects.filter(job__job_id=data.get('job_id')).values()
            for data in data_list:
                candidate_id = data.get('candidate_id')
                candidate = list(Candidate.objects.filter(id=candidate_id).values())
                response['result'] = candidate

    except Exception as e:
        response['errors'] = e
        response['status'] = 'fail'
    return Response(response)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_job_role(request):
    response = {'status': 'success', 'result': {}, 'errors': []}
    try:
        if request.method == 'GET':
            data = Job.objects.filter().values()
            response['result'] = data

    except Exception as e:
        response['errors'] = e
        response['status'] = 'fail'
    return Response(response)

