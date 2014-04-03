from yss.model.BaseModel import *

class Collection(BaseModel):
    queryString = 'select id, collectionName, collectionType, collectionImageUrl, contentList from collections'
    queryStringWithId = 'select id, collectionName, collectionType, collectionImageUrl, contentList from collections where id = \'%s\''
    updateString = 'update collections set collectionName = ?, collectionType = ?, collectionImageUrl = ?, contentList = ? where id = ?'
    insertString = 'insert into collections (collectionName, collectionType, collectionImageUrl, contentList) values (?, ?, ?, ?)'

    def __init__(self):
        self.imageUrl = ''
        self.type = 0
        self.contentList =''
        pass

    def __setFromArray(self, row):
        self.collectionId = row[0]
        self.name = row[1]
        self.type = row[2]
        self.imageUrl = row[3]
        self.contentList = row[4]

    def setFromRequest(self):
        self.name = request.form['collectionName']
        self.imageUrl = request.form['imageUrl']

    def __repr__(self):
        return "--- <collection ('%s')>" % (self.name)

    def save (self):
        if hasattr(self, 'collectionId'):
            g.db.execute(Collection.updateString,
                       [self.name, self.type, self.imageUrl, self.contentList, self.collectionId])
        else:
            g.db.execute(Collection.insertString,
                       [self.name, self.type, self.imageUrl, self.contentList])
        g.db.commit()

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

        if collections.count > 0:
            return collections[0]
        else:
            return nil;

    @staticmethod
    def readFromDatabase():
        cur = g.db.execute(Collection.queryString)
        collections = list()

        for row in cur.fetchall():
            collection = Collection()
            collection.__setFromArray(row)
            collections.append(collection)

        return collections;
