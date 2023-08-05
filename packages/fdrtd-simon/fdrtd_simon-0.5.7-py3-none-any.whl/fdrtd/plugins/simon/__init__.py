from fdrtd.plugins.simon.microservice import MicroserviceSimon


def fdrtd_register(registry):

    registry.register(
        {
            "namespace": "fdrtd",
            "protocol": "Simon",
            "version": "0.5.6"
        },
        MicroserviceSimon()
    )
