# def handle_message(message):
#     if isinstance(message, str):
#         print("Log:", message)
#     elif isinstance(message, list):
#         for item in message:
#             if isinstance(item, str):
#                 print("Message part:", item)
#             elif isinstance(item, dict):
#                 print("Message data:", item)
#
# message1 = "System started successfully."
# message2 = ["Error occurred:", {"error_code": 404, "description": "Not found"}]
#
# handle_message(message1)
# handle_message(message2)
from typing import TypedDict, List

class APIResponse(TypedDict):
    status: int
    messages: List[str]

def handle_api_response(response: APIResponse):
    print("Status Code:", response["status"])
    for message in response["messages"]:
        print("Message:", message)

# 示例使用
response_data = APIResponse(status=200, messages=["Success", "Operation completed"])
handle_api_response(response_data)
from dataclasses import dataclass, field
from typing import List

@dataclass
class InventoryItem:
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        """计算并返回库存项的总成本"""
        return self.unit_price * self.quantity_on_hand

# 示例使用
item = InventoryItem(name="Widget", unit_price=25.00, quantity_on_hand=100)
print(f"Total cost for {item.name}: ${item.total_cost()}")

