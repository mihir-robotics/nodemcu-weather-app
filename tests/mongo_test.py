
# Import necessary modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import patch, MagicMock
from mongo import connectToMongo, load, fetch, mongoClose


class MongoTest(unittest.TestCase):

    # Test connectToMongo function
    @patch('pymongo.MongoClient')
    def test_connectToMongo(self, mock_client):
        mock_db = MagicMock()
        mock_client.return_value = mock_db
        client, db, collection = connectToMongo('uri', 'db_name', 'collection_name')
        self.assertEqual(client, mock_db)

    # Test load function
    @patch('pymongo.collection.Collection')
    def test_load(self, mock_collection):
        mock_response = MagicMock()
        mock_collection.insert_one.return_value = mock_response
        response = load(mock_collection, {'key': 'value'})
        self.assertEqual(response, {"inserted_id": str(mock_response.inserted_id)})

    # Test fetch function
    @patch('pymongo.collection.Collection')
    def test_fetch(self, mock_collection):
        mock_cursor = MagicMock()
        mock_collection.find.return_value = mock_cursor
        records = fetch(mock_collection, 1)
        self.assertEqual(records, list(mock_cursor))

    # Test mongoClose function
    @patch('pymongo.MongoClient')
    def test_mongoClose(self, mock_client):
        mongoClose(mock_client)
        mock_client.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
