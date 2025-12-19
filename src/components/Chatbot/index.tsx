import React, { useState } from 'react';
import { MessageSquare, X, Send } from 'lucide-react';
import styles from './styles.module.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [input, setInput] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I am your Physical AI guide. How can I help you today?' }
  ]);

  const handleSend = () => {
    const rawInput = input.trim();
    const lowerInput = rawInput.toLowerCase();
    if (!lowerInput) return;

    // 1. Add User Message and temporary Thinking state
    const userMsg: Message = { role: 'user', content: rawInput };
    setMessages(prev => [...prev, userMsg, { role: 'assistant', content: 'Thinking...' }]);
    setInput('');

    // 2. Simulate "Thinking" delay (1 second)
    setTimeout(() => {
      let aiResponse = "I am currently in demo mode. Please explore the 'Docs' for full technical details!";
      
      // Logic for specific responses
      if (lowerInput === 'hi' || lowerInput === 'hii' || lowerInput === 'hello') {
        aiResponse = "How may I assist you?";
      } else if (lowerInput.includes('book') || lowerInput.includes('about')) {
        aiResponse = "This book covers Physical AI and Humanoid Robotics, focusing on simulation-to-reality workflows!";
      }

      // 3. Replace 'Thinking...' with the actual response
      setMessages(prev => {
        const newMsgs = [...prev];
        newMsgs[newMsgs.length - 1] = { role: 'assistant', content: aiResponse };
        return newMsgs;
      });
    }, 1000); 
  };

  return (
    <div className={styles.chatWrapper}>
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <span>AI Assistant</span>
            <X onClick={() => setIsOpen(false)} size={20} style={{ cursor: 'pointer' }} />
          </div>
          <div className={styles.chatBody}>
            {messages.map((m, i) => (
              <div key={i} className={m.role === 'user' ? styles.userMsg : styles.aiMsg}>
                {m.content}
              </div>
            ))}
          </div>
          <div className={styles.chatInput}>
            <input 
              value={input} 
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            />
            <button onClick={handleSend} className={styles.sendButton} type="button">
              <Send size={20} className={styles.sendBtn} />
            </button>
          </div>
        </div>
      )}
      <button className={styles.launcher} onClick={() => setIsOpen(!isOpen)} type="button">
        <MessageSquare color="white" />
      </button>
    </div>
  );
}