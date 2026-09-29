"""Checks for the evaluation harness using handwritten solutions, not model runs."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('eval_runner', ROOT / 'evals/run.py')
evals = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evals)

SLUG_SOLUTION = '''import re, sys
if len(sys.argv) != 2:
    print("Provide one text argument", file=sys.stderr); sys.exit(2)
value = re.sub(r"[^a-z0-9]+", "-", sys.argv[1].lower()).strip("-")
if not value:
    print("No valid characters", file=sys.stderr); sys.exit(2)
print(value)
'''
LABEL_SOLUTION = '''import json, sys
def version():
    return "legacy-1"
def normalize_labels(values):
    if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
        raise ValueError("Expected a list of strings")
    return list(dict.fromkeys(v.strip().lower() for v in values if v.strip()))
if __name__ == "__main__":
    try:
        if len(sys.argv) != 2: raise ValueError("One JSON argument required")
        print(json.dumps(normalize_labels(json.loads(sys.argv[1]))))
    except ValueError as exc:
        print(str(exc), file=sys.stderr); sys.exit(2)
'''


class EvalHarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.dest = self.root / 'trial'
    def tearDown(self):
        self.temp.cleanup()
    def test_prepare_is_not_a_host_trial(self):
        info = evals.prepare('natural-cli', self.dest)
        self.assertEqual(info['host_trial'], 'NOT_RUN')
        self.assertTrue((self.dest / '.agents/skills/project/SKILL.md').is_file())
    def test_marker_matches_written_bytes(self):
        evals.prepare('natural-cli', self.dest)
        marker = evals.tool.load_json(self.dest / '.project-eval-fixture.json')
        self.assertEqual(marker['preserve']['OWNER-NOTES.md'], evals.tool.digest(self.dest / 'OWNER-NOTES.md'))
    def test_platform_line_endings_are_accepted(self):
        evals.prepare('natural-cli', self.dest)
        solution = SLUG_SOLUTION.replace('print(value)', 'sys.stdout.buffer.write((value + \"\\r\\n\").encode(\"utf-8\"))')
        (self.dest / 'slug.py').write_text(solution, encoding='utf-8')
        self.assertEqual(evals.check(self.dest, True)['result'], 'PASS')
    def test_malformed_double_carriage_return_is_rejected(self):
        evals.prepare('natural-cli', self.dest)
        solution = SLUG_SOLUTION.replace('print(value)', 'sys.stdout.buffer.write((value + \"\\r\\r\\n\").encode(\"utf-8\"))')
        (self.dest / 'slug.py').write_text(solution, encoding='utf-8')
        self.assertEqual(evals.check(self.dest, True)['result'], 'FAIL')
    def test_existing_trial_not_overwritten(self):
        evals.prepare('natural-cli', self.dest)
        with self.assertRaises(evals.tool.ProjectError): evals.prepare('natural-cli', self.dest)
    def test_execution_requires_explicit_consent(self):
        with self.assertRaisesRegex(evals.tool.ProjectError, '--allow-exec'): evals.check(self.dest)
    def test_missing_implementation_fails(self):
        evals.prepare('natural-cli', self.dest)
        self.assertEqual(evals.check(self.dest, True)['result'], 'FAIL')
    def test_handwritten_slug_solution_passes_checker(self):
        evals.prepare('natural-cli', self.dest)
        (self.dest / 'slug.py').write_text(SLUG_SOLUTION, encoding='utf-8')
        result = evals.check(self.dest, True)
        self.assertEqual(result['result'], 'PASS', result)
        self.assertEqual(result['model_identity'], 'NOT_RECORDED')
    def test_wrong_slug_solution_fails_checker(self):
        evals.prepare('natural-cli', self.dest)
        (self.dest / 'slug.py').write_text('print("always-wrong")\n', encoding='utf-8')
        self.assertEqual(evals.check(self.dest, True)['result'], 'FAIL')
    def test_handwritten_document_solution_passes_checker(self):
        evals.prepare('spec-existing', self.dest)
        (self.dest / 'labels.py').write_text(LABEL_SOLUTION, encoding='utf-8')
        result = evals.check(self.dest, True)
        self.assertEqual(result['result'], 'PASS', result)
    def test_mutating_input_is_detected(self):
        evals.prepare('spec-existing', self.dest)
        solution = LABEL_SOLUTION.replace('return list(dict.fromkeys', 'values.reverse()\n    return list(dict.fromkeys')
        (self.dest / 'labels.py').write_text(solution, encoding='utf-8')
        self.assertEqual(evals.check(self.dest, True)['result'], 'FAIL')
    def test_destroyed_user_content_is_detected(self):
        evals.prepare('natural-cli', self.dest)
        (self.dest / 'slug.py').write_text(SLUG_SOLUTION, encoding='utf-8')
        (self.dest / 'OWNER-NOTES.md').unlink()
        self.assertEqual(evals.check(self.dest, True)['result'], 'FAIL')
    def test_existing_test_change_is_detected(self):
        evals.prepare('spec-existing', self.dest)
        (self.dest / 'labels.py').write_text(LABEL_SOLUTION, encoding='utf-8')
        (self.dest / 'test_existing.py').write_text('', encoding='utf-8')
        self.assertEqual(evals.check(self.dest, True)['result'], 'FAIL')


if __name__ == '__main__':
    unittest.main()
