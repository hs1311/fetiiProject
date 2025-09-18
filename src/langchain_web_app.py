"""
LangChain-based Web Chatbot for FetiiPro Data Analysis
Web interface for the LangChain NL-SQL chatbot
"""
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from langchain_chatbot import FetiiProLangChainChatbot

class LangChainChatbotHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the LangChain chatbot web interface"""
    
    def __init__(self, *args, **kwargs):
        self.chatbot = None
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_html()
        elif parsed_path.path == '/api/query':
            self.handle_query()
        elif parsed_path.path == '/api/info':
            self.handle_info()
        elif parsed_path.path == '/api/samples':
            self.handle_samples()
        elif parsed_path.path == '/api/analytics':
            self.handle_analytics()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/query':
            self.handle_query_post()
        else:
            self.send_error(404)
    
    def serve_html(self):
        """Serve the main HTML page"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
        <meta http-equiv="Pragma" content="no-cache">
        <meta http-equiv="Expires" content="0">
        <meta name="version" content="2.0">
    <title>FetiiPro LangChain SQL Chatbot</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #1f77b4 0%, #9c27b0 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5rem;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 10px;
        }
        .main-content {
            display: flex;
            min-height: 600px;
        }
        .sidebar {
            width: 300px;
            background: #f8f9fa;
            padding: 20px;
            border-right: 1px solid #e9ecef;
        }
        .chat-area {
            flex: 1;
            padding: 20px;
            display: flex;
            flex-direction: column;
        }
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            max-height: 500px;
            margin-bottom: 20px;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 15px;
            background: #fafafa;
        }
        .message {
            margin-bottom: 15px;
            padding: 12px 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background: #e3f2fd;
            margin-left: auto;
            border-left: 4px solid #2196f3;
        }
        .bot-message {
            background: #f3e5f5;
            border-left: 4px solid #9c27b0;
        }
        .error-message {
            background: #ffebee;
            border-left: 4px solid #f44336;
        }
        .input-area {
            display: flex;
            gap: 10px;
        }
        .input-area input {
            flex: 1;
            padding: 12px 15px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
        }
        .input-area input:focus {
            border-color: #1f77b4;
        }
        .input-area button {
            padding: 12px 25px;
            background: linear-gradient(135deg, #1f77b4 0%, #9c27b0 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        .input-area button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .sample-question {
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .sample-question:hover {
            background: #e3f2fd;
            border-color: #2196f3;
            transform: translateX(5px);
        }
        .info-section {
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            border: 1px solid #e9ecef;
        }
        .info-section h3 {
            margin-top: 0;
            color: #1f77b4;
        }
        .loading {
            display: none;
            text-align: center;
            color: #666;
            font-style: italic;
        }
        .sql-display {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            color: #495057;
        }
        .model-info {
            background: #e8f5e8;
            border: 1px solid #4caf50;
            border-radius: 5px;
            padding: 8px;
            margin-top: 10px;
            font-size: 12px;
            color: #2e7d32;
        }
        .suggestion-item {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
            color: #495057;
        }
        .suggestion-item:hover {
            background: #e3f2fd;
            border-color: #2196f3;
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(33, 150, 243, 0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚗 FetiiPro LangChain SQL Chatbot</h1>
            <p>Powered by LangChain + OpenAI GPT-4</p>
            <div class="badge">🧠 Natural Language to SQL</div>
        </div>
        
        <div class="main-content">
            <div class="sidebar">
                <div class="info-section">
                    <h3>💡 Quick Suggestions</h3>
                    <div id="quick-suggestions">
                        <div class="suggestion-item" onclick="askQuestion('How many total trips are there?')">
                            📊 Total trips count
                        </div>
                        <div class="suggestion-item" onclick="askQuestion('What is the average passenger count?')">
                            👥 Average passengers
                        </div>
                        <div class="suggestion-item" onclick="askQuestion('What are the busiest hours for trips?')">
                            ⏰ Busiest hours
                        </div>
                        <div class="suggestion-item" onclick="askQuestion('How many trips happened on weekends?')">
                            🎉 Weekend trips
                        </div>
                        <div class="suggestion-item" onclick="askQuestion('What is the average age of users?')">
                            👤 User demographics
                        </div>
                    </div>
                </div>
                
                <div class="info-section">
                    <h3>💡 Sample Questions</h3>
                    <div id="sample-questions"></div>
                </div>
                
                <div class="info-section">
                    <h3>🎯 Quick Actions</h3>
                    <button onclick="clearChat()" style="background-color: #dc3545; margin-bottom: 10px;">🗑️ Clear Chat</button>
                    <button onclick="clearMemory()" style="background-color: #ffc107; color: #000; margin-bottom: 10px;">🧠 Clear Memory</button>
                    <button onclick="showAnalytics()" style="background-color: #17a2b8; color: white;">📊 Show Analytics</button>
                </div>
                
                <div class="info-section">
                    <h3>📈 Query Analytics</h3>
                    <div id="analytics-display" style="font-size: 12px; color: #666;">
                        Click "Show Analytics" to view statistics
                    </div>
                </div>
            </div>
            
            <div class="chat-area">
                <div class="chat-messages" id="chat-messages">
                    <div class="message bot-message">
                        <strong>Bot:</strong> Welcome! I'm powered by LangChain and OpenAI GPT-4. I can understand natural language and convert it to SQL queries for your FetiiPro data. Ask me anything!
                    </div>
                </div>
                
                <div class="loading" id="loading">Processing your question with AI...</div>
                
                <div class="input-area">
                    <input type="text" id="user-input" placeholder="Ask a question about the FetiiPro data..." onkeypress="handleKeyPress(event)">
                    <button onclick="sendMessage()">Send</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const chatArea = document.getElementById('chat-messages');
        const userInput = document.getElementById('user-input');
        const sampleQuestionsDiv = document.getElementById('sample-questions');

        function displayMessage(message, isUser = true, isError = false, modelInfo = null) {
            const msgDiv = document.createElement('div');
            msgDiv.classList.add('message');
            if (isError) {
                msgDiv.classList.add('error-message');
                msgDiv.innerHTML = `<strong>Error:</strong> ${message}`;
            } else if (isUser) {
                msgDiv.classList.add('user-message');
                msgDiv.innerHTML = `<strong>You:</strong> ${message}`;
            } else {
                msgDiv.classList.add('bot-message');
                msgDiv.innerHTML = `<strong>Bot:</strong> ${message}`;
                
                if (modelInfo) {
                    const modelDiv = document.createElement('div');
                    modelDiv.classList.add('model-info');
                    modelDiv.innerHTML = `🤖 Powered by ${modelInfo}`;
                    msgDiv.appendChild(modelDiv);
                }
            }
            chatArea.appendChild(msgDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        async function sendMessage() {
            const message = userInput.value.trim();
            if (message) {
                displayMessage(message, true);
                userInput.value = '';
                
                // Display loading
                document.getElementById('loading').style.display = 'block';
                
                try {
                    const response = await fetch('/api/query', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ question: message })
                    });
                    const result = await response.json();
                    
                    document.getElementById('loading').style.display = 'none';
                    
                    if (result.success) {
                        displayMessage(result.response, false, false, result.model ? `LangChain + ${result.model}` : 'LangChain');
                    } else {
                        displayMessage(result.error, false, true);
                    }
                } catch (error) {
                    document.getElementById('loading').style.display = 'none';
                    displayMessage(`Failed to connect to the chatbot server: ${error}`, false, true);
                }
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        async function loadDbInfo() {
            try {
                const response = await fetch('/api/info');
                const data = await response.json();
                dbInfoTextarea.value = data.info;
            } catch (error) {
                dbInfoTextarea.value = `Error loading database info: ${error}`;
            }
        }

        function refreshDbInfo() {
            loadDbInfo();
        }

        async function loadSampleQuestions() {
            try {
                const response = await fetch('/api/samples');
                const data = await response.json();
                sampleQuestionsDiv.innerHTML = '';
                data.sample_questions.forEach(q => {
                    const qButton = document.createElement('div');
                    qButton.classList.add('sample-question');
                    qButton.textContent = q;
                    qButton.onclick = () => {
                        userInput.value = q;
                        sendMessage();
                    };
                    sampleQuestionsDiv.appendChild(qButton);
                });
            } catch (error) {
                sampleQuestionsDiv.innerHTML = `<div class="error-message">Error loading sample questions: ${error}</div>`;
            }
        }

        function clearChat() {
            chatArea.innerHTML = '';
            displayMessage("Welcome! I'm powered by LangChain and OpenAI GPT-4. I can understand natural language and convert it to SQL queries for your FetiiPro data. Ask me anything!", false, false, 'LangChain + GPT-4');
        }

        function askQuestion(question) {
            userInput.value = question;
            sendMessage();
        }

        async function clearMemory() {
            try {
                await fetch('/api/clear-memory', { method: 'POST' });
                displayMessage("🧠 Conversation memory cleared!", false, false, 'LangChain');
            } catch (error) {
                displayMessage("Error clearing memory: " + error, false, true);
            }
        }

        async function showAnalytics() {
            try {
                const response = await fetch('/api/analytics');
                const data = await response.json();
                
                if (data.success) {
                    const analytics = data.analytics;
                    const stats = analytics.stats;
                    
                    const analyticsHtml = `
                        <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
                            <strong>📊 Query Statistics:</strong><br>
                            • Total Queries: ${stats.total_queries}<br>
                            • Successful: ${stats.successful_queries}<br>
                            • Failed: ${stats.failed_queries}<br>
                            • Avg Response Time: ${stats.avg_response_time.toFixed(2)}s<br>
                            • Success Rate: ${((stats.successful_queries / stats.total_queries) * 100).toFixed(1)}%
                        </div>
                    `;
                    
                    document.getElementById('analytics-display').innerHTML = analyticsHtml;
                } else {
                    document.getElementById('analytics-display').innerHTML = 'Error loading analytics';
                }
            } catch (error) {
                document.getElementById('analytics-display').innerHTML = 'Error loading analytics: ' + error;
            }
        }

        // Initial load
        window.onload = () => {
            loadDbInfo();
            loadSampleQuestions();
        };
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def handle_query(self):
        """Handle GET query requests"""
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        question = query_params.get('q', [''])[0]
        
        if not question:
            self.send_error(400, "Missing question parameter")
            return
        
        result = self.get_chatbot().process_query(question)
        self.send_json_response(result)
    
    def handle_query_post(self):
        """Handle POST query requests"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            question = data.get('question', '')
            
            if not question:
                self.send_error(400, "Missing question")
                return
            
            result = self.get_chatbot().process_query(question)
            self.send_json_response(result)
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
    
    def handle_info(self):
        """Handle database info requests"""
        try:
            chatbot = self.get_chatbot()
            info = chatbot.get_database_info()
            result = {"success": True, "info": info}
            self.send_json_response(result)
        except Exception as e:
            result = {"success": False, "error": str(e)}
            self.send_json_response(result)
    
    def handle_samples(self):
        """Handle sample questions requests"""
        try:
            chatbot = self.get_chatbot()
            samples = chatbot.get_sample_questions()
            result = {"success": True, "sample_questions": samples}
            self.send_json_response(result)
        except Exception as e:
            result = {"success": False, "error": str(e)}
            self.send_json_response(result)
    
    def handle_analytics(self):
        """Handle analytics requests"""
        try:
            chatbot = self.get_chatbot()
            analytics = chatbot.get_query_analytics()
            result = {"success": True, "analytics": analytics}
            self.send_json_response(result)
        except Exception as e:
            result = {"success": False, "error": str(e)}
            self.send_json_response(result)
    
    def get_chatbot(self):
        """Get or create chatbot instance"""
        if self.chatbot is None:
            db_path = "data/database/fetiipro.db"
            openai_api_key = os.getenv("OPENAI_API_KEY")
            
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            
            self.chatbot = FetiiProLangChainChatbot(db_path, openai_api_key)
        return self.chatbot
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def run_server(port=None):
    """Run the LangChain web server"""
    # Use environment port for cloud deployment, fallback to 8082
    port = port or int(os.environ.get('PORT', 8082))
    server_address = ('0.0.0.0', port)  # Allow external connections
    httpd = HTTPServer(server_address, LangChainChatbotHandler)
    print(f"🚗 FetiiPro LangChain SQL Chatbot Web Server")
    print(f"🌐 Server running at: http://localhost:{port}")
    print(f"🌍 External access: http://[YOUR_IP]:{port}")
    print(f"📊 Database: data/database/fetiipro.db")
    print(f"🤖 Powered by: LangChain + OpenAI GPT-4")
    print(f"💡 Ask natural language questions about your ride-sharing data!")
    print(f"🔄 Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
