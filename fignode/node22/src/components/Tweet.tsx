type TweetProps = {
  name:string;
}

export function Tweet(props:TweetProps){
  return <p>{props.name}</p>
}