from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Test, Question
from .serializers import TestSerializer
import random
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class LevelTestView(APIView):

    def get(self, request, level):
        try:
            test = Test.objects.get(level=level)
        except Test.DoesNotExist:
            return Response({"error": "Test not found for this level."}, status=status.HTTP_404_NOT_FOUND)

        # Get 15 random questions from the test
        questions = test.questions.all()
        random_questions = random.sample(list(questions), 15)

        # Serialize and return the questions
        serializer = TestSerializer(test)
        return Response({"test_level": level, "questions": serializer.data['questions']})


class EvaluateLevelTestView(APIView):
    @swagger_auto_schema(
        operation_description="Evaluate answers for a given test level",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'answers': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Submitted answers for the test",
                    example={
                        "1": 2,
                        "2": 3,
                        "3": 1
                    }
                ),
            },
            required=['answers']
        ),
        responses={
            200: openapi.Response('Result', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'total_questions': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                      description='Total number of questions'),
                    'correct_answers': openapi.Schema(type=openapi.TYPE_INTEGER, description='Correct answers count'),
                    'score': openapi.Schema(type=openapi.TYPE_NUMBER, description='Score percentage')
                }
            )),
            400: 'Bad Request'
        }
    )
    def post(self, request, level):
        # Ensure this method is configured for POST
        submitted_answers = request.data.get('answers', {})
        try:
            test = Test.objects.get(level=level)
        except Test.DoesNotExist:
            return Response({"error": "Test not found for this level."}, status=status.HTTP_404_NOT_FOUND)

        questions = test.questions.all()
        correct_count = 0

        # Validate the submitted answers
        for question in questions:
            question_id = str(question.id)
            if question_id in submitted_answers:
                if submitted_answers[question_id] == question.correct_option:
                    correct_count += 1

        return Response({
            "total_questions": len(questions),
            "correct_answers": correct_count,
            "score": (correct_count / 15) * 100
        })
