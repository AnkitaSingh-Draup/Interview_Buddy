from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import *
import json
from .ml_utils.transcript_utils import *
from .ml_utils.model_utils import *
# Create your views here.

import json

job_role_data = json.load(open('hackathon/ml_utils/model/job_role.json', 'r+'))


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_candidate_details(request):
    response = {'status': 'success', 'result': [], 'errors': []}
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            data_list = JobCandidateMapping.objects.filter(job__job_id=data.get('job_id'))
            for data in data_list:
                candidate_core_skills = data.candidate.core_skills
                candidate_soft_skills = data.candidate.soft_skills
                past_title_candidate = data.candidate.past_title
                past_role_candidate = data.candidate.past_role

                job_core_skills = data.job.core_skills
                past_title_job = data.job.title
                past_role_job = data.job.role
                job_soft_skills = data.job.soft_skills

                core_skill_match = len(set(job_core_skills).intersection(set(candidate_core_skills))) / len(
                    set(job_core_skills).union(set(candidate_core_skills)))
                soft_skill_match = len(set(job_soft_skills).intersection(set(candidate_soft_skills))) / len(
                    set(job_soft_skills).union(set(candidate_soft_skills)))

                global job_role_data
                if not job_role_data:
                    job_role_data = json.load(open('hackathon/ml_utils/model/job_role.json', 'r+'))
                if past_title_candidate == past_title_job:
                    role_match = 1.0
                if past_role_candidate == past_role_job:
                    role_match = 0.8
                elif job_role_data[past_role_candidate]['job_family'] == job_role_data[past_role_job]['job_family']:
                    role_match = 0.5
                elif job_role_data[past_role_candidate]['job_occupation'] == job_role_data[past_role_job]['job_occupation']:
                    role_match = 0.3
                else:
                    role_match = 0.0
                sim_weightage = {'core': 0.4,
                                 'soft': 0.1,
                                 'role': 0.5}
                final_match_score = core_skill_match * sim_weightage['core'] + soft_skill_match * sim_weightage[
                    'soft'] + soft_skill_match * sim_weightage['role']

                common_skills = set(job_core_skills).intersection(set(candidate_core_skills))

                candidate_id = data.candidate.id
                candidate = list(Candidate.objects.filter(id=candidate_id).values())
                response['result'].append(
                    {'candidate': candidate, 'final_match_score': final_match_score})

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
                            if response['result'].get(level):
                                response['result'][level].append({'question': question_row.question.question,
                                                                  'score': question_row.rating.id})
                            else:
                                response['result'][level] = [{'question': question_row.question.question,
                                                              'score': question_row.rating.id}]

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
            obj = Transcript.objects.filter(id=1).first()
            interviewer_name = data.get('interviewer_name')
            questions_list, interviewer_text, candidate_text = process_transcript(obj.vtt_file, interviewer_name)
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

            transcript_obj = Transcript.objects.get_or_create(vtt_file=transcript_text)[0]

            interviewer_obj = Interviewer.objects.filter(email=email).first()
            interview_obj = Interview.objects.get_or_create(
                candidate_id=candidate_id, job_id=job_id, level_id=level_id, interviewer=interviewer_obj,
                grammar_rating=grammar_rating, interviewer_sentiment=interviewer_sentiment, transcript=transcript_obj,
                candidate_sentiment=candidate_sentiment
            )[0]

            questions_list = data.get('questions_list')
            for question_score in questions_list:
                question = question_score.get('question')
                score = question_score.get('score')
                obj = Question.objects.get_or_create(question=question)[0]
                rating_obj = Rating.objects.get_or_create(values=score)[0]
                question_level_rating = QuestionLevelRating.objects.get_or_create(
                    question=obj, rating=rating_obj, interview=interview_obj)

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


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_suggestion(request):
    response = {'status': 'success', 'result': {}, 'errors': []}
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            keyword = data.get('keyword')
            data = search_suggestions(keyword)
            response['result'] = data
    except Exception as e:
        response['errors'] = e
        response['status'] = 'fail'
    return Response(response)


