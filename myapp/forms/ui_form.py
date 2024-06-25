from dataclasses import field


class BootstrapForm(object):  # 用于继承bootstrap装饰
    Bootstrap_class_exclude = ["color", "is_public"]  # 排除一些字段不作bootstrap装饰

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.Bootstrap_class_exclude:
                continue
            old_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (
                "{} w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500".format(
                    old_class
                )
            )
            field.widget.attrs["placeholder"] = "请输入" + field.label
            field.widget.attrs["autocomplete"] = "off"


class CssForm(object):  # 用于继承css装饰
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            old_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = "{} form-control".format(old_class)
            field.widget.attrs["placeholder"] = "请输入" + field.label
