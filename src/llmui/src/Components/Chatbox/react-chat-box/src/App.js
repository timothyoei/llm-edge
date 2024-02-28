import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import bg from './herobg.png'


function App() {
  const [messages, setMessages] = useState([]);
  
  const [newMessage, setNewMessage] = useState('');
  const chatMessagesRef = useRef(null);


  const sendMessage = async () => {
    if (newMessage.trim() !== '') {
      setMessages([...messages, { text: newMessage, sender: 'user' }]);
      setNewMessage('');

      // Simulate GPT response (replace with actual GPT integration)
      const gptResponse = await simulateGptResponse(newMessage);
      setMessages([...messages, { text: gptResponse, sender: 'gpt' }]);
    }
  };

  const simulateGptResponse = async (userMessage) => {
    // Simulate API call to GPT for generating response
    // In a real scenario, this would be replaced with actual GPT API integration
    return `${userMessage}`;
  };

  function keyHandler() {
    let handle = document.querySelector(".message-input");
    handle.addEventListener("keydown", keyDownHandler);
  }
  
  function keyDownHandler(event) {
    if (event.key === "Enter" && event.target.value.trim() !== "") {
      event.preventDefault();
      sendMessage();
    }
  }

  function scrollToBottom(){
    if (chatMessagesRef.current) {
      const scrollHeight = chatMessagesRef.current.scrollHeight;
      chatMessagesRef.current.scrollTop = scrollHeight;
    }
  }
  
  useEffect(() => {
    keyHandler(); // Call keyHandler when the component mounts(when component renders in)
    
    return () => {
      // Cleanup: Remove event listener when the component is unmounted
      const inputField = document.querySelector(".message-input");
      inputField.removeEventListener("keydown", keyDownHandler);
    }
  }) // The empty dependency array ensures that it runs only once

  useEffect(() => {
    let limit = document.querySelector(".chat-messages");
    if(limit.scrollTop < limit.scrollHeight ){

      limit.scrollTop = limit.scrollHeight;
    }
  
    
  });

  return (
    <div className="App" style={{ backgroundImage:`url(${bg})` }}>
      <div className="chat-container">
        <div className="chat-header">
          <h2>Chat</h2>
          <hr></hr>
        </div>
        <div className="chat-messages" id="chat-messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${'user-message'}`}
            >
              {message.text}
            </div>
          ))}
        </div>
        <div className="chat-input">
          <textarea
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Type your message..."
            className="message-input"
          />
            
          

          <button onClick={sendMessage} className="send-button">
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;