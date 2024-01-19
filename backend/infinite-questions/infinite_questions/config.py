"""
Simple configuration file for infinite-Questions API
"""

WIKIPEDIA_API_PROJECT_NAME = 'Infinite'
WIKIPEDIA_LANGUAGE = 'he'
WIKIPEDIA_RANDOM_ARTICLE_URL = 'https://he.wikipedia.org/wiki/%D7%9E%D7%99%D7%95%D7%97%D7%93:%D7%90%D7%A7%D7%A8%D7%90%D7%99'
WIKIPEDIA_NEWS_AND_AFFAIRS_PAGE_NAME = 'תבנית:חדשות_ואקטואליה'

GPT_TRIVIA_PROMPT = 'הכן שאלת טריוויה ותשובה על בסיס תוכן הפסקה הבאה בלבד, ללא שאלות בנושא תאריכים. שלח בשורות נפרדות את השאלה והתשובה בפורמט הבא: שאלה: <הכנס שאלה>\nתשובה: <הכנס תשובה>'
GPT_MODEL = 'gpt-3.5-turbo'
