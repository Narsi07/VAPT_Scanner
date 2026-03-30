# -*- coding: utf-8 -*-
# VAPT Security Platform

import logging

import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from authentication.tests import UserCreationTest
from networkscanners.models import *
from projects.models import *

logging.disable(logging.CRITICAL)


class NetworkScanTest(TestCase):
    fixtures = [
        "fixtures/default_user_roles.json",
        "fixtures/default_organization.json",
    ]

    auth_test = UserCreationTest()

    def setUp(self):
        """
        This is the class which runs at the start before running test case.
        This method updates password of admin user
        """
        # Creating Admin user
        UserProfile.objects.create_user(
            name=self.auth_test.admin.get("name"),
            email=self.auth_test.admin.get("email"),
            password=self.auth_test.admin.get("password"),
            role=1,
            organization=1,
        )

        # Creating analyst User
        UserProfile.objects.create_user(
            name=self.auth_test.analyst.get("name"),
            email=self.auth_test.analyst.get("email"),
            password=self.auth_test.analyst.get("password"),
            role=2,
            organization=1,
        )

        # Create viewer user
        UserProfile.objects.create_user(
            name=self.auth_test.viewer.get("name"),
            email=self.auth_test.viewer.get("email"),
            password=self.auth_test.viewer.get("password"),
            role=3,
            organization=1,
        )

    # Test network scan list page
    def test_network_scan_list(self):
        client = Client()

        # from admin users
        client.login(
            username=self.auth_test.admin.get("email"),
            password=self.auth_test.admin.get("password"),
        )

        response = client.get("/networkscanners/list_scans/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "networkscanners/scans/list_scans.html")

        # from analyst users
        client.login(
            username=self.auth_test.analyst.get("email"),
            password=self.auth_test.analyst.get("password"),
        )

        response = client.get("/networkscanners/list_scans/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "networkscanners/scans/list_scans.html")

        # from viewers users
        client.login(
            username=self.auth_test.viewer.get("email"),
            password=self.auth_test.viewer.get("password"),
        )

        response = client.get("/networkscanners/list_scans/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "networkscanners/scans/list_scans.html")
            "/networkscanners/scan_details/?vuln_id=%s&scanner=%s"
            % (vuln_id, "Openvas")
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "networkscanners/scans/vuln_details.html")

        # from analyst users
        client.login(
            username=self.auth_test.analyst.get("email"),
            password=self.auth_test.analyst.get("password"),
        )

        response = client.get(
            "/networkscanners/scan_details/?vuln_id=%s&scanner=%s"
            % (vuln_id, "Openvas")
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "networkscanners/scans/vuln_details.html")

        # from viewer users
        client.login(
            username=self.auth_test.analyst.get("email"),
            password=self.auth_test.analyst.get("password"),
        )

        response = client.get(
            "/networkscanners/scan_details/?vuln_id=%s&scanner=%s"
            % (vuln_id, "Openvas")
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "networkscanners/scans/vuln_details.html")

    def test_network_scan_delete(self):
        client = Client()

        # from admin users
        client.login(
            username=self.auth_test.admin.get("email"),
            password=self.auth_test.admin.get("password"),
        )

        client.post(
            "/projects/project_create/",
            data={"project_name": "name", "project_disc": "disc"},
        )
        project_id = (
            ProjectDb.objects.filter(project_name="name").values("uu_id").get()["uu_id"]
        )

        file_path = "https://raw.githubusercontent.com/archerysec/report-sample/main/Openvas/openvas.xml"

        response = requests.get(file_path)

        file_n = SimpleUploadedFile(
            name="test.xml",
            content=response.text.encode(),
            content_type="multipart/form-data",
        )

        data = {
            "scanner": "openvas",
            "file": file_n,
            "target": "http://test.com",
            "project_id": str(project_id),
        }
        # upload one sample report
        client.post("/report-upload/upload/", data=data)

        # get scan_id form network scans db
        scan_id = NetworkScanDb.objects.filter().values("scan_id").get()["scan_id"]

        response = client.post(
            "/networkscanners/scan_delete/", data={"scan_id": scan_id}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/networkscanners/list_scans/")
        scan_id = NetworkScanDb.objects.filter(scan_id=scan_id).values()
        self.assertEqual(str(scan_id), "<QuerySet []>")

        # from analyst users
        client.login(
            username=self.auth_test.analyst.get("email"),
            password=self.auth_test.analyst.get("password"),
        )

        client.post(
            "/projects/project_create/",
            data={"project_name": "name", "project_disc": "disc"},
        )
        project_id = (
            ProjectDb.objects.filter(project_name="name").values("uu_id").get()["uu_id"]
        )

        file_path = "https://raw.githubusercontent.com/archerysec/report-sample/main/Openvas/openvas.xml"

        response = requests.get(file_path)

        file_n = SimpleUploadedFile(
            name="test.xml",
            content=response.text.encode(),
            content_type="multipart/form-data",
        )

        data = {
            "scanner": "openvas",
            "file": file_n,
            "target": "http://test.com",
            "project_id": str(project_id),
        }
        # upload one sample report
        client.post("/report-upload/upload/", data=data)

        scan_id = NetworkScanDb.objects.filter().values("scan_id").get()["scan_id"]

        response = client.post(
            "/networkscanners/scan_delete/", data={"scan_id": scan_id}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/networkscanners/list_scans/")
        scan_id = NetworkScanDb.objects.filter(scan_id=scan_id).values()
        self.assertEqual(str(scan_id), "<QuerySet []>")

        # from analyst users
        client.login(
            username=self.auth_test.viewer.get("email"),
            password=self.auth_test.viewer.get("password"),
        )

        response = client.post(
            "/networkscanners/scan_delete/", data={"scan_id": scan_id}
        )
        self.assertEqual(response.status_code, 403)

    def test_network_scan_vuln_delete(self):
        client = Client()

        # from admin users
        client.login(
            username=self.auth_test.admin.get("email"),
            password=self.auth_test.admin.get("password"),
        )

        client.post(
            "/projects/project_create/",
            data={"project_name": "name", "project_disc": "disc"},
        )
        project_id = (
            ProjectDb.objects.filter(project_name="name").values("uu_id").get()["uu_id"]
        )

        file_path = "https://raw.githubusercontent.com/archerysec/report-sample/main/Openvas/openvas.xml"

        response = requests.get(file_path)

        file_n = SimpleUploadedFile(
            name="test.xml",
            content=response.text.encode(),
            content_type="multipart/form-data",
        )

        data = {
            "scanner": "openvas",
            "file": file_n,
            "target": "http://test.com",
            "project_id": str(project_id),
        }
        # upload one sample report
        client.post("/report-upload/upload/", data=data)

        # get scan_id form network scans db
        scan_id = NetworkScanDb.objects.filter().values("scan_id").get()["scan_id"]

        vuln_info = NetworkScanResultsDb.objects.filter(scan_id=scan_id)
        vuln_id = ""
        for vuln in vuln_info:
            vuln_id = vuln.vuln_id

        response = client.post(
            "/networkscanners/vuln_delete/",
            data={"scan_id": scan_id, "vuln_id": vuln_id},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/networkscanners/list_scans/")
        vuln_id = NetworkScanResultsDb.objects.filter(vuln_id=vuln_id).values()
        self.assertEqual(str(vuln_id), "<QuerySet []>")

        # from analyst users
        client.login(
            username=self.auth_test.analyst.get("email"),
            password=self.auth_test.analyst.get("password"),
        )

        # get scan_id form network scans db
        scan_id = NetworkScanDb.objects.filter().values("scan_id").get()["scan_id"]

        vuln_info = NetworkScanResultsDb.objects.filter(scan_id=scan_id)
        vuln_id = ""
        for vuln in vuln_info:
            vuln_id = vuln.vuln_id

        response = client.post(
            "/networkscanners/vuln_delete/",
            data={"scan_id": scan_id, "vuln_id": vuln_id},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/networkscanners/list_scans/")
        vuln_id = NetworkScanResultsDb.objects.filter(vuln_id=vuln_id).values()
        self.assertEqual(str(vuln_id), "<QuerySet []>")

        # from analyst users
        client.login(
            username=self.auth_test.viewer.get("email"),
            password=self.auth_test.viewer.get("password"),
        )

        # get scan_id form network scans db
        scan_id = NetworkScanDb.objects.filter().values("scan_id").get()["scan_id"]

        vuln_info = NetworkScanResultsDb.objects.filter(scan_id=scan_id)
        vuln_id = ""
        for vuln in vuln_info:
            vuln_id = vuln.vuln_id

        response = client.post(
            "/networkscanners/vuln_delete/",
            data={"scan_id": scan_id, "vuln_id": vuln_id},
        )
        self.assertEqual(response.status_code, 403)
