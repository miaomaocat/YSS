# -*- coding: utf-8 -*-

from yss.model.BaseModel import *

class Chapter(BaseModel):

    def __init__(self):
        self.chapterStatus = 0

    def __setFromArray(self, row):
        self.chapterId = row[0]
        self.chapterName = row[1]
        self.chapterStatus = row[2]
        self.contentId = row[3]
        self.chapterFileName = row[4]

    def setFromRequest(self):
        print request.form
        self.contentId = request.form['contentId']
        self.chapterName = request.form['chapterName']
        self.chapterStatus = request.form['chapterStatus']

    def __repr__(self):
        return "--- <chapter('%s')>" % (self.chapterName)

    @staticmethod
    def chaptersWithContentId(contentId):
        query = 'select id, chapterName, chapterStatus, ContentId, chapterFileName from chapters where contentId = ' + contentId + ' order by id desc'
        cur = g.db.execute(query)
        chapters = list()
        for row in cur.fetchall():
            chapter = Chapter()
            chapter.__setFromArray(row)
            chapters.append(chapter)
        return chapters

    @staticmethod
    def chapterWithId(chapterId):
        query = 'select id, chapterName, chapterStatus, ContentId, chapterFileName from chapters where id = \'' + chapterId + '\' order by id desc'
        print query
        cur = g.db.execute(query)
        chapters = list()
        for row in cur.fetchall():
            chapter = Chapter()
            chapter.__setFromArray(row)
            chapters.append(chapter)

        if chapters.count > 0:
            return chapters[0]
        else:
            return nil;

    def save (self):
        print "saved chapter"
        if hasattr(self, 'chapterId'):
            g.db.execute('update chapters set chapterName = ?, chapterStatus = ?, chapterFileName = ? where id = ?',
                       [self.chapterName, self.chapterStatus, self.chapterFileName, self.chapterId])
        else:
            g.db.execute('insert into chapters (ContentId, chapterName, chapterStatus) values (?, ?, ?)',
                       [self.contentId, self.chapterName, self.chapterStatus])
        g.db.commit()
