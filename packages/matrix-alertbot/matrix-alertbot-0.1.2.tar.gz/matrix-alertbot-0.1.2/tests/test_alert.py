import os
import unittest
from typing import Dict

from matrix_alertbot.alert import Alert, AlertRenderer

TESTS_DIR = os.path.dirname(__file__)


class AlertTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.alert_dict: Dict = {
            "fingerprint": "fingerprint1",
            "generatorURL": "http://example.com",
            "status": "unknown",
            "labels": {"alertname": "alert1", "severity": "critical", "job": "job1"},
            "annotations": {"description": "some description"},
        }

    def test_create_firing_alert_from_dict(self) -> None:
        self.alert_dict["status"] = "firing"
        alert = Alert.from_dict(self.alert_dict)

        self.assertEqual("fingerprint1", alert.fingerprint)
        self.assertEqual("http://example.com", alert.url)
        self.assertTrue(alert.firing)
        self.assertEqual("critical", alert.status)
        self.assertDictEqual(
            {"alertname": "alert1", "severity": "critical", "job": "job1"}, alert.labels
        )
        self.assertDictEqual({"description": "some description"}, alert.annotations)

    def test_create_resolved_alert_from_dict(self) -> None:
        self.alert_dict["status"] = "resolved"
        alert = Alert.from_dict(self.alert_dict)

        self.assertEqual("resolved", alert.status)
        self.assertFalse(alert.firing)

    def test_create_unknown_alert_from_dict(self) -> None:
        alert = Alert.from_dict(self.alert_dict)

        self.assertEqual("resolved", alert.status)
        self.assertFalse(alert.firing)


class AlertRendererTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.alert_dict: Dict = {
            "fingerprint": "fingerprint1",
            "generatorURL": "http://example.com",
            "status": "unknown",
            "labels": {"alertname": "alert1", "severity": "critical", "job": "job1"},
            "annotations": {"description": "some description"},
        }
        self.renderer = AlertRenderer()

    def test_render_firing_critical_alert(self) -> None:
        self.alert_dict["status"] = "firing"
        alert = Alert.from_dict(self.alert_dict)
        alert.labels["severity"] = "critical"

        html = self.renderer.render(alert, html=True)
        self.assertEqual(
            '<font color="#dc3545">\n  <b>[🔥 CRITICAL]</b>\n</font> '
            '<a href="http://example.com">alert1</a>\n (job1)<br/>\n'
            "some description",
            html,
        )

        plaintext = self.renderer.render(alert, html=False)
        self.assertEqual("[🔥 CRITICAL] alert1: some description", plaintext)

    def test_render_firing_warning_alert(self) -> None:
        self.alert_dict["status"] = "firing"
        self.alert_dict["labels"]["severity"] = "warning"
        alert = Alert.from_dict(self.alert_dict)

        html = self.renderer.render(alert, html=True)
        self.assertEqual(
            '<font color="#ffc107">\n  <b>[⚠️ WARNING]</b>\n</font> '
            '<a href="http://example.com">alert1</a>\n (job1)<br/>\n'
            "some description",
            html,
        )

        plaintext = self.renderer.render(alert, html=False)
        self.assertEqual("[⚠️ WARNING] alert1: some description", plaintext)

    def test_render_firing_unknown_alert(self) -> None:
        self.alert_dict["status"] = "firing"
        self.alert_dict["labels"]["severity"] = "unknown"
        alert = Alert.from_dict(self.alert_dict)

        with self.assertRaisesRegex(KeyError, "unknown"):
            self.renderer.render(alert, html=True)

        with self.assertRaisesRegex(KeyError, "unknown"):
            self.renderer.render(alert, html=False)

    def test_render_resolved_alert(self) -> None:
        self.alert_dict["status"] = "resolved"
        alert = Alert.from_dict(self.alert_dict)

        html = self.renderer.render(alert, html=True)
        self.assertEqual(
            '<font color="#33cc33">\n  <b>[🥦 RESOLVED]</b>\n</font> '
            '<a href="http://example.com">alert1</a>\n (job1)<br/>\n'
            "some description",
            html,
        )

        plaintext = self.renderer.render(alert, html=False)
        self.assertEqual("[🥦 RESOLVED] alert1: some description", plaintext)

    def test_render_resolved_alert_without_job(self) -> None:
        self.alert_dict["status"] = "resolved"
        del self.alert_dict["labels"]["job"]
        alert = Alert.from_dict(self.alert_dict)

        html = self.renderer.render(alert, html=True)
        self.assertEqual(
            '<font color="#33cc33">\n  <b>[🥦 RESOLVED]</b>\n</font> '
            '<a href="http://example.com">alert1</a>\n<br/>\n'
            "some description",
            html,
        )

        plaintext = self.renderer.render(alert, html=False)
        self.assertEqual("[🥦 RESOLVED] alert1: some description", plaintext)

    def test_render_with_existing_filesystem_template(self) -> None:
        alert = Alert.from_dict(self.alert_dict)

        template_dir = os.path.join(TESTS_DIR, "resources/templates")
        renderer = AlertRenderer(template_dir)

        html = renderer.render(alert, html=True)
        self.assertEqual(
            "<b>hello world</b>",
            html,
        )

        plaintext = renderer.render(alert, html=False)
        self.assertEqual("hello world", plaintext)

    def test_render_with_inexistent_filesystem_template(self) -> None:
        self.alert_dict["status"] = "resolved"
        alert = Alert.from_dict(self.alert_dict)

        renderer = AlertRenderer(TESTS_DIR)
        html = renderer.render(alert, html=True)
        self.assertEqual(
            '<font color="#33cc33">\n  <b>[🥦 RESOLVED]</b>\n</font> '
            '<a href="http://example.com">alert1</a>\n (job1)<br/>\n'
            "some description",
            html,
        )

        plaintext = renderer.render(alert, html=False)
        self.assertEqual("[🥦 RESOLVED] alert1: some description", plaintext)


if __name__ == "__main__":
    unittest.main()
