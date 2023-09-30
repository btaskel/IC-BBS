from wtforms import Form


class BaseForm(Form):
    @property
    def messages(self):
        message_list = []
        if self.errors:
            for errors in self.errors.values():
                # 将一个列表追加到另一个列表末尾
                message_list.extend(errors)
        return message_list
