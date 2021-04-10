from webargs import fields, validate

login_args = {
    "email": fields.Email(required=True),
    "password": fields.Str(required=True)

}

register_args = {
    "name": fields.Str(required=True),
    "email": fields.Str(required=True),
    "password": fields.Str(required=True),
    "phone_num": fields.Str(required=True),
    "admin": fields.Bool(required=False, default=False),
    "manager": fields.Bool(required=False, default=False)
}
