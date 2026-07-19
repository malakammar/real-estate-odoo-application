import json
import io
import xlsxwriter

from ast import literal_eval

from odoo import http
from odoo.http import request


class TestApi(http.Controller):

    # =====================================
    # Common Response
    # =====================================

    def response(self, success, message, data=None, status=200):
        return request.make_json_response(
            {
                'success': success,
                'message': message,
                'data': data
            },
            status=status
        )

    # =====================================
    # Create Property
    # =====================================

    @http.route(
        '/v1/test',
        methods=['POST'],
        auth='none',
        type='http',
        csrf=False
    )
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

            cr = request.env.cr

            query = """
                INSERT INTO property
                (name, post_code)
                VALUES
                ('property_malakooz2', '201')
                RETURNING id, name, post_code
            """

            cr.execute(query)

            res = cr.fetchone()

            if res:

                return self.response(
                    success=True,
                    message='Property created successfully',
                    data={
                        'id': res[0]
                    },
                    status=200
                )

        except Exception as error:

            return self.response(
                success=False,
                message=str(error),
                status=400
            )

    # =====================================
    # Get Properties
    # =====================================

    @http.route(
        '/v1/properties',
        methods=['GET'],
        auth='none',
        type='http',
        csrf=False
    )
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

    # =====================================
    # Get One Property
    # =====================================

    @http.route(
        '/v1/property/<int:property_id>',
        methods=['GET'],
        auth='none',
        type='http',
        csrf=False
    )
    def get_property(self, property_id):

        try:

            property_record = request.env[
                'property'
            ].sudo().browse(property_id)

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

    # =====================================
    # Update Property
    # =====================================

    @http.route(
        '/v1/property/<int:property_id>',
        methods=['PUT'],
        auth='none',
        type='http',
        csrf=False
    )
    def update_property(self, property_id):

        args = request.httprequest.data.decode()
        vals = json.loads(args)

        try:

            property_record = request.env[
                'property'
            ].sudo().browse(property_id)

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

    # =====================================
    # Delete Property
    # =====================================

    @http.route(
        '/v1/property/<int:property_id>',
        methods=['DELETE'],
        auth='none',
        type='http',
        csrf=False
    )
    def delete_property(self, property_id):

        try:

            property_record = request.env[
                'property'
            ].sudo().browse(property_id)

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


# =====================================
# Excel Report Controller
# =====================================

class PropertyExcelReport(http.Controller):

    @http.route(
        '/property/excel/report/<string:property_ids>',
        type='http',
        auth='user'
    )
    def property_excel_report(self, property_ids):

        property_ids = literal_eval(property_ids)

        properties = request.env[
            'property'
        ].sudo().browse(property_ids)

        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(
            output,
            {'in_memory': True}
        )

        worksheet = workbook.add_worksheet(
            'Properties'
        )

        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#D9EAD3',
            'border': 1,
            'align': 'center'
        })

        data_format = workbook.add_format({
            'border': 1
        })

        price_format = workbook.add_format({
            'border': 1,
            'num_format': '#,##0.00'
        })

        headers = [
            'ID',
            'Name',
            'Post Code',
            'Selling Price',
            'Garden'
        ]

        for col_num, header in enumerate(headers):

            worksheet.write(
                0,
                col_num,
                header,
                header_format
            )

        row_no = 1

        for property_rec in properties:

            worksheet.write(
                row_no,
                0,
                property_rec.id,
                data_format
            )

            worksheet.write(
                row_no,
                1,
                property_rec.name or '',
                data_format
            )

            worksheet.write(
                row_no,
                2,
                property_rec.post_code or '',
                data_format
            )

            worksheet.write(
                row_no,
                3,
                property_rec.selling_price or 0,
                price_format
            )

            worksheet.write(
                row_no,
                4,
                'Yes' if property_rec.garden else 'No',
                data_format
            )

            row_no += 1

        workbook.close()

        output.seek(0)

        file_name = 'Property_Report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                (
                    'Content-Type',
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                ),
                (
                    'Content-Disposition',
                    f'attachment; filename={file_name}'
                )
            ]
        )