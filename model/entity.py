# Papers_with_code
class PageCard:
    def __init__(self, id, title, content, star, pdf_url, github_url, date, create_time):
        self.id = id
        self.title = title
        self.content = content
        self.star = star
        self.pdf_url = pdf_url
        self.github_url = github_url
        self.date = date
        self.create_time = create_time

    def string_title(self):
        print(self.date + ': ' + self.title)

    # list-dict to list-entity
    def db_json_list_to_entity(paras_list):
        data_lsit = []
        for data in paras_list:
            data_lsit.append(PageCard(data['id'], data['title'], data['content'], data['star'],
                                      data['pdf_url'], data['github_url'], data['date'], data['create_time']))
        return data_lsit

    def __str__(self) -> str:
        return super().__str__()
