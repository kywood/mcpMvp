import asyncio
from fastmcp import Client

async def main():
    async with Client("http://localhost:8001/mcp") as client:
        # 사용 가능한 툴 목록 확인
        tools = await client.list_tools()
        print("사용 가능한 툴:", [t.name for t in tools])

        # ping 툴 호출
        result = await client.call_tool("ping_async", {})
        print("결과:", result)

asyncio.run(main())