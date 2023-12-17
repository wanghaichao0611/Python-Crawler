import datetime

SCROLL_JS = "window.scrollTo(0, document.body.scrollHeight)"

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
NOW_TIME = datetime.datetime.now().strftime(DATE_FORMAT)
MAIN_START = 'Start: ' + NOW_TIME
MAIN_END = 'End: ' + NOW_TIME

TRUNCATE_PAPERS_WINT_CODE_SQL = '''truncate table papers_with_code'''

BATCH_INSET_PAPERS_WINT_CODE_SQL = '''
    INSERT INTO papers_with_code
    (id, title, content, star, pdf_url, github_url, `date`, create_time)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
    '''

SELECT_PAPERS_WINT_CODE_SQL = '''select * from papers_with_code'''

ON_DUPLICATE_KEY_UPDATE_PAPERS = ''' 
     INSERT INTO papers_with_code
    (id, title, content, star, pdf_url, github_url, `date`, create_time)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE pdf_url=(pdf_url)
'''
