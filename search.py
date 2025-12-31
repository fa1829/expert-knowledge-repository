"""
Search indexing module using Whoosh
"""
import os
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, KEYWORD, DATETIME
from whoosh.qparser import MultifieldParser
from whoosh.analysis import StemmingAnalyzer


class SearchIndex:
    """Search index manager for knowledge items"""
    
    def __init__(self, index_path):
        self.index_path = index_path
        self.schema = Schema(
            id=ID(stored=True, unique=True),
            title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            description=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            content=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            category=TEXT(stored=True),
            tags=KEYWORD(stored=True, commas=True, scorable=True),
            author=TEXT(stored=True),
            created_at=DATETIME(stored=True)
        )
        
        if not os.path.exists(index_path):
            os.makedirs(index_path)
        
        if not exists_in(index_path):
            self.index = create_in(index_path, self.schema)
        else:
            self.index = open_dir(index_path)
    
    def add_document(self, knowledge_item):
        """Add or update a knowledge item in the search index"""
        writer = self.index.writer()
        writer.update_document(
            id=str(knowledge_item.id),
            title=knowledge_item.title or '',
            description=knowledge_item.description or '',
            content=knowledge_item.content or '',
            category=knowledge_item.category or '',
            tags=knowledge_item.tags or '',
            author=knowledge_item.author.username if knowledge_item.author else '',
            created_at=knowledge_item.created_at
        )
        writer.commit()
    
    def remove_document(self, item_id):
        """Remove a knowledge item from the search index"""
        writer = self.index.writer()
        writer.delete_by_term('id', str(item_id))
        writer.commit()
    
    def search(self, query_string, limit=20):
        """Search the index for knowledge items"""
        with self.index.searcher() as searcher:
            parser = MultifieldParser(
                ['title', 'description', 'content', 'category', 'tags', 'author'],
                schema=self.schema
            )
            query = parser.parse(query_string)
            results = searcher.search(query, limit=limit)
            
            # Convert results to list of dicts
            return [
                {
                    'id': int(hit['id']),
                    'title': hit['title'],
                    'description': hit['description'],
                    'category': hit.get('category', ''),
                    'tags': hit.get('tags', ''),
                    'author': hit.get('author', ''),
                    'score': hit.score
                }
                for hit in results
            ]
    
    def reindex_all(self, knowledge_items):
        """Rebuild the entire search index"""
        writer = self.index.writer()
        for item in knowledge_items:
            writer.add_document(
                id=str(item.id),
                title=item.title or '',
                description=item.description or '',
                content=item.content or '',
                category=item.category or '',
                tags=item.tags or '',
                author=item.author.username if item.author else '',
                created_at=item.created_at
            )
        writer.commit()
