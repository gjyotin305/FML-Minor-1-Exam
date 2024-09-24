# from typing import List
# from deepeval import evaluate
# from deepeval.metrics import BiasMetric, BaseMetric
# from deepeval.test_case import LLMTestCase

# class Experiment(object):
#     def __init__(self, prompt: List[str], actual_output: List[str]) -> None:
#         self.prompt = prompt
#         self.actual_output = actual_output

#     def _make_test_cases(self) -> List[LLMTestCase]:
#         test_cases = []
#         assert len(self.prompt) == len(self.actual_output), "Check Length of List"
#         for k, v in zip(self.prompt, self.actual_output):
#             test_case = LLMTestCase(
#                 input=k,
#                 actual_output=v
#             )
#             test_cases.append(test_case)
#         return test_cases

#     def run_exp_batch(self, metric: BaseMetric):
#         test_cases = self._make_test_cases()
#         evaluate(test_cases, [metric])