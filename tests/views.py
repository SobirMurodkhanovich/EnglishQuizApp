from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Test, Question
from .serializers import TestSerializer
import random


class LevelTestView(APIView):

    def get(self, request, level):
        # Fetch the test for the given level
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


class EvaluateTestView(APIView):

    def post(self, request):
        submitted_answers = request.data.get('answers', {})
        test_level = request.data.get('level')

        # Get the test and its questions
        try:
            test = Test.objects.get(level=test_level)
        except Test.DoesNotExist:
            return Response({"error": "Test not found for this level."}, status=status.HTTP_404_NOT_FOUND)

        questions = test.questions.all()
        correct_count = 0

        # Check submitted answers
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
