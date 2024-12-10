import mqtt from 'mqtt'

class MQTTClient {
  constructor() {
    this.client = null
    this.connected = false
  }

  connect(brokerUrl, options = {}) {
    return new Promise((resolve, reject) => {
      this.client = mqtt.connect(brokerUrl, options)

      this.client.on('connect', () => {
        this.connected = true
        resolve(this.client)
      })

      this.client.on('error', (error) => {
        reject(error)
      })
    })
  }

  subscribe(topic) {
    if (!this.connected) {
      throw new Error('MQTT client not connected')
    }
    return new Promise((resolve, reject) => {
      this.client.subscribe(topic, (error) => {
        if (error) {
          reject(error)
        } else {
          resolve()
        }
      })
    })
  }

  publish(topic, message) {
    if (!this.connected) {
      throw new Error('MQTT client not connected')
    }
    return new Promise((resolve, reject) => {
      this.client.publish(topic, message, (error) => {
        if (error) {
          reject(error)
        } else {
          resolve()
        }
      })
    })
  }

  disconnect() {
    if (this.client) {
      this.client.end()
      this.connected = false
    }
  }
}

export default new MQTTClient() 