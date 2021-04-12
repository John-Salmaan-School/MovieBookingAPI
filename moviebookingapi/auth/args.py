from webargs import fields

login_args = {
    "email": fields.Email(required=True),
    "password": fields.Str(required=True)

}

register_args = {
    "name": fields.Str(required=True),
    "email": fields.Email(required=True),
    "password": fields.Str(required=True),
    "phone_num": fields.Str(required=True),
    "admin": fields.Bool(missing=False),
    "manager": fields.Bool(missing=False)
}
