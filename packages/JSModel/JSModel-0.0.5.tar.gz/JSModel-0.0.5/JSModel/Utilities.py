class Utilities:
    @staticmethod
    def attract_value(input_data, v):

        if isinstance(v, list):
            for index, element in enumerate(v):
                if index == 0:
                    data = input_data[element]
                else:
                    data = data[element]
            return data
        elif isinstance(v, str):
            return input_data[v]

        else:
            ## pass for now
            pass
