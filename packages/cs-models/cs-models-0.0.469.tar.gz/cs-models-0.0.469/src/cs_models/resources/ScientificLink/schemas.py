from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load,
)
from ...utils.utils import pre_load_date_fields


class ScientificLinkResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    doi = fields.String(required=True, validate=not_blank)
    pubmed_id = fields.Integer(allow_none=True)
    date = fields.DateTime(allow_none=True)
    title = fields.String(allow_none=True)
    type = fields.String(allow_none=True)
    abstract = fields.String(allow_none=True)
    journal_title = fields.String(allow_none=True)
    inbound_ref_count = fields.Integer(allow_none=True)
    outbound_ref_count = fields.Integer(allow_none=True)
    orig_file_url = fields.String(allow_none=True)
    best_oa_location = fields.String(allow_none=True)
    method = fields.String(allow_none=True)
    verification = fields.String(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)

    @pre_load
    def convert_string_to_datetime(self, in_data, **kwargs):
        date_fields = ['date']

        in_data = pre_load_date_fields(
            in_data,
            date_fields,
            date_format='%Y%m%dT%H%M%S',
        )
        return in_data
