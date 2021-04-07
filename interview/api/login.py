from rest_framework.response import Response
from InterviewBackend.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, VERIFY_SID
from rest_framework import status, generics
from rest_framework_jwt.settings import api_settings
from rest_framework import generics
from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="./account.log", level=logging.DEBUG)


class UserList(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserDetail(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer


class UserLogin(generics.CreateAPIView):
    serializer_class = AccountLoginSerializer

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone", None)
        if phone is None:
            return Response(
                {"error": "Введите номер телефона"}, status=status.HTTP_403_FORBIDDEN
            )
        try:
            user, created = Account.objects.get_or_create(phone=phone)
            if user.username is None:
                user.username = f"Guest_{Account.objects.count() + 1}"
                user.save()
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            verify = client.verify.services(VERIFY_SID)
            verify.verifications.create(to=phone, channel="sms")
            return Response(
                {"message": "Код авторизации был успешно отправлен"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserVerify(generics.CreateAPIView):
    serializer_class = AccountVerifySerializer

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone", None)
        code = request.data.get("code", None)
        if phone is None:
            return Response(
                {"error": "Введите номер телефона"}, status=status.HTTP_400_BAD_REQUEST
            )
        if code is None:
            return Response(
                {"error": "Введите код подтверждения"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            verify = client.verify.services(VERIFY_SID)
            verify_result = verify.verification_checks.create(to=phone, code=code)
            user = Account.objects.get(phone=phone)
            if verify_result.status != "approved":
                return Response(
                    {"message": "Неверный код авторизации"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response(
                {
                    "token": token,
                    "user": UserSerializer(user, context={"request": request}).data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
