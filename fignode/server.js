import { fastify } from 'fastify'
import { DatabasePostgres } from './database-postgres.js'

const server = fastify()
const database = new DatabasePostgres()

server.get('/', (req, reply) => {
  const stream = fs.createReadStream('./node22/dist/index.html')
  reply.type('text/html').send(stream)
})

server.get('/', (req, reply) => {
  reply.sendFile('./node22/dist/index.html') // 
})


server.get('/videos', () => {
  const videos = database.list()
  console.log(videos);
  return videos
})
server.post('/videos', async (request, reply) => {
  const { title, description, duration } = request.body

  await database.create({
    title,
    description,
    duration,
  })
  return reply.status(201).send()
})

server.put('/videos/:id', async (request, reply) => {
  const videoId = request.params.id
  const { title, description, duration } = request.body

  await database.update(videoId, {
    title,
    description,
    duration,
  })
  return reply.status(204).send()

})
server.delete('/videos/:id', async (request, reply) => {
  const videoId = request.params.id
  await database.delete(videoId)
  return reply.status(204).send()
})

server.listen({
  host: '0.0.0.0',
  port: process.env.port ?? 3333
})