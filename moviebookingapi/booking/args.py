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
remove_args = {
    "id": fields.Str(required=True)
}

update_args = {
    "id": fields.Str(required=True),
    "name": fields.Str(required=False
                       ),
    "show": fields.Str(required=False),
    "date": fields.Str(required=False),
    "adult_tickets": fields.Str(required=False),
    "child_tickets": fields.Str(required=False),
    "discount": fields.Str(required=False),
    "cost": fields.Str(required=False)
}