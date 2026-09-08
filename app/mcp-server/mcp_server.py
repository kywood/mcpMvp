from fastmcp import FastMCP

mcp = FastMCP("mcpMvp")


@mcp.tool()
def ping() -> str:
    """서버가 살아있는지 확인하는 테스트 툴 (동기 버전)"""
    return "pong"


@mcp.tool()
async def ping_async() -> str:
    """서버가 살아있는지 확인하는 테스트 툴 (비동기 버전)"""
    return "pong (async)"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8001)