import unittest
from main import app
import json


class MeetingTestCase(unittest.TestCase):

    def setUp(self):
        # Test client oluştur
        self.app = app.test_client()
        self.app.testing = True

    def test_create_meeting(self):
        # Yeni bir toplantı oluştur
        meeting_data = {
            'topic': 'Project Discussion',
            'date': '2024-10-18',
            'start_time': '10:00',
            'end_time': '11:00',
            'participants': ['Alice', 'Bob']
        }
        response = self.app.post('/api/v1/meetings', data=json.dumps(meeting_data), content_type='application/json')

        # Status code 201 olmalı
        self.assertEqual(response.status_code, 201)

        # Cevap verisini kontrol et
        response_data = json.loads(response.data)
        self.assertIn('id', response_data)
        self.assertEqual(response_data['topic'], 'Project Discussion')

    def test_get_meetings(self):
        # Toplantıları listele
        response = self.app.get('/api/v1/meetings')

        # Status code 200 olmalı
        self.assertEqual(response.status_code, 200)

        # Gelen veri JSON formatında olmalı
        self.assertEqual(response.content_type, 'application/json')

    def test_update_meeting(self):
        # Bir toplantıyı güncelle
        meeting_data = {
            'topic': 'Updated Meeting',
            'date': '2024-10-19',
            'start_time': '12:00',
            'end_time': '13:00',
            'participants': ['Alice', 'Bob']
        }

        # İlk olarak toplantıyı oluştur
        post_response = self.app.post('/api/v1/meetings', data=json.dumps(meeting_data),
                                      content_type='application/json')
        post_data = json.loads(post_response.data)
        meeting_id = post_data['id']

        # Şimdi toplantıyı güncelle
        updated_data = {
            'topic': 'New Topic',
            'date': '2024-10-20',
            'start_time': '14:00',
            'end_time': '15:00',
            'participants': ['Alice', 'Charlie']
        }
        response = self.app.put(f'/api/v1/meetings/{meeting_id}', data=json.dumps(updated_data),
                                content_type='application/json')

        # Status code 200 olmalı
        self.assertEqual(response.status_code, 200)

        # Güncellenen veriyi kontrol et
        response_data = json.loads(response.data)
        self.assertEqual(response_data['topic'], 'New Topic')

    def test_delete_meeting(self):
        # Silinecek bir toplantı oluştur
        meeting_data = {
            'topic': 'To Be Deleted',
            'date': '2024-10-21',
            'start_time': '10:00',
            'end_time': '11:00',
            'participants': ['Alice']
        }
        post_response = self.app.post('/api/v1/meetings', data=json.dumps(meeting_data),
                                      content_type='application/json')
        post_data = json.loads(post_response.data)
        meeting_id = post_data['id']

        # Toplantıyı sil
        response = self.app.delete(f'/api/v1/meetings/{meeting_id}')

        # Status code 200 olmalı
        self.assertEqual(response.status_code, 200)

        # Silindiğini kontrol et
        get_response = self.app.get(f'/api/v1/meetings/{meeting_id}')
        self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()