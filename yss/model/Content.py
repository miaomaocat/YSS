from yss.model.BaseModel import *
from flask import g, request
import sqlite3

class Content(BaseModel):

    # select contentName, description, publish, author, length
    def __init__(self):
        self.downloadCount = 0;
        self.relatedContentList = ""


    def setFromRequest(self):
        # [request.form['fileName'], request.form['description'], request.form['publish'], request.form['author'], request.form['length']
        form = request.form
        if form.has_key('fileName'):
            self.name = request.form['fileName']

        if form.has_key('description'):
            self.desc = request.form['description']

        if form.has_key('publish'):
            self.publish = request.form['publish']

        if form.has_key('author'):
            self.author = request.form['author']

        if form.has_key('length'):
            self.length = request.form['length']

        # todo add this two feild
        self.downloadCount = 0;
        self.relatedContentList = ""

    def __setFromArray(self, array):
        self.contentId = array[0]
        self.name = array[1]
        self.desc = array[2]
        self.publish = array[3]
        self.author = array[4]
        self.length = array[5]
        # todo add this two feild
        self.downloadCount = 0;
        self.relatedContentList = ""

    def __repr__(self):
        return "--- <Content('%s', '%s', '%s')>" % (self.name, self.desc, self.publish)

    def save (self):
        print "saved content"
        g.db.execute('insert into contents (contentName, description, publish, author, length, downloadCount, relatedContentList) values (?, ?, ?, ?, ?, ?, ?)',
                       [self.name, self.desc, self.publish, self.author, self.length, self.downloadCount, self.relatedContentList])
        g.db.commit()

    @staticmethod
    def contentWithId(contentId):
        query = 'select id, contentName, description, publish, author, length from contents where id = \'' + contentId + '\' order by id desc'
        print query
        cur = g.db.execute(query)
        contents = list()
        for row in cur.fetchall():
            content = Content()
            content.__setFromArray(row)
            contents.append(content)

        if contents.count > 0:
            return contents[0]
        else:
            return nil;

    @staticmethod
    def readFromDatabase():
        query = 'select id, contentName, description, publish, author, length from contents order by id desc'
        cur = g.db.execute('select id, contentName, description, publish, author, length from contents order by id desc')
        contents = list()
        for row in cur.fetchall():
            content = Content()
            content.__setFromArray(row)
            contents.append(content)
        return contents;