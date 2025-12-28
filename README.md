# 🗂️ MCP Filesystem Assistant

A beautiful AI-powered file manager built with **Model Context Protocol (MCP)**, featuring a modern web interface, OpenAI integration, and secure filesystem operations.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 🎯 What is This?

An AI assistant that can read, write, and manage your files through natural language. Built on the Model Context Protocol (MCP), it demonstrates how to:

- 🤖 Connect AI models to real tools
- 🔒 Safely manage files in a sandboxed environment
- 🎨 Build beautiful interfaces with Streamlit
- 🛠️ Create production-ready MCP servers

Perfect for learning MCP or building your own AI-powered tools!

---

## ✨ Features

### 💬 Natural Language Interface
Ask the AI to manage files in plain English:
- "List all files in the workspace"
- "Read notes.txt and summarize it"
- "Create a backup folder and organize my files"
- "Show me details about data.json"

### 🎨 Beautiful Web Interface
- **Chat Tab** - Talk to the AI assistant
- **File Browser** - Visual workspace explorer
- **Quick Actions** - Direct file operations without AI

### 🛠️ 8 Powerful Tools
| Tool | What it does |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Create or overwrite files |
| `append_file` | Add to existing files |
| `delete_file` | Remove files safely |
| `list_directory` | Browse folders |
| `create_directory` | Make new folders |
| `move_file` | Rename or relocate files |
| `get_file_info` | Show file details |

### 🔒 Security First
- All operations sandboxed to `workspace/` folder
- Path traversal protection
- Input validation on every operation

---

## 📁 Project Structure

```
filesystem-mcp-project/
├── host/                      # Streamlit web app
│   ├── app.py                 # Main interface
│   ├── mcp_connector.py       # Connects to MCP server
│   └── ui_components.py       # UI styling
│
├── server/                    # MCP server
│   ├── filesystem_mcp_server.py  # 8 filesystem tools
│   └── config.py              # Settings
│
├── workspace/                 # Your files live here
│   ├── notes.txt             
│   └── data.json             
│
├── requirements.txt           # Python packages
├── .env.example              # Config template
└── README.md                 # You are here!
```

---

## 🚀 Quick Start

### 1. Install

```bash
# Clone or download the project
cd filesystem-mcp-project

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

Create a `.env` file:

```env
OPENAI_API_KEY=sk-your-key-here
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

### 3. Run

**Terminal 1 - Start MCP Server:**
```bash
python server/filesystem_mcp_server.py
```

You should see:
```
🚀 MCP Server starting...
📁 Workspace directory: /path/to/workspace
🌐 Server running on http://127.0.0.1:8000
✅ Available tools: 8
```

**Terminal 2 - Launch Web Interface:**
```bash
streamlit run host/app.py
```

Browser opens at `http://localhost:8501` 🎉

---

## 💡 Usage Examples

### Example 1: List Files
**You:** "What files are in the workspace?"

**AI:** *Uses `list_directory` tool*
```
📁 Directory: .

  📄 notes.txt (1.2 KB)
  📄 data.json (856 bytes)
```

### Example 2: Create File
**You:** "Create a file called hello.txt with 'Hello World!'"

**AI:** *Uses `write_file` tool*
```
✅ File written successfully: hello.txt (12 characters)
```

### Example 3: Organize Files
**You:** "Create a backup folder and move old files into it"

**AI:** *Uses `create_directory` and `move_file` tools*
```
✅ Directory created: backup
✅ File moved: old_data.txt → backup/old_data.txt
```

---

## 🏗️ How It Works

```
┌─────────────────┐
│   You (User)    │
│  Ask questions  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Streamlit App  │
│  localhost:8501 │  ← Beautiful web interface
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   OpenAI API    │
│     GPT-4       │  ← AI decides which tools to use
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   MCP Server    │
│  localhost:8000 │  ← Executes file operations
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   workspace/    │
│   Your Files    │  ← Safe sandbox folder
└─────────────────┘
```

---

## 🔧 Configuration

### Basic Settings (`.env`)

```env
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional (defaults shown)
MCP_SERVER_HOST=127.0.0.1
MCP_SERVER_PORT=8000
```

### Advanced Settings (`server/config.py`)

```python
# Change workspace location
WORKSPACE_DIR = Path("my_custom_folder")

# Change server port
MCP_SERVER_PORT = 9000
```

---

## 🐛 Troubleshooting

### "Server Not Connected"
1. Check if MCP server is running (Terminal 1)
2. Click "Check Connection" button in sidebar
3. Restart both server and Streamlit

### "OpenAI API Key Error"
1. Make sure `.env` file exists
2. Check your API key is correct
3. Restart Streamlit after updating `.env`

### "Port Already in Use"
```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or change port in .env
MCP_SERVER_PORT=8001
```

### "File Not Found"
Remember: All paths are relative to `workspace/`

```python
✅ Correct:   read_file("notes.txt")
❌ Wrong:     read_file("workspace/notes.txt")
❌ Wrong:     read_file("/absolute/path/file.txt")
```

---

## 🛠️ Development

### Add a New Tool

Edit `server/filesystem_mcp_server.py`:

```python
@mcp.tool()
def search_files(query: str) -> str:
    """
    Search for files containing text.
    
    Args:
        query: Text to search for
    
    Returns:
        List of matching files
    """
    # Your implementation here
    return "Found 3 files matching 'query'"
```

Restart the server - that's it! The tool is automatically available.

## 🤝 Contributing

Contributions welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Make your changes
4. Test everything works
5. Submit a pull request

---

## 🎓 Workshop Ready

This project is designed for learning and teaching:
- ✅ Clear, commented code
- ✅ Step-by-step setup
- ✅ Real-world example
- ✅ Production patterns
- ✅ Security best practices

Perfect for:
- Learning MCP architecture
- Building AI tools
- Teaching modern Python
- Prototyping ideas

---

**Happy building! 🎉**
