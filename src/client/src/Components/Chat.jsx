import './Chat.css';
import deleteIcon from '../Assets/delete-icon.png';

function Chat({ id, currChatIdx, onClick, deleteChat, text }) {
  if (currChatIdx === id) {
    return (
      <div className='Chat-selected'>
        <p className='Chat-title' onClick={() => onClick(id)}>{text}</p>
        <img className='Chat-delete' src={deleteIcon} onClick={() => deleteChat(id)}></img>
      </div>
    )
  } else {
    return (
      <div className='Chat'>
        <p className='Chat-title' onClick={() => onClick(id)}>{text}</p>
        <img className='Chat-delete' src={deleteIcon} onClick={() => deleteChat(id)}></img>
      </div>
    )
  }
}

export default Chat;