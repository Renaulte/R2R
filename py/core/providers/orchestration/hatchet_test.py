import asyncio
from hatchet_sdk import Context, Hatchet
 
hatchet = Hatchet(debug=True)
 
@hatchet.workflow(on_events=["user:create"])
class Workflow:
    def __init__(self):
        self.my_value = "test"
 
    @hatchet.step(timeout="2s")
    async def step1(self, context: Context):
        context.refresh_timeout("5s")
 
        print("started step1")
        await asyncio.sleep(1)
        print("finished step1")
 
        return {"test": "test"}
 
    @hatchet.step(parents=["step1"], timeout="4s")
    async def step2(self, context):
        print("started async step2")
        await asyncio.sleep(1)
        print("finished step2")
 
async def main():
    worker = hatchet.worker("first-worker", max_runs=4)
    worker.register_workflow(Workflow())
    await worker.async_start()
 
asyncio.run(main())