import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Chat = () => {
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');
    const [chatHistory, setChatHistory] = useState([]);

    useEffect(() => {
        const fetchChatHistory = async () => {
            try {
                const response = await axios.get('http://localhost:5000/get_chat_history', { withCredentials: true });
                setChatHistory(response.data);
            } catch (error) {
                console.error(error);
            }
        };
        fetchChatHistory();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const aiResponse = await axios.post('http://localhost:5000/chat', { message });
            setResponse(aiResponse.data.response);

            await axios.post('http://localhost:5000/save_chat', { message, response: aiResponse.data.response }, { withCredentials: true });

            setChatHistory([...chatHistory, { message, response: aiResponse.data.response, timestamp: new Date().toISOString() }]);
            setMessage('');
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div style={styles.container}>
            <h2>Chat with AI</h2>
            <div style={styles.chatHistory}>
                {chatHistory.map((chat, index) => (
                    <div key={index} style={styles.chatMessage}>
                        <p><strong>You:</strong> {chat.message}</p>
                        <p><strong>AI:</strong> {chat.response}</p>
                        <p><em>{new Date(chat.timestamp).toLocaleString()}</em></p>
                    </div>
                ))}
            </div>
            <form onSubmit={handleSubmit} style={styles.form}>
                <input
                    type="text"
                    placeholder="Type a message"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    style={styles.input}
                />
                <button type="submit" style={styles.button}>Send</button>
            </form>
        </div>
    );
};

const styles = {
    container: {
        padding: '20px',
        textAlign: 'center',
    },
    chatHistory: {
        marginBottom: '20px',
    },
    chatMessage: {
        borderBottom: '1px solid #ccc',
        padding: '10px',
    },
    form: {
        display: 'flex',
        justifyContent: 'center',
    },
    input: {
        padding: '10px',
        width: '300px',
        marginRight: '10px',
    },
    button: {
        padding: '10px',
        backgroundColor: '#333',
        color: '#fff',
        border: 'none',
        cursor: 'pointer',
    },
};

export default Chat;