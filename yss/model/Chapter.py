from yss.model.BaseModel import *
from flask import g, request
import sqlite3

class Chapter(BaseModel):
    def __init__(self):
        self.chapterStatus = 0

    def __setFromArray(self, row):
        self.chapterId = row[0]
        self.chapterName = row[1]
        self.chapterStatue = row[2]

    def setFromRequest(self):
        print request.form
        self.contentId = request.form['contentId']
        self.chapterName = request.form['chapterName']
        self.chapterStatus = request.form['chapterStatus']

    def __repr__(self):
        return "--- <chapter('%s')>" % (self.chapterName)

    @staticmethod
    def chaptersWithContentId(contentId):
        query = 'select id, chapterName, chapterStatus from chapters where contentId = ' + contentId + ' order by id desc'
        cur = g.db.execute(query)
        chapters = list()
        for row in cur.fetchall():
            chapter = Chapter()
            chapter.__setFromArray(row)
            chapter.ContentId = contentId
            chapters.append(chapter)
        return chapters

    def save (self):
        print "saved chapter"
        g.db.execute('insert into chapters (ContentId, chapterName, chapterStatus) values (?, ?, ?)',
                       [self.contentId, self.chapterName, self.chapterStatus])
        g.db.commit()
