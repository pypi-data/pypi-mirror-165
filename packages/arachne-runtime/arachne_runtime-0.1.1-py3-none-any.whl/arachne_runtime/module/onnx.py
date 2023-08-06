import time
from typing import List

import numpy as np

from .factory import RuntimeModuleBase, RuntimeModuleFactory


def onnx_tensor_type_to_np_dtype(ottype: str):
    dtype = ottype.replace("tensor(", "").replace(")", "")
    if dtype == "float":
        dtype = "float32"
    elif dtype == "double":
        dtype = "float64"
    return dtype


@RuntimeModuleFactory.register("onnx")
class ONNXRuntimeModule(RuntimeModuleBase):
    def __init__(self, model: str, providers: List[str] = ["CPUExecutionProvider"], **kwargs):
        import onnxruntime as ort

        self.module: ort.InferenceSession = ort.InferenceSession(
            model, providers=providers, **kwargs
        )
        self._inputs = {}
        self._outputs = {}
        self.input_details = self.module.get_inputs()
        self.output_details = self.module.get_outputs()

    def run(self):
        # NOTE: should we support run_options?
        self._outputs = self.module.run(output_names=None, input_feed=self._inputs)

    def set_input(self, idx, value, **kwargs):
        """Set input data.

        Args:
            idx (int): layer index to set data
            value (np.ndarray): input data
        """
        if not isinstance(idx, int):
            raise Exception("idx should be int")
        self._inputs[self.input_details[idx].name] = value

    def get_output(self, idx):
        """Get inference output.

        Args:
            index (int): layer index to get output

        Returns:
            np.ndarray: output data
        """
        return self._outputs[idx]

    def _convert_detail(self, x):
        return {"name": x.name, "dtype": onnx_tensor_type_to_np_dtype(x.type), "shape": x.shape}

    def get_input_details(self):
        return list(map(self._convert_detail, self.input_details))

    def get_output_details(self):
        return list(map(self._convert_detail, self.output_details))

    def benchmark(self, warmup: int = 1, repeat: int = 10, number: int = 1):
        for idx, inp in enumerate(self.input_details):
            input_data = np.random.uniform(0, 1, size=inp.shape).astype(
                onnx_tensor_type_to_np_dtype(inp.type)
            )
            self.set_input(idx, input_data)

        for _ in range(warmup):
            self.run()

        times = []
        for _ in range(repeat):
            time_start = time.perf_counter()
            for _ in range(number):
                self.run()
            time_end = time.perf_counter()
            times.append((time_end - time_start) / number)

        mean_ts = np.mean(times) * 1000
        std_ts = np.std(times) * 1000
        max_ts = np.max(times) * 1000
        min_ts = np.min(times) * 1000

        return {"mean": mean_ts, "std": std_ts, "max": max_ts, "min": min_ts}
