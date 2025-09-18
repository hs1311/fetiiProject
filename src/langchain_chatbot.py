"""
LangChain-based NL-SQL Chatbot for FetiiPro Data Analysis
Uses OpenAI's language model to convert natural language to SQL queries
"""
import os
import sqlite3
from typing import Dict, Any, List
from pathlib import Path

# LangChain imports
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents import AgentExecutor
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import BaseMessage
from langchain_core.prompts import PromptTemplate

class FetiiProLangChainChatbot:
    """
    A chatbot that uses LangChain and OpenAI to convert natural language 
    queries to SQL and execute them on the FetiiPro database.
    """
    
    def __init__(self, db_path: str, openai_api_key: str = None):
        """
        Initialize the LangChain SQL chatbot
        
        Args:
            db_path: Path to the SQLite database
            openai_api_key: OpenAI API key (if None, will use environment variable)
        """
        self.db_path = db_path
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it directly.")
        
        # Set the API key
        os.environ["OPENAI_API_KEY"] = self.openai_api_key
        
        # Initialize components
        self.db = None
        self.toolkit = None
        self.agent_executor = None
        self.memory = None
        
        # Query analytics
        self.query_history = []
        self.query_stats = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "avg_response_time": 0
        }
        
        self._setup_database()
        self._setup_agent()
    
    def _setup_database(self):
        """Set up the SQL database connection"""
        try:
            self.db = SQLDatabase.from_uri(f"sqlite:///{self.db_path}")
            print(f"✅ Connected to database: {self.db_path}")
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            raise
    
    def _setup_agent(self):
        """Set up the LangChain SQL agent with enhanced configuration"""
        try:
            # Initialize the LLM with GPT-4 for better performance
            llm = ChatOpenAI(
                model="gpt-4",
                temperature=0,
                openai_api_key=self.openai_api_key,
                max_retries=3,
                request_timeout=60  # Increased timeout for GPT-4
            )
            
            # Create SQL toolkit
            self.toolkit = SQLDatabaseToolkit(db=self.db, llm=llm)
            
            # Create memory for conversation context
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                memory_key_prefix="fetii_pro_"
            )
            
            # Create custom prompt for better SQL generation
            custom_prompt = PromptTemplate(
                input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
                template="""
You are a helpful SQL assistant for FetiiPro ride-sharing data analysis. 
You have access to the following tables:
- demographics: user_id, age
- riders: trip_id, user_id, age  
- trips: trip_id, booking_user_id, pick_up_address, drop_off_address, passenger_count, date, hour, day_of_week, is_weekend, time_of_day

Guidelines:
1. Always use proper JOINs when combining data from multiple tables
2. Use descriptive column aliases in your results
3. Include LIMIT clauses for large result sets
4. Handle NULL values appropriately
5. Provide clear, formatted responses

Question: {input}

You have access to the following tools:
{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
                """
            )
            
            # Create the SQL agent with enhanced configuration
            self.agent_executor = create_sql_agent(
                llm=llm,
                toolkit=self.toolkit,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                memory=self.memory,
                handle_parsing_errors=True,
                max_iterations=5,
                early_stopping_method="generate"
            )
            
            print("✅ LangChain SQL agent initialized successfully with enhanced configuration")
            
        except Exception as e:
            print(f"❌ Error setting up LangChain agent: {e}")
            raise
    
    def process_query(self, natural_language_query: str) -> Dict[str, Any]:
        """
        Process a natural language query and return the result with enhanced formatting
        
        Args:
            natural_language_query: The user's question in natural language
            
        Returns:
            Dictionary with success status, response, and metadata
        """
        import time
        start_time = time.time()
        
        try:
            print(f"🤖 Processing query: {natural_language_query}")
            
            # Validate query
            if not natural_language_query.strip():
                response_time = time.time() - start_time
                self._log_query(natural_language_query, False, response_time)
                return {
                    "success": False,
                    "error": "Please provide a valid question.",
                    "query_type": "langchain_nl_sql"
                }
            
            # Use the LangChain agent to process the query
            result = self.agent_executor.invoke({
                "input": natural_language_query
            })
            
            response_text = result.get("output", "No response generated")
            response_time = time.time() - start_time
            
            # Enhanced response formatting
            formatted_response = self._format_response(response_text, natural_language_query)
            
            # Log successful query
            self._log_query(natural_language_query, True, response_time, response_text)
            
            return {
                "success": True,
                "response": formatted_response,
                "raw_response": response_text,
                "query_type": "langchain_nl_sql",
                "model": "gpt-3.5-turbo",
                "timestamp": self._get_timestamp(),
                "response_time": response_time
            }
            
        except Exception as e:
            response_time = time.time() - start_time
            error_msg = f"Error processing query: {str(e)}"
            print(f"❌ {error_msg}")
            
            # Log failed query
            self._log_query(natural_language_query, False, response_time)
            
            return {
                "success": False,
                "error": error_msg,
                "query_type": "langchain_nl_sql",
                "timestamp": self._get_timestamp(),
                "response_time": response_time
            }
    
    def _format_response(self, response: str, original_query: str) -> str:
        """Format the response to show only the clean answer"""
        # Extract just the final answer
        if "Final Answer:" in response:
            # Extract the final answer
            final_answer = response.split("Final Answer:")[-1].strip()
            return final_answer
        else:
            return response
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_database_info(self) -> str:
        """Get information about the database schema"""
        try:
            if self.db:
                # Get table information
                table_info = self.db.get_table_info()
                return f"Database Schema:\n{table_info}"
            else:
                return "Database not connected"
        except Exception as e:
            return f"Error getting database info: {e}"
    
    def get_sample_questions(self) -> List[str]:
        """Get sample questions that work well with this chatbot"""
        return [
            "How many total trips are there?",
            "What is the average passenger count?",
            "How many trips happened on weekends?",
            "What are the busiest hours for trips?",
            "How many large group trips are there?"
        ]
    
    def clear_memory(self):
        """Clear the conversation memory"""
        if self.memory:
            self.memory.clear()
            print("🧹 Conversation memory cleared")
    
    def get_query_analytics(self) -> Dict[str, Any]:
        """Get query analytics and statistics"""
        return {
            "stats": self.query_stats,
            "recent_queries": self.query_history[-10:],  # Last 10 queries
            "total_queries": len(self.query_history)
        }
    
    def get_query_history(self) -> List[Dict[str, Any]]:
        """Get full query history"""
        return self.query_history
    
    def _log_query(self, query: str, success: bool, response_time: float, response: str = None):
        """Log query for analytics"""
        query_log = {
            "timestamp": self._get_timestamp(),
            "query": query,
            "success": success,
            "response_time": response_time,
            "response_length": len(response) if response else 0
        }
        
        self.query_history.append(query_log)
        self.query_stats["total_queries"] += 1
        
        if success:
            self.query_stats["successful_queries"] += 1
        else:
            self.query_stats["failed_queries"] += 1
        
        # Update average response time
        total_time = sum(q["response_time"] for q in self.query_history)
        self.query_stats["avg_response_time"] = total_time / len(self.query_history)

def main():
    """Main function for testing the LangChain chatbot"""
    print("🚗 FetiiPro LangChain SQL Chatbot")
    print("=" * 50)
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Check database
    db_path = "data/database/fetiipro.db"
    if not Path(db_path).exists():
        print("❌ Database not found. Please run simple_setup.py first")
        return
    
    try:
        # Initialize chatbot
        chatbot = FetiiProLangChainChatbot(db_path)
        
        print("\n📊 Database Information:")
        print(chatbot.get_database_info())
        
        print("\n💡 Sample questions you can ask:")
        for i, question in enumerate(chatbot.get_sample_questions(), 1):
            print(f"{i:2d}. {question}")
        
        print("\n💬 Ask questions about your FetiiPro data (type 'quit' to exit):")
        print("=" * 50)
        
        while True:
            user_input = input("\nYour question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            result = chatbot.process_query(user_input)
            
            if result["success"]:
                print(f"\n✅ Answer:")
                print(result["response"])
            else:
                print(f"\n❌ Error:")
                print(result["error"])
            
            print("=" * 50)
    
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")

if __name__ == "__main__":
    main()
