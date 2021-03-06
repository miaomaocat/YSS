# -*- coding: utf-8 -*-

from yss.model.BaseModel import *
from yss.model.Chapter import *

class Content(BaseModel):

    # select contentName, description, publish, author, length
    def __init__(self):
        self.downloadCount = 0;
        self.relatedContentList = ""
        self.type = BaseModel.content_type_book


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

        if form.has_key('type'):
            self.type = request.form['type']

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
        self.relatedContentList = array[6]
        self.type = array[7]
        # todo add this feild
        self.downloadCount = 0;

    def __repr__(self):
        return "----- <Content('%s', '%s', '%s', '%s')>" % (self.name, self.desc, self.publish, self.relatedContentList)

    def save (self):
        print "saved content"
        if hasattr(self, 'contentId'):
            g.db.execute('update contents set contentName = ?, description = ?, publish = ?, author = ?, length = ?, downloadCount = ?, relatedContentList= ?, contentType = ? where id = ?',
                       [self.name, self.desc, self.publish, self.author, self.length, self.downloadCount, self.relatedContentList, self.contentId, self.type])
        else:
            g.db.execute('insert into contents (contentName, description, publish, author, length, downloadCount, relatedContentList, contentType) values (?, ?, ?, ?, ?, ?, ?, ?)',
                       [self.name, self.desc, self.publish, self.author, self.length, self.downloadCount, self.relatedContentList, self.type])
        g.db.commit()

    def delete(self):
        sql = 'delete from contents where id = %d;' % self.contentId
        g.db.execute(sql)
        g.db.commit()


    def jsondict(self):
        _dict = obj2dict(self);
        _chapters = Chapter.chaptersWithContentId(str(self.contentId))

        chapters = []
        for chapter in _chapters:
            chapters.append(chapter.jsondict())

        if len(chapters) > 0:
            _dict['chapters'] = chapters

        return _dict


    @staticmethod
    def contentWithId(contentId):
        query = 'select id, contentName, description, publish, author, length, relatedContentList, contentType from contents where id = \'' + contentId + '\' order by id desc'
        print query
        cur = g.db.execute(query)
        contents = list()
        for row in cur.fetchall():
            content = Content()
            content.__setFromArray(row)
            contents.append(content)

        if len(contents) > 0:
            return contents[0]
        else:
            return None;

    @staticmethod
    def readFromDatabaseWithType(contentType):
        query = 'select id, contentName, description, publish, author, length, relatedContentList, contentType from contents where contentType = \'' + str(contentType) + '\' order by id desc'
        print query
        cur = g.db.execute(query)
        contents = list()
        for row in cur.fetchall():
            content = Content()
            content.__setFromArray(row)
            contents.append(content)
        return contents;

    @staticmethod
    def readFromDatabase():
        query = 'select id, contentName, description, publish, author, length, relatedContentList, contentType  from contents order by id desc'
        cur = g.db.execute(query)
        contents = list()
        for row in cur.fetchall():
            content = Content()
            content.__setFromArray(row)
            contents.append(content)
        return contents;
