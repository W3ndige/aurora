import json
import r2pipe

from karton.core import Karton, Task

class R2Disasm(Karton):
    identity = "kartons.r2disasm"
    filters = [{"type": "sample"}]

    def process(self, task: Task):
        sample = task.get_resource("sample")
        with sample.download_temporary_file() as sample_file:
            path = sample_file.name

            opcodes = []
            r2_obj = r2pipe.open(path)
            r2_obj.cmd("aaa")

            functions = json.loads(r2_obj.cmd("aflj"))

            for function in functions:
                function_name = function["name"]
                function_info = json.loads(r2_obj.cmd(f"pdfj @{function_name}"))

                for opcode in function_info["ops"]:
                    try:
                        opcodes.append(opcode["disasm"])
                    except:
                        pass

            task = Task(
                {
                    "type": "feature",
                    "kind": "disasm",
                }
            )

            task.add_payload("opcodes", opcodes)
            task.add_payload("sha256", sample.sha256)

            self.send_task(task)


