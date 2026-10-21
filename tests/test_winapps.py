import importlib.util
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "winapps.py"
SPEC = importlib.util.spec_from_file_location("winapps", MODULE_PATH)
winapps = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(winapps)


class WinAppsTests(unittest.TestCase):
    def test_catalog_has_required_fields(self):
        for app_id, app in winapps.CATALOG.items():
            with self.subTest(app=app_id):
                self.assertTrue(app["name"])
                self.assertIn("windows", app)
                self.assertIn("linux", app)

    def test_windows_command_uses_exact_winget_id(self):
        command = winapps.package_command("firefox", "windows", "winget")
        self.assertEqual(command[:4], ["winget", "install", "--id", "Mozilla.Firefox"])
        self.assertIn("--exact", command)

    def test_linux_apt_command_uses_sudo_and_apt(self):
        command = winapps.package_command("git", "linux", "apt")
        self.assertEqual(command, ["sudo", "apt-get", "install", "-y", "git"])

    def test_unsupported_package_manager_is_safe(self):
        self.assertIsNone(winapps.package_command("vscode", "linux", "apk"))
        self.assertIsNone(winapps.package_command("git", "macos", None))

    def test_unknown_app_is_not_in_catalog(self):
        self.assertNotIn("unknown-app", winapps.CATALOG)


if __name__ == "__main__":
    unittest.main()
