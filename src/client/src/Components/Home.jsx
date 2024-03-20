import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';

import './Home.css';
import Chat from './Chat';

function Home() {
  const location = useLocation();
  const [chats, setChats] = useState(location.state.user.chats);
  const [currChatIdx, setCurrChatIdx] = useState(0);
  const [query, setQuery] = useState('');
  const chatMessagesRef = useRef(null);

  const createChat = async () => {
    try {
      await axios.post("http://localhost:8000/api/chats", {}, {
        "headers": {
          "Authorization": `Bearer ${location.state.token}`
        }
      }).then(res => {
        if (res.status === 404) {
          console.log(res.data.error);
        } else if (res.status === 201) {
          setChats([...chats, res.data.chat]);
        }
      }).catch(e => {console.log(e)});
    } catch (e) {
      console.log(e);
    }
  };

  const sendQuery = async () => {
    if (query.trim() !== '') {
      try {
        await axios.post(`http://localhost:8000/api/chats/${currChatIdx}`, {"query": query}, {
          "headers": {
            "Authorization": `Bearer ${location.state.token}`
          }
        }).then(res => {
          if (res.status === 400) {
            console.log(res.data.error);
          } else if (res.status === 409) {
            if (chats.length <= currChatIdx) {
              console.log("Create a chat first!");
            } else {
              console.log(res.data.error);
            }
          } else if (res.status === 200) {
            const newChats = chats.map((chat, idx) => {
              if (idx === currChatIdx) {
                return {"title": chats[idx].title, "history": [...chats[idx].history, {"query": query, "response": res.data.response}]};
              }
              return chat;
            });
            setChats(newChats);
          }
        }).catch(e => {console.log(e)});
      } catch (e) {
        console.log(e);
      }
      setQuery("");
    }
  };

  const deleteChat = async (chatIdx) => {
    try {
      await axios.delete(`http://localhost:8000/api/chats/${chatIdx}`, {
        "headers": {"Authorization": `Bearer ${location.state.token}`}
      }).then(res => {
        if (res.status === 200) {
          setChats(chats.filter((chat, idx) => idx !== chatIdx));
        } else {console.log(res.data.error)}
      }).catch(e => {console.log(e)});
    } catch (e) {console.log(e)}
  };

  function keyHandler() {
    let handle = document.querySelector(".message-input");
    handle.addEventListener("keydown", keyDownHandler);
  }
  
  function keyDownHandler(event) {
    if (event.key === "Enter" && event.target.value.trim() !== "") {
      event.preventDefault();
      sendQuery();
    }
  }

  function scrollToBottom(){
      const scrollHeight = chatMessagesRef.current.scrollHeight;
      chatMessagesRef.current.scrollTop = scrollHeight;
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
    if (limit && limit.scrollTop < limit.scrollHeight ){
      limit.scrollTop = limit.scrollHeight;
    }
  });

  return (
    <div className="Home">
      <div className="chat-controller">
        <button className="chat-create" onClick={createChat}>
          Create Chat
        </button>
        <hr />
        {
          chats.map((chat, idx) => (
            <Chat key={idx} id={idx} currChatIdx={currChatIdx} onClick={setCurrChatIdx} deleteChat={deleteChat} text={chat.title} />
          ))
        }
      </div>
      <div className="chat-container">
        {
          (() => {
            if (chats.length > 0) {
              return (
                <div className="chat-header">
                  <h2>{chats[currChatIdx].title}</h2>
                  <hr></hr>
                </div>
              )
            }
          })()
        }
        <div className="chat-messages" id="chat-messages">
          {
            (() => {
              if (chats.length > 0) {
                return (
                chats[currChatIdx].history.map((qa, index) => (
                  <div key={index} className="chat-message">
                    <div className="user-message">{qa.query}</div>
                    <div className="response-message">{qa.response}</div>
                  </div>
                )));
              }
          })()}
        </div>
        <div className="chat-input">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type your message..."
            className="message-input"
          />
          <button onClick={sendQuery} className="send-button">
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default Home;