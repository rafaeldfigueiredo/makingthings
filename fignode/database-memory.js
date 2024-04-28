import {randomUUID} from 'node:crypto'

export class DatabaseMemory{
  #videos = new Map()

  list(){
    return Array.from(this.#videos.entries()).map((videoArray)=>{
      const videoId = videoArray[0]
      const data = videoArray[1]

      return{
        videoId,
        ...data
      }
    }
    )
  }
  create(video){
    const videoId = randomUUID()
    this.#videos.set(videoId,video)
  }
  update(id,video){
    this.#videos.set(id,video)
  }
  delete(id,video){
    this.#videos.delete(id,video)
  }
}