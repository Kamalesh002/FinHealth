import { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Send, MessageCircle, Sparkles, User } from 'lucide-react';
import { chatAPI } from '../services/api';

function ChatInterface({ companyId }) {
    const { t } = useTranslation();
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [suggestions, setSuggestions] = useState([]);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        loadSuggestions();
    }, [companyId]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const loadSuggestions = async () => {
        try {
            const response = await chatAPI.getSuggestions(companyId);
            setSuggestions(response.data.questions || []);
        } catch (error) {
            console.error('Failed to load suggestions:', error);
        }
    };

    const sendMessage = async (text) => {
        if (!text.trim() || loading) return;

        const userMessage = { role: 'user', content: text };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await chatAPI.query({
                company_id: companyId,
                message: text,
                conversation_history: messages.slice(-10)
            });

            const assistantMessage = {
                role: 'assistant',
                content: response.data.response
            };
            setMessages(prev => [...prev, assistantMessage]);

            if (response.data.suggested_questions) {
                setSuggestions(response.data.suggested_questions);
            }
        } catch (error) {
            const errorMessage = {
                role: 'assistant',
                content: 'Sorry, I encountered an error. Please try again.'
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        sendMessage(input);
    };

    const handleSuggestionClick = (suggestion) => {
        sendMessage(suggestion);
    };

    return (
        <div className="chat-interface">
            <div className="chat-header">
                <MessageCircle size={20} />
                <h3>{t('analysis.chat')}</h3>
                <Sparkles size={16} className="ai-badge" />
            </div>

            <div className="chat-messages">
                {messages.length === 0 ? (
                    <div className="chat-empty">
                        <Sparkles size={32} className="empty-icon" />
                        <p>Ask me anything about your financial data!</p>
                        <p className="text-muted text-sm">I can help you understand your metrics, identify risks, and provide recommendations.</p>
                    </div>
                ) : (
                    messages.map((msg, idx) => (
                        <div key={idx} className={`message ${msg.role}`}>
                            <div className="message-avatar">
                                {msg.role === 'user' ? <User size={16} /> : <Sparkles size={16} />}
                            </div>
                            <div className="message-content">
                                {msg.content}
                            </div>
                        </div>
                    ))
                )}

                {loading && (
                    <div className="message assistant">
                        <div className="message-avatar">
                            <Sparkles size={16} />
                        </div>
                        <div className="message-content typing">
                            <span></span><span></span><span></span>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {suggestions.length > 0 && messages.length < 3 && (
                <div className="chat-suggestions">
                    {suggestions.slice(0, 4).map((suggestion, idx) => (
                        <button
                            key={idx}
                            className="suggestion-chip"
                            onClick={() => handleSuggestionClick(suggestion)}
                        >
                            {suggestion}
                        </button>
                    ))}
                </div>
            )}

            <form className="chat-input" onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder={t('dashboard.askQuestion')}
                    disabled={loading}
                />
                <button type="submit" disabled={loading || !input.trim()}>
                    <Send size={18} />
                </button>
            </form>

            <style>{`
        .chat-interface {
          background: var(--bg-card);
          border-radius: var(--radius-lg);
          border: 1px solid var(--border);
          display: flex;
          flex-direction: column;
          height: 500px;
        }

        .chat-header {
          display: flex;
          align-items: center;
          gap: var(--spacing-sm);
          padding: var(--spacing-md) var(--spacing-lg);
          border-bottom: 1px solid var(--border);
        }

        .chat-header h3 {
          font-size: var(--font-size-base);
          font-weight: 600;
          flex: 1;
        }

        .ai-badge {
          color: var(--primary);
        }

        .chat-messages {
          flex: 1;
          overflow-y: auto;
          padding: var(--spacing-lg);
          display: flex;
          flex-direction: column;
          gap: var(--spacing-md);
        }

        .chat-empty {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100%;
          text-align: center;
          color: var(--text-secondary);
        }

        .empty-icon {
          color: var(--primary);
          margin-bottom: var(--spacing-md);
          opacity: 0.5;
        }

        .message {
          display: flex;
          gap: var(--spacing-sm);
          max-width: 85%;
        }

        .message.user {
          align-self: flex-end;
          flex-direction: row-reverse;
        }

        .message-avatar {
          width: 28px;
          height: 28px;
          border-radius: var(--radius-full);
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
        }

        .message.user .message-avatar {
          background: var(--gradient-primary);
          color: white;
        }

        .message.assistant .message-avatar {
          background: rgba(99, 102, 241, 0.2);
          color: var(--primary);
        }

        .message-content {
          padding: var(--spacing-sm) var(--spacing-md);
          border-radius: var(--radius-lg);
          font-size: var(--font-size-sm);
          line-height: 1.5;
        }

        .message.user .message-content {
          background: var(--gradient-primary);
          color: white;
          border-bottom-right-radius: var(--spacing-xs);
        }

        .message.assistant .message-content {
          background: var(--bg-dark);
          color: var(--text-primary);
          border-bottom-left-radius: var(--spacing-xs);
        }

        .typing span {
          display: inline-block;
          width: 6px;
          height: 6px;
          background: var(--text-muted);
          border-radius: 50%;
          margin: 0 2px;
          animation: bounce 1.4s infinite ease-in-out both;
        }

        .typing span:nth-child(1) { animation-delay: -0.32s; }
        .typing span:nth-child(2) { animation-delay: -0.16s; }

        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }

        .chat-suggestions {
          display: flex;
          gap: var(--spacing-sm);
          padding: 0 var(--spacing-lg) var(--spacing-md);
          flex-wrap: wrap;
        }

        .suggestion-chip {
          padding: var(--spacing-xs) var(--spacing-sm);
          background: rgba(99, 102, 241, 0.1);
          border: 1px solid rgba(99, 102, 241, 0.3);
          border-radius: var(--radius-full);
          color: var(--primary-light);
          font-size: var(--font-size-xs);
          cursor: pointer;
          transition: all var(--transition-fast);
        }

        .suggestion-chip:hover {
          background: rgba(99, 102, 241, 0.2);
          border-color: var(--primary);
        }

        .chat-input {
          display: flex;
          gap: var(--spacing-sm);
          padding: var(--spacing-md) var(--spacing-lg);
          border-top: 1px solid var(--border);
        }

        .chat-input input {
          flex: 1;
          padding: var(--spacing-sm) var(--spacing-md);
          background: var(--bg-dark);
          border: 1px solid var(--border);
          border-radius: var(--radius-full);
          color: var(--text-primary);
          font-size: var(--font-size-sm);
        }

        .chat-input input:focus {
          outline: none;
          border-color: var(--primary);
        }

        .chat-input button {
          width: 40px;
          height: 40px;
          border-radius: var(--radius-full);
          background: var(--gradient-primary);
          border: none;
          color: white;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all var(--transition-fast);
        }

        .chat-input button:hover:not(:disabled) {
          box-shadow: var(--shadow-glow);
        }

        .chat-input button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
      `}</style>
        </div>
    );
}

export default ChatInterface;
