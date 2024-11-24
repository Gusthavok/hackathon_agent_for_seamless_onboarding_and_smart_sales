import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const { conversation } = req.body

    // Vérifiez le format des messages
    if (!Array.isArray(conversation)) {
      return res.status(400).json({ error: 'Invalid conversation format' })
    }

    // Exemple de réponse contextuelle
    const lastUserMessage = conversation
      .filter((msg: { isUser: boolean }) => msg.isUser)
      .pop()?.text || ''

    const reply = `Vous avez dit : "${lastUserMessage}". Voici une réponse basée sur toute la conversation.`

    res.status(200).json({ reply })
  } else {
    res.setHeader('Allow', ['POST'])
    res.status(405).end(`Méthode ${req.method} non autorisée`)
  }
}
