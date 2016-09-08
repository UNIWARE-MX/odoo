# -*- coding: utf-8 -*-
import json
import logging
import werkzeug.utils

from odoo import http, service
from odoo.http import request

_logger = logging.getLogger(__name__)


class PosController(http.Controller):

    @http.route('/pos/web', type='http', auth='user')
    def pos_web(self, debug=False, **k):
        # if user not logged in, log him in
        pos_sessions = request.env['pos.session'].search([('state', '=', 'opened'), ('user_id', '=', request.session.uid)])
        if not pos_sessions:
            return werkzeug.utils.redirect('/web#action=point_of_sale.action_client_pos_menu')
        pos_sessions.login()

        version_info = service.common.exp_version()
        db_info = {
            'server_version': version_info.get('server_version'),
            'server_version_info': version_info.get('server_version_info'),
        }

        return request.render('point_of_sale.index', qcontext={'db_info': json.dumps(db_info)})
