from drf_spectacular.extensions import OpenApiAuthenticationExtension

from trainers.authentication import TrainerTokenAuthentication


class TrainerTokenScheme(OpenApiAuthenticationExtension):
    target_class = TrainerTokenAuthentication
    name = 'Bearer'

    def get_security_definition(self, auto_schema):
        return {'type': 'http', 'scheme': 'bearer'}
