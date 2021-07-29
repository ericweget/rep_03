###############
class HrqDataFromFile:

    def __init__(self,json, full_name):

        with open(full_name, 'r') as f:
            self.hrq_data_from_file = json.load(f)

    def getAll(self):

        return self.hrq_data_from_file

    def getNextQuestionCode(self, question_code):

        return self.hrq_data_from_file[question_code]['next_one']  
