import unittest
import app


class FlaskTest(unittest.TestCase):

    def test_index(self):
        tester = app.app.test_client(self)
        responce = tester.get('/report')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_index_xml(self):
        tester = app.app.test_client(self)
        responce = tester.get('/report-xml')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_index_content_json(self):
        tester = app.app.test_client(self)
        responce = tester.get('/report')
        self.assertEqual(responce.content_type, 'application/json')

    def test_index_content_xml(self):
        tester = app.app.test_client(self)
        responce = tester.get('/report-xml')
        self.assertEqual(responce.content_type, 'text/xml; charset=utf-8')


    def test_index_data(self):
        tester = app.app.test_client(self)
        responce = tester.get('/report')
        self.assertTrue(b'full_name' in responce.data)


if __name__ == '__main__':
    unittest.main()