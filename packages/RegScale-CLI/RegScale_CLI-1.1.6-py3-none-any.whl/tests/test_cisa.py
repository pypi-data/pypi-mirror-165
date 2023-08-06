#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from app.api import Api
from app.application import Application
from app.cisa import (
    alerts,
    regscale_threats,
    update_known_vulnerabilities,
    update_regscale,
)
from app.logz import create_logger


class Test_Cisa:
    logger = create_logger()
    app = Application()
    api = Api(app)

    def test_kev(self):

        data = update_known_vulnerabilities()
        assert data
        update_regscale(data)

    def test_updates(self):
        reg_threats = regscale_threats(self.api, self.app.config)
        assert reg_threats

    def test_alerts(self):
        alerts(2021)
        assert 1 == 1
