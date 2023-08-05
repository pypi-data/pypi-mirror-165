class ContentDataValidator:
    @staticmethod
    def validate(data: dict, *args, **kwargs) -> bool:
        is_valid = True
        content_data = data.get("content_data")

        counter = 0
        if isinstance(content_data, list):
            for item in content_data:
                if item.get("error"):
                    error_codes = data.setdefault("error_code", [])
                    error_messages = data.setdefault("error_message", [])
                    error_codes.append(item["error"]["code"])
                    error_messages.append(item["error"]["message"])
                    counter += 1

            if counter == len(content_data):
                is_valid = False

        if content_data is None:
            is_valid = False
            data["error_code"] = 1
            data["error_message"] = "Content data is None"

        return is_valid
