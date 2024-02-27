import react from 'react';
import {useLocation, useNavigate} from 'react-router-dom';


function Chat(){
    const location = useLocation()
    return(
        <div className = 'Home'>
        <h1>Hello {location.state.id}</h1>
    </div>
    )
    

}

export default Chat