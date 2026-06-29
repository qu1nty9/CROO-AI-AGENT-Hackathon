import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_PATH = ROOT / "examples" / "run_benchmark.py"


def _load_benchmark_module():
    spec = importlib.util.spec_from_file_location("proofmesh_run_benchmark", BENCHMARK_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BenchmarkTest(unittest.TestCase):
    def test_benchmark_cases_are_balanced(self):
        benchmark = _load_benchmark_module()
        cases = benchmark.build_cases()
        labels = [case["expected_status"] for case in cases]

        self.assertEqual(len(cases), 30)
        self.assertEqual(labels.count("supported"), 10)
        self.assertEqual(labels.count("unsupported"), 10)
        self.assertEqual(labels.count("contradicted"), 10)

    def test_benchmark_expected_accuracy(self):
        benchmark = _load_benchmark_module()
        result = benchmark.run_benchmark(benchmark.build_cases())

        self.assertEqual(result["cases_total"], 30)
        self.assertEqual(result["cases_correct"], 30)
        self.assertEqual(result["accuracy"], 1.0)


if __name__ == "__main__":
    unittest.main()
