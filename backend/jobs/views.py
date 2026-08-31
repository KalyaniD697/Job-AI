from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import JobSearchSerializer
from .services.job_search import JobSearchService
from .services.job_extractor import JobExtractor
from .services.job_analyzer import JobAnalyzer
from .services.contact_finder import ContactFinderService
from .services.email_generator import EmailGeneratorService


class HealthCheckView(APIView):

    def get(self, request):

        return Response(
            {
                "status": "success",
                "message": "Job AI backend is running"
            },
            status=status.HTTP_200_OK
        )


class JobSearchView(APIView):

    def post(self, request):

        serializer = JobSearchSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "status": "error",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        role = serializer.validated_data["role"]

        location = serializer.validated_data["location"]

        experience = serializer.validated_data.get(
            "experience",
            ""
        )

        try:

            # -----------------------------------------
            # 1. Search jobs
            # -----------------------------------------

            search_service = JobSearchService()

            jobs = search_service.search_jobs(
                role=role,
                location=location,
                experience=experience
            )


            # -----------------------------------------
            # 2. Analyze jobs
            # -----------------------------------------

            analyzer = JobAnalyzer()

            analyzed_jobs = []


            for job in jobs[:5]:

                try:

                    analyzed_job = analyzer.analyze_job(
                        job=job,
                        role=role,
                        location=location,
                        experience=experience
                    )


                    if not analyzed_job.get(
                        "is_relevant",
                        True
                    ):
                        continue


                    analyzed_job["job_url"] = job.get(
                        "url",
                        ""
                    )

                    analyzed_job["source"] = job.get(
                        "source",
                        ""
                    )


                    # ---------------------------------
                    # IMPORTANT:
                    # Do NOT find contacts here.
                    #
                    # Contact search is expensive.
                    # It will happen when the user
                    # clicks "Find Contact".
                    # ---------------------------------

                    analyzed_job["contact"] = None


                    analyzed_jobs.append(
                        analyzed_job
                    )


                except Exception as analysis_error:

                    analyzed_jobs.append(
                        {
                            **job,
                            "analysis_error": str(
                                analysis_error
                            )
                        }
                    )


            return Response(
                {
                    "status": "success",
                    "count": len(analyzed_jobs),
                    "jobs": analyzed_jobs
                },
                status=status.HTTP_200_OK
            )


        except Exception as e:

            return Response(
                {
                    "status": "error",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class JobExtractView(APIView):

    def post(self, request):

        url = request.data.get("url")


        if not url:

            return Response(
                {
                    "status": "error",
                    "message": "URL is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        try:

            extractor = JobExtractor()

            text = extractor.extract_page_text(
                url
            )


            return Response(
                {
                    "status": "success",
                    "url": url,
                    "text": text[:20000]
                },
                status=status.HTTP_200_OK
            )


        except Exception as e:

            return Response(
                {
                    "status": "error",
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerateEmailView(APIView):

    def post(self, request):

        job = request.data.get(
            "job"
        )

        candidate = request.data.get(
            "candidate"
        )


        if not job:

            return Response(
                {
                    "status": "error",
                    "message": "Job information is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        if not candidate:

            return Response(
                {
                    "status": "error",
                    "message": "Candidate information is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        try:

            generator = EmailGeneratorService()

            email = generator.generate_email(
                job=job,
                candidate=candidate
            )


            return Response(
                {
                    "status": "success",
                    "email": email
                },
                status=status.HTTP_200_OK
            )


        except Exception as error:

            return Response(
                {
                    "status": "error",
                    "message": str(error)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ContactFinderView(APIView):

    def post(self, request):

        company = request.data.get(
            "company"
        )

        job_title = request.data.get(
            "job_title",
            ""
        )

        location = request.data.get(
            "location",
            ""
        )


        if not company:

            return Response(
                {
                    "status": "error",
                    "message": "Company is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        try:

            service = ContactFinderService()


            contact = service.find_contacts(
                company=company,
                job_title=job_title,
                location=location
            )


            return Response(
                {
                    "status": "success",
                    "contact": contact
                },
                status=status.HTTP_200_OK
            )


        except Exception as exc:

            return Response(
                {
                    "status": "error",
                    "message": str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )