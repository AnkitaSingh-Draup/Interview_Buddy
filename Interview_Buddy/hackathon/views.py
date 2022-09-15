from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import *
import json
from .ml_utils.transcript_utils import *
from .ml_utils.model_utils import *
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


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_candidate_interview_details(request):
    response = {'status': 'success', 'result': {}, 'errors': []}
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            candidate_id = data.get('candidate_id')
            job_id = data.get('job_id')
            interview_data = Interview.objects.filter(candidate_id=candidate_id, job_id=job_id)
            if interview_data:
                for row in interview_data:
                    level = row.level.name
                    question_rating = QuestionLevelRating.objects.filter(interview_id=row.id)
                    if question_rating:
                        for question_row in question_rating:
                            response['result'][level] = {'question': question_row.question.question,
                                                         'score': question_row.rating.values}

    except Exception as e:
        response['errors'] = e
        response['status'] = 'fail'
    return Response(response)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_transcript_questions(request):
    response = {'status': 'success', 'result': {}, 'errors': []}
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            transcript_text = data.get('transcript_text')
            interviewer_name = data.get('interviewer_name')
            questions_list, interviewer_text, candidate_text = process_transcript(transcript_text, interviewer_name)
            grammar_rating = get_grammar_rating(candidate_text)
            interviewer_sentiment_score = sentiment_scores(interviewer_text)
            candidate_sentiment_score = sentiment_scores(candidate_text)
            response['result'] = {'questions_list': questions_list,
                                  'grammar_rating': grammar_rating,
                                  'interviewer_sentiment_score': interviewer_sentiment_score,
                                  'candidate_sentiment_score': candidate_sentiment_score}

    except Exception as e:
        response['errors'] = e
        response['status'] = 'fail'
    return Response(response)


@api_view(['POST'])
@permission_classes((AllowAny,))
def save_questions(request):
    response = {'status': 'success', 'result': {}, 'errors': []}
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            candidate_id = data.get('candidate_id')
            job_id = data.get('job_id')
            level_id = data.get('level_id')
            email = data.get('email')
            transcript_text = data.get('transcript_text')
            grammar_rating = data.get('grammar_rating')
            interviewer_sentiment = data.get('interviewer_sentiment')
            candidate_sentiment = data.get('candidate_sentiment')

            transcript_obj = Transcript.objects.create(vtt_file=transcript_text)
            transcript_obj.save()

            interviewer_obj = Interviewer.objects.filter(email=email).first()
            interview_obj = Interview.objects.create(
                candidate_id=candidate_id, job_id=job_id, level_id=level_id, interviewer=interviewer_obj,
                grammar_rating=grammar_rating, interviewer_sentiment=interviewer_sentiment, transcript=transcript_obj,
                candidate_sentiment=candidate_sentiment
            )
            interview_obj.save()

            questions_list = data.get('questions_list')
            for question_score in questions_list:
                question = question_score.get('question')
                score = question_score.get('score')
                obj = Question.objects.create(question=question)
                obj.save()
                rating_obj = Rating.objects.create(values=score)
                rating_obj.save()
                question_level_rating = QuestionLevelRating.objects.create(
                    question=obj, rating=rating_obj, interview=interview_obj)
                question_level_rating.save()

    except Exception as e:
        response['errors'] = e
        response['status'] = 'fail'
    return Response(response)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_roadmap_data(request):
    response = {'status': 'success', 'result': {}, 'errors': []}
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            job = data.get('job_id')
            level = data.get('level')
            data = RoadMap.objects.filter(role__job_id=job, level__name=level).values()
            response['result'] = data
    except Exception as e:
        response['errors'] = e
        response['status'] = 'fail'
    return Response(response)

