from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse

from login_page.models import User
from resource_dashboard.models import Projects, VMs, VM_Group
from resource_dashboard.views import is_blank_or_whitespace, name_length_error

# Not a real password - just here so bandit only has one literal to flag
# instead of one per User.objects.create(...) call below
TEST_PASSWORD = "not-a-real-password"  # nosec B105


def log_in_session(client, user):
    # This app tracks login state in the session directly, no django.contrib.auth,
    # so we log in the same way the real login view does
    session = client.session
    session["logged_in"] = True
    session["user_type"] = user.user_type
    session["user_id"] = user.id
    session.save()


class ValidationHelperTests(TestCase):
    # No DB needed for these, just checking the helper functions directly

    def test_is_blank_or_whitespace_true_for_empty_string(self):
        self.assertTrue(is_blank_or_whitespace(""))

    def test_is_blank_or_whitespace_true_for_whitespace_only(self):
        self.assertTrue(is_blank_or_whitespace("    "))

    def test_is_blank_or_whitespace_true_for_none(self):
        self.assertTrue(is_blank_or_whitespace(None))

    def test_is_blank_or_whitespace_false_for_real_text(self):
        self.assertFalse(is_blank_or_whitespace("Project Alpha"))

    def test_name_length_error_too_short(self):
        self.assertIsNotNone(name_length_error("ab", 3, 100))

    def test_name_length_error_too_long(self):
        self.assertIsNotNone(name_length_error("a" * 101, 3, 100))

    def test_name_length_error_within_bounds(self):
        self.assertIsNone(name_length_error("Project Alpha", 3, 100))


class CreateProjectValidationTests(TestCase):
    def setUp(self):
        cache.clear()
        self.admin = User.objects.create(
            firstname="Susan", lastname="Connery", emailaddress="susan.connery@gmail.com",
            password=TEST_PASSWORD, user_type="ADMIN"
        )
        log_in_session(self.client, self.admin)

    def test_blank_project_name_rejected(self):
        response = self.client.post(reverse("create_project_request"), {
            "project_name": "   ",
            "project_identifier": "abc12345"
        })
        self.assertEqual(response.json()["status"], "fail")
        self.assertEqual(Projects.objects.count(), 0)

    def test_too_short_project_name_rejected(self):
        response = self.client.post(reverse("create_project_request"), {
            "project_name": "ab",
            "project_identifier": "abc12345"
        })
        self.assertEqual(response.json()["status"], "fail")
        self.assertEqual(Projects.objects.count(), 0)

    def test_too_long_project_name_rejected(self):
        response = self.client.post(reverse("create_project_request"), {
            "project_name": "a" * 101,
            "project_identifier": "abc12345"
        })
        self.assertEqual(response.json()["status"], "fail")
        self.assertEqual(Projects.objects.count(), 0)

    def test_project_name_at_max_length_boundary_is_accepted(self):
        response = self.client.post(reverse("create_project_request"), {
            "project_name": "a" * 100,
            "project_identifier": "abc99999"
        })
        self.assertEqual(response.json()["status"], "success")

    def test_valid_project_name_creates_project_and_is_trimmed(self):
        response = self.client.post(reverse("create_project_request"), {
            "project_name": "  Project Alpha  ",
            "project_identifier": "abc12345"
        })
        self.assertEqual(response.json()["status"], "success")

        # One "PROJECT" root entry and one "ADMIN" entity entry get created per project
        self.assertEqual(Projects.objects.filter(project_name="Project Alpha").count(), 2)


class RenameProjectValidationTests(TestCase):
    def setUp(self):
        cache.clear()
        self.admin = User.objects.create(
            firstname="Marcus", lastname="Webb", emailaddress="marcus.webb@gmail.com",
            password=TEST_PASSWORD, user_type="ADMIN"
        )
        log_in_session(self.client, self.admin)

        self.project = Projects.objects.create(
            entity_type="PROJECT", entity_id="0", owner_id=self.admin,
            project_name="Original Name", project_identifier_code="abc12345"
        )

    def test_blank_new_name_rejected(self):
        response = self.client.post(reverse("rename_project_request"), {
            "project_id": self.project.id,
            "new_project_name": "   "
        })
        self.assertEqual(response.json()["status"], "fail")
        self.project.refresh_from_db()
        self.assertEqual(self.project.project_name, "Original Name")

    def test_valid_rename_updates_and_trims_name(self):
        response = self.client.post(reverse("rename_project_request"), {
            "project_id": self.project.id,
            "new_project_name": "  Renamed Project  "
        })
        self.assertEqual(response.json()["status"], "success")
        self.project.refresh_from_db()
        self.assertEqual(self.project.project_name, "Renamed Project")

    def test_missing_csrf_token_is_rejected(self):
        # ADMIN_USER_PROMPT_rename_project used to be missing @csrf_protect entirely,
        # this just guards against that coming back
        strict_client = Client(enforce_csrf_checks=True)
        log_in_session(strict_client, self.admin)

        response = strict_client.post(reverse("rename_project_request"), {
            "project_id": self.project.id,
            "new_project_name": "Renamed Without Token"
        })
        self.assertEqual(response.status_code, 403)


class CreateGroupValidationTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create(
            firstname="Priya", lastname="Nair", emailaddress="priya.nair@gmail.com",
            password=TEST_PASSWORD, user_type="USER"
        )
        log_in_session(self.client, self.user)

    def test_blank_group_name_rejected(self):
        response = self.client.post(reverse("create_group_request"), {
            "selected_group_name": "  "
        })
        self.assertEqual(response.json()["status"], "fail")
        self.assertEqual(VM_Group.objects.count(), 0)

    def test_too_short_group_name_rejected(self):
        response = self.client.post(reverse("create_group_request"), {
            "selected_group_name": "ab"
        })
        self.assertEqual(response.json()["status"], "fail")
        self.assertEqual(VM_Group.objects.count(), 0)

    def test_valid_group_name_creates_group(self):
        response = self.client.post(reverse("create_group_request"), {
            "selected_group_name": "My Group"
        })
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(VM_Group.objects.filter(vm_group_name="My Group").count(), 1)


class ThrottleActionTests(TestCase):
    def setUp(self):
        cache.clear()
        self.admin = User.objects.create(
            firstname="Derek", lastname="Holt", emailaddress="derek.holt@gmail.com",
            password=TEST_PASSWORD, user_type="ADMIN"
        )
        log_in_session(self.client, self.admin)

    def tearDown(self):
        cache.clear()

    def test_second_immediate_request_to_same_endpoint_is_throttled(self):
        first_response = self.client.post(reverse("create_project_request"), {
            "project_name": "Throttle Test Project",
            "project_identifier": "thr00001"
        })
        self.assertEqual(first_response.json()["status"], "success")

        second_response = self.client.post(reverse("create_project_request"), {
            "project_name": "Throttle Test Project Two",
            "project_identifier": "thr00002"
        })
        self.assertEqual(second_response.status_code, 429)
        self.assertEqual(second_response.json()["status"], "fail")

        # Only the first request should have actually created anything
        self.assertEqual(Projects.objects.filter(project_name="Throttle Test Project Two").count(), 0)

    def test_different_users_are_not_throttled_by_each_other(self):
        other_admin = User.objects.create(
            firstname="Fiona", lastname="Marsh", emailaddress="fiona.marsh@gmail.com",
            password=TEST_PASSWORD, user_type="ADMIN"
        )
        other_client = Client()
        log_in_session(other_client, other_admin)

        self.client.post(reverse("create_project_request"), {
            "project_name": "First Admin Project",
            "project_identifier": "thr10001"
        })

        response = other_client.post(reverse("create_project_request"), {
            "project_name": "Second Admin Project",
            "project_identifier": "thr10002"
        })
        self.assertEqual(response.json()["status"], "success")


class AddVmToGroupDuplicateTests(TestCase):
    # Regression tests for USRER_ADMIN_PROMPT_add_vm_to_group - the duplicate
    # check used to be a no-op comparison instead of an assignment
    def setUp(self):
        cache.clear()
        self.user = User.objects.create(
            firstname="Tara", lastname="Nguyen", emailaddress="tara.nguyen@gmail.com",
            password=TEST_PASSWORD, user_type="USER"
        )
        log_in_session(self.client, self.user)

        self.vm = VMs.objects.create(vm_name="Test VM", vm_online="Online", vm_ip="10.0.0.5", owner_id=self.user)
        VM_Group.objects.create(owner_id=self.user, vm_group_name="My Group")  # the group's root entry

    def tearDown(self):
        cache.clear()

    def test_adding_same_vm_twice_is_rejected_the_second_time(self):
        first = self.client.post(reverse("add_vm_to_group_request"), {
            "vm_id": self.vm.id,
            "selected_group_name": "My Group"
        })
        self.assertEqual(first.json()["status"], "success")

        cache.clear()  # bypass the throttle - this test is only about the duplicate check

        second = self.client.post(reverse("add_vm_to_group_request"), {
            "vm_id": self.vm.id,
            "selected_group_name": "My Group"
        })
        data = second.json()
        self.assertEqual(data["status"], "fail")
        self.assertIn("already in the group", data["message"])

        # Only one membership row should exist for this vm+group, not two
        self.assertEqual(
            VM_Group.objects.filter(vm_group_name="My Group", vm_id=self.vm).count(),
            1
        )


class CollateUserProjectListingsTests(TestCase):
    # Regression test for collate_USER_project_listings - it used to end with
    # a bare "return" so it always sent back null instead of the project list
    def setUp(self):
        self.owner = User.objects.create(
            firstname="Warren", lastname="Locke", emailaddress="warren.locke@gmail.com",
            password=TEST_PASSWORD, user_type="ADMIN"
        )
        self.member = User.objects.create(
            firstname="Isabel", lastname="Cruz", emailaddress="isabel.cruz@gmail.com",
            password=TEST_PASSWORD, user_type="USER"
        )

        Projects.objects.create(
            entity_type="PROJECT", entity_id="0", owner_id=self.owner,
            project_name="Shared Project", project_identifier_code="proj0001"
        )
        Projects.objects.create(
            entity_type="USER", entity_id=str(self.member.id), owner_id=self.owner,
            project_name="Shared Project", project_identifier_code="proj0001"
        )

        log_in_session(self.client, self.member)

    def test_user_sees_project_they_belong_to(self):
        response = self.client.post(reverse("project_list_request"))
        data = response.json()

        self.assertEqual(data["status"], "success")
        self.assertIsInstance(data["projects"], list)
        self.assertEqual(len(data["projects"]), 1)
        self.assertEqual(data["projects"][0]["project_name"], "Shared Project")

    def test_user_does_not_see_unrelated_project(self):
        Projects.objects.create(
            entity_type="PROJECT", entity_id="0", owner_id=self.owner,
            project_name="Unrelated Project", project_identifier_code="proj0002"
        )

        response = self.client.post(reverse("project_list_request"))
        project_names = [project["project_name"] for project in response.json()["projects"]]

        self.assertNotIn("Unrelated Project", project_names)
