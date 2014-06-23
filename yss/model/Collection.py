from yss.model.BaseModel import *
from yss.model.Content import *

class Collection(BaseModel):
    queryString = 'select id, collectionName, collectionType, collectionImageUrl, contentList, collectionImageUrl2 from collections'
    queryStringWithId = 'select id, collectionName, collectionType, collectionImageUrl, contentList, collectionImageUrl2 from collections where id = \'%s\''
    updateString = 'update collections set collectionName = ?, collectionType = ?, collectionImageUrl = ?, contentList = ? , collectionImageUrl2 = ? where id = ?'
    insertString = 'insert into collections (collectionName, collectionType, collectionImageUrl, contentList, collectionImageUrl2) values (?, ?, ?, ?, ?)'

    def __init__(self):
        self.imageUrl = ''
        self.imageUrl2 = ''
        self.type = 0
        self.contentList =''
        pass

    def __setFromArray(self, row):
        self.collectionId = row[0]
        self.name = row[1]
        self.type = row[2]
        self.imageUrl = row[3]
        self.contentList = row[4]
        self.imageUrl2 = row[5]

    def setFromRequest(self):
        self.name = request.form['collectionName']
        self.imageUrl = request.form['imageUrl']
        self.imageUrl2 = request.form['imageUrl2']

    def __repr__(self):
        return "--- <collection ('%s')>" % (self.name)

    def save (self):
        if hasattr(self, 'collectionId'):
            g.db.execute(Collection.updateString,
                       [self.name, self.type, self.imageUrl, self.contentList, self.imageUrl2, self.collectionId])
        else:
            g.db.execute(Collection.insertString,
                       [self.name, self.type, self.imageUrl, self.contentList, self.imageUrl2])
        g.db.commit()

    def delete(self):
        sql = 'delete from collections where id = %d;' % self.collectionId
        g.db.execute(sql)
        g.db.commit()

    def jsondict(self):
        _dict = obj2dict(self);
        _dict.pop('contentList')

        contentList = self.contentList
        contentIds = contentList.split(',')
        contents = list()

        for id in contentIds:
            if id != u'':
                content = Content.contentWithId(id)
                if content != None:
                    contents.append(content.jsondict())

        if len(contents) > 0:
            _dict['contents'] = contents

        return _dict

    @staticmethod
    def collectionWithId(collectionId):
        query = Collection.queryStringWithId % collectionId
        print query
        cur = g.db.execute(query)
        collections = list()

        for row in cur.fetchall():
            collection = Collection()
            collection.__setFromArray(row)
            collections.append(collection)

        if len(collections) > 0:
            return collections[0]
        else:
            return None;

    @staticmethod
    def readFromDatabase():
        cur = g.db.execute(Collection.queryString)
        collections = list()

        for row in cur.fetchall():
            collection = Collection()
            collection.__setFromArray(row)
            collections.append(collection)

        return collections;
