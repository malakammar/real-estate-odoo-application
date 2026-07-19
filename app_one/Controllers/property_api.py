import json
from odoo import http
from odoo.http import request


class TestApi(http.Controller):

    # Function for handling the response structure

    def response(self, success, message, data=None, status=200):
        return request.make_json_response(
            {
                'success': success,
                'message': message,
                'data': data
            },
            status=status
        )

    @http.route('/v1/test', methods=['POST'], auth="none", type='http', csrf=False)
    def post_property(self):

        args = request.httprequest.data.decode()
        vals = json.loads(args)

        if not vals.get('name'):

            return self.response(
                success=False,
                message='Name is required',
                status=400
            )

        try:

            #res = request.env['property'].sudo().create(vals)
            # we use cursur(cr) to contact with postgre using orm
            cr = request.env.cr
            query ="""insert into property  (name,post_code) values ('property_malakooz2', '201') returning id, name, post_code """
            cr.execute(query)
            res = cr.fetchone()
            if res:

                return self.response(
                    success=True,
                    message='Property created successfully',
                    data={
                        'id': res.id
                    },
                    status=200
                )

        except Exception as error:

            return self.response(
                success=False,
                message=str(error),
                status=400
            )

    #Get all properties with pagination
    @http.route('/v1/properties',
                methods=['GET'],
                auth='none',
                type='http',
                csrf=False)
    def get_properties(self):

        try:

            page = int(
                request.httprequest.args.get('page', 1)
            )

            limit = int(
                request.httprequest.args.get('limit', 10)
            )

            offset = (page - 1) * limit

            properties = request.env['property'].sudo().search(
                [],
                limit=limit,
                offset=offset
            )

            total_records = request.env['property'].sudo().search_count([])

            data = []

            for rec in properties:
                data.append({
                    'id': rec.id,
                    'name': rec.name,
                    'description': rec.description
                })

            return self.response(
                success=True,
                message='Properties fetched successfully',
                data={
                    'page': page,
                    'limit': limit,
                    'total_records': total_records,
                    'properties': data
                },
                status=200
            )

        except Exception as error:

            return self.response(
                success=False,
                message=str(error),
                status=400
            )

    @http.route('/v1/property/<int:property_id>',
                methods=['GET'],
                auth='none',
                type='http',
                csrf=False)
    def get_property(self, property_id):

        try:

            property_record = request.env['property'].sudo().browse(property_id)

            if not property_record.exists():

                return self.response(
                    success=False,
                    message='Property not found',
                    status=404
                )

            data = {
                'id': property_record.id,
                'name': property_record.name,
                'description': property_record.description
            }

            return self.response(
                success=True,
                message='Property fetched successfully',
                data=data,
                status=200
            )

        except Exception as error:

            return self.response(
                success=False,
                message=str(error),
                status=400
            )

    @http.route('/v1/property/<int:property_id>',
                methods=['PUT'],
                auth='none',
                type='http',
                csrf=False)
    def update_property(self, property_id):

        args = request.httprequest.data.decode()
        vals = json.loads(args)

        try:

            property_record = request.env['property'].sudo().browse(property_id)

            if not property_record.exists():

                return self.response(
                    success=False,
                    message='Property not found',
                    status=404
                )

            property_record.write(vals)

            return self.response(
                success=True,
                message='Property updated successfully',
                status=200
            )

        except Exception as error:

            return self.response(
                success=False,
                message=str(error),
                status=400
            )

    @http.route('/v1/property/<int:property_id>',
                methods=['DELETE'],
                auth='none',
                type='http',
                csrf=False)
    def delete_property(self, property_id):

        try:

            property_record = request.env['property'].sudo().browse(property_id)

            if not property_record.exists():

                return self.response(
                    success=False,
                    message='Property not found',
                    status=404
                )

            property_record.unlink()

            return self.response(
                success=True,
                message='Property deleted successfully',
                status=200
            )

        except Exception as error:

            return self.response(
                success=False,
                message=str(error),
                status=400
            )

    def action_print_excel(self):
            return {
                'type': 'ir.actions.act_url',
                'url': f'/property/excel/report/{self.env.context.get("active_ids")}',
                'target': 'new',
            }