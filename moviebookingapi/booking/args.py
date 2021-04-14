from webargs import fields

submit_args = {
    "show": fields.Str(required=True),
    "date": fields.Str(required=True),
    "adult_tickets": fields.Str(required=True),
    "child_tickets": fields.Str(required=True),
    "discount": fields.Str(required=True),
    "cost": fields.Str(required=True)
}
remove_args = {
    "id": fields.Str(required=True)
}

update_args = {
    "id": fields.Str(required=True),
    "show": fields.Str(required=True),
    "date": fields.Str(required=True),
    "adult_tickets": fields.Str(required=True),
    "child_tickets": fields.Str(required=True),
    "discount": fields.Str(required=True),
    "cost": fields.Str(required=True)
}
