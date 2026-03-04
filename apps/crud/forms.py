from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    username = StringField(
        "사용자명",
        validators=[
            DataRequired(message="사용자명은 필수입니다"),
            Length(max=30, message="30자 이내로 입력해주세요"),
        ],
    )
    email = StringField(
        "e-mail",
        validators=[
            DataRequired(message="e-mail 입력은 필수입니다"),
            Email(message="형식에 맞게 입력해주세요."),
        ],
    )
    password = PasswordField(
        "비밀번호",
        validators=[
            DataRequired(message="비밀번호 입력은 필수입니다."),
        ],
    )

    submit = SubmitField("신규 등록")

    