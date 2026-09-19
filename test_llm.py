from pydantic import BaseModel
from src.llm import LLMClient


class LabValue(BaseModel):
    name: str
    value: float
    unit: str


llm = LLMClient()

print(llm.generate("Say hello in one short sentence."))

result = llm.generate_structured(
    "Extract the lab value: Hemoglobin 10.2 g/dL",
    schema=LabValue,
)
print(result)