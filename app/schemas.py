from marshmallow import Schema, fields, validate

class ReviewSchema(Schema):
    product_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str(required=True, validate=validate.Length(min=1, max=500))