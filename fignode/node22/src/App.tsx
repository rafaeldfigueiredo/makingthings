import { useState } from 'react'
import './App.css'
import { Tweet } from './components/Tweet'
import { AppRoutes } from './Routes'

function App() {
  const [tweets, setTweets] = useState<string[]>(['Maysa','é','Uma','Bebê'])

  const createTweet = ()=>{
    setTweets([...tweets,"Mentira, é mocinha"])
  }
  return (
    <>
    <AppRoutes />
    {tweets.map((tweet, index) => {
      return <Tweet key={index} name={tweet} />
    })}
    <button onClick={createTweet}
    style={{
      backgroundColor: 'purple',
      color: '#FFF',
      border: 0,
      padding: '6px 12px'
    }}>Mudar</button>
    </> 
  )
}

export default App
