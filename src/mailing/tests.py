import io
import os
import random

import pytest
from django.core.files import File
from django.core.files.uploadedfile import UploadedFile
from ninja_extra.testing import TestClient
from .endpoints import MailingController
from django.test.client import MULTIPART_CONTENT
from django.core.cache import cache as dj_cache

from .models import MailTemplate

#
# @pytest.mark.django_db
# class TestMailingController:
#     headers = {
#         'Authorization': 'Bearer admin'
#     }
#     client = TestClient(MailingController)
#
#     @pytest.mark.parametrize("expected_status",
#                              [
#                                  200,
#                              ]
#                              )
#     def test_create_delete_template(self, expected_status):
#         random_template = random.choice(os.listdir(
#             os.path.join("seed", "template")))
#         file_path = os.path.join("seed", "template", random_template)
#         with open(file_path, 'rb') as f:
#             file_content = io.FileIO(f.fileno())
#             size = os.path.getsize(file_path)
#             file_content.name = 'mailing-template.html'
#             files = {
#                 'file': UploadedFile(file_content,
#                                      content_type='text/html', size=size)}
#             response = self.client.post("/template/",
#                                         files=file_content,
#                                         content_type=MULTIPART_CONTENT,
#                                         FILES=files,
#                                         headers=self.headers)
#         assert response.status_code == expected_status
#
#     @pytest.mark.parametrize("expected_status",
#                              [
#                                  200,
#                              ]
#                              )
#     def test_get_templates(self, expected_status):
#         response = self.client.get("/templates/",
#                                    headers=self.headers)
#         assert response.status_code == expected_status
#
#     def test_mailing(self, ):
#         random_template = random.choice(os.listdir(
#             os.path.join("seed", "template")))
#         file_path = os.path.join("seed", "template", random_template)
#         file = open(file_path, "rb")
#
#         template = MailTemplate.objects.create(
#             name='mailing-template',
#             file=File(file, "/media/MailTemplate/" + file.name)
#         )
#         mailing_response = self.client.post(f"/start/",
#                                             json={
#                                                 'temp_id': template.id,
#                                                 'user_ids': [
#                                                     1, 2, 3
#                                                 ]
#                                             },
#                                             headers=self.headers)
#         assert mailing_response.status_code == 200
#
#     def test_status(self):
#         get_status = True
#         while get_status:
#             status_response = self.client.get(f"/status/",
#                                               headers=self.headers)
#             if status_response.status_code == 201:
#                 dj_cache.delete('mailing_task')
#                 get_status = False