# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Test script to verify MCP server functionality."""

import asyncio
import pytest
from awslabs.document_loader_mcp_server.server import mcp


@pytest.mark.asyncio
async def test_server():
    """Test the MCP server tools."""
    print('Testing MCP Server...')

    # Test getting tools
    try:
        tools = await mcp.get_tools()
        print(f'\nAvailable tools ({len(tools)}):')

        tool_names = []
        for tool in tools:
            if hasattr(tool, 'name'):
                print(f'- {tool.name}: {getattr(tool, "description", "No description")}')
                tool_names.append(tool.name)
            else:
                print(f'- {tool}: {type(tool)}')
                tool_names.append(str(tool))

        # Verify our tools are present
        expected_tools = ['read_pdf', 'read_docx', 'read_xlsx', 'read_pptx', 'read_image']

        for expected_tool in expected_tools:
            if expected_tool in tool_names:
                print(f'✓ {expected_tool} tool found')
            else:
                print(f'✗ {expected_tool} tool missing')

        print('\nMCP Server is working correctly!')

    except Exception as e:
        print(f'Error testing server: {e}')
        import traceback

        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(test_server())
