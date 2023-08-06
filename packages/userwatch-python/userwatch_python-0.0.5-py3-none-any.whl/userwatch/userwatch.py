import grpc

from userwatch import userwatch_shepherd_pb2
from userwatch import userwatch_shepherd_pb2_grpc


class Userwatch:
    shepherd = None
    privateApiKey = None

    def __init__(self, privateApiKey, options={}):
        url = options.get("url", "api.userwat.ch:443")
        self.privateApiKey = privateApiKey
        channel = None
        if options.get("insecure", False):
            channel = grpc.insecure_channel(url)
        else:
            channel = grpc.secure_channel(
                url,
                grpc.ssl_channel_credentials()
            )
        self.shepherd = userwatch_shepherd_pb2_grpc.ShepherdStub(channel)

    # Access the assessment of a user for whom an event was previously
    # registered with Userwatch via a track(UserInfo, EventType) call from
    # your client application.
    #
    # At this point you can also attach any additional UserInfo your server
    # has which your client might not have had available.
    def verify(self,
               eventToken,  # string
               userInfo,  # userwatch_public_pb2.UserInfo
               challengeVerification=None):  # optional userwatch_shepherd_pb2.ChallengeVerificationRequest
        def doit():
            return self.shepherd.Verify(
                userwatch_shepherd_pb2.VerifyRequest(
                    event_token=eventToken,
                    userinfo=userInfo,
                    challenge_verification=challengeVerification,
                ),
                metadata=[("x-api-key", self.privateApiKey)]
            )

        return self.__retryNonIllegalArg(doit)

    def createChallenge(self,
                        type,  # userwatch_public_pb2.ChallengeType
                        userInfo,  # userwatch_public_pb2.UserInfo
                        deviceId,  # string
                        origin=None  # Optional. Required for webauthn Should be consistent eg. login.company.com or similar
                        ):
        def doit():
            return self.shepherd.CreateChallenge(
                userwatch_shepherd_pb2.CreateChallengeRequest(
                    type=type,
                    userinfo=userInfo,
                    device_id=deviceId,
                    origin=origin
                ),
                metadata=[("x-api-key", self.privateApiKey)]
            )

        return self.__retryNonIllegalArg(doit)

    def verifyChallenge(
        self,
        type,  # userwatch_public_pb2.ChallengeType
        userInfo,  # userwatch_public_pb2.UserInfo
        deviceId,  # string
        challengeId,  # string
        secretResponse  # string, eg the sms code.
    ):
        def doit():
            return self.shepherd.VerifyChallenge(
                userwatch_shepherd_pb2.ChallengeVerificationRequest(
                    type=type,
                    userinfo=userInfo,
                    device_id=deviceId,
                    challenge_id=challengeId,
                    secret_response=secretResponse
                ),
                metadata=[("x-api-key", self.privateApiKey)]
            )

        return self.__retryNonIllegalArg(doit)

    # def reportDevice(self, userId, deviceId):
    #     return self.shepherd.reportDevice(
    #         userId=userId,
    #         deviceId=deviceId,
    #         global
    #     )

    # def approveDevice(self, userId, deviceId):
    #     return self.shepherd.approveDevice(
    #         userId=userId,
    #         deviceId=deviceId,
    #         global
    #     )

    def getDeviceList(self, userId):
        def doit():
            return self.shepherd.GetDeviceList(
                userwatch_shepherd_pb2.DeviceListRequest(user_id=userId),
                metadata=[("x-api-key", self.privateApiKey)]
            )

        return self.__retryNonIllegalArg(doit)

    # Run the function, retrying once on errors other than illegal argument.
    # Illegal argument errors, will never work a second time.
    # We primarily expect the retry to succeed when there is an intermittent
    # network error
    #
    # Consider asking customers to use the 'retry' library if they want more
    # nuanced logic. https://pypi.org/project/retry/
    # We should be cautious about what retry behaviour we apply globally.

    def __retryNonIllegalArg(self, fn):
        try:
            return fn()
        except grpc.RpcError as err:
            if err and err.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise err
            else:
                # Ideally we should report the error in the background using historian.
                return fn()
