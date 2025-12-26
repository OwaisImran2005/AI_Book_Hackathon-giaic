import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, RotateCcw } from 'lucide-react';
import styles from './styles.module.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface Source {
  id: string | number;
  text: string;
  source_url?: string;
  similarity_score?: number;
  metadata?: Record<string, any>;
  embedding_model?: string;
}

interface ChatResponse {
  query: string;
  response: string;
  sources: Source[];
  status: string;
  metadata?: Record<string, any>;
}

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [input, setInput] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I\'m your Physical AI & Robotics Guide. I can help you with questions about ROS 2, Gazebo, Isaac Sim, and humanoid robotics. What would you like to know?' }
  ]);
  const [sources, setSources] = useState<Source[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const chatBodyRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    const rawInput = input.trim();
    if (!rawInput || isLoading) return;

    // Add User Message
    const userMsg: Message = { role: 'user', content: rawInput };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      // Call the backend API
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: rawInput,
          top_k: 3
        })
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data: ChatResponse = await response.json();

      // Add the assistant's response
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);

      // Store sources if available
      if (data.sources && data.sources.length > 0) {
        setSources(data.sources);
      }
    } catch (error) {
      console.error('Error calling API:', error);
      // Add error message
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const clearChat = () => {
    setMessages([
      { role: 'assistant', content: 'Hello! I\'m your Physical AI & Robotics Guide. I can help you with questions about ROS 2, Gazebo, Isaac Sim, and humanoid robotics. What would you like to know?' }
    ]);
  };

  return (
    <div className={styles.chatWrapper}>
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <span>🤖 Physical AI Guide</span>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                onClick={clearChat}
                title="Clear chat"
                style={{
                  background: 'none',
                  border: 'none',
                  color: 'rgba(255,255,255,0.8)',
                  cursor: 'pointer',
                  padding: '4px'
                }}
              >
                <RotateCcw size={16} />
              </button>
              <button
                onClick={() => setIsOpen(false)}
                title="Close"
                style={{
                  background: 'none',
                  border: 'none',
                  color: 'white',
                  cursor: 'pointer',
                  padding: '4px'
                }}
              >
                <X size={16} />
              </button>
            </div>
          </div>
          <div className={styles.chatBody} ref={chatBodyRef}>
            {messages.map((m, i) => (
              <div
                key={i}
                className={
                  m.role === 'user'
                    ? styles.userMsg
                    : m.content === 'Thinking...'
                      ? styles.thinkingMsg
                      : styles.aiMsg
                }
              >
                {m.content === 'Thinking...' ? (
                  <div className={styles.loadingDots}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                ) : (
                  m.content
                )}
              </div>
            ))}
            {isLoading && (
              <div className={styles.thinkingMsg}>
                <div className={styles.loadingDots}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
          </div>
          <div className={styles.chatInput}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything about the book..."
              onKeyDown={handleKeyDown}
              disabled={isLoading}
              autoFocus
            />
            <button
              onClick={handleSend}
              className={styles.sendButton}
              type="button"
              disabled={isLoading}
              title="Send message"
            >
              <Send size={18} className={styles.sendBtn} />
            </button>
          </div>
        </div>
      )}
      <button
        className={styles.launcher}
        onClick={() => setIsOpen(!isOpen)}
        type="button"
        title="Open AI Assistant"
      >
        <MessageSquare size={28} color="white" />
      </button>
    </div>
  );
}