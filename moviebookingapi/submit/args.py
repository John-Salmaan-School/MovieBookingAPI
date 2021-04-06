from webargs import fields

submit_args = {
    "name": fields.Str(required=True),
    "show": fields.Str(required=True),
    "date": fields.Str(required=True),
    "adult_tickets": fields.Str(required=True),
    "child_tickets": fields.Str(required=False),
    "discount": fields.Str(required=True),
    "cost": fields.Str(required=True)
}
