import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { API_URL } from "@/app/api"
import { useRouter } from 'next/navigation'; // Import du hook useRouter

export default function ChatbotInterface() {
  const [messages, setMessages] = useState<{ text: string; isUser: boolean }[]>([
    { text: "Bonjour ! Comment puis-je vous aider aujourd'hui ?", isUser: false },
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const router = useRouter(); // Appel du hook useRouter ici

  const fetchBotResponse = async (conversation: { text: string; isUser: boolean }[]) => {
    try {
      setIsLoading(true)

      // Requête au backend avec l'historique complet
      const response = await fetch(API_URL + '/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ conversation }), // On envoie tout l'historique
      })

      if (!response.ok) {
        throw new Error('Erreur lors de la récupération de la réponse du bot.')
      }

      const data = await response.json()

      // Si une redirection est fournie, on l'affiche et on redirige après un délai
      setMessages(prev => [...prev, { text: data.reply, isUser: false }])

      if (data.redirect && data.redirect !== '') {
        // Attendre quelques secondes avant de rediriger (par exemple, 3 secondes)
        setTimeout(() => {
          router.push(data.redirect); // Rediriger sans recharger la page
        }, 3000); // Délai de 3 secondes

        return; // Ne pas continuer à ajouter un autre message de bot
      }

      // Ajouter la réponse du bot aux messages si pas de redirection
    } catch (error) {
      console.error('Erreur:', error)
      setMessages(prev => [...prev, { text: "Désolé, une erreur s'est produite.", isUser: false }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim()) {
      // Ajouter le message utilisateur à l'historique local
      const updatedMessages = [...messages, { text: input, isUser: true }]
      setMessages(updatedMessages)

      const userMessage = input
      setInput('') // Réinitialiser le champ d'entrée

      // Envoyer l'historique complet au backend
      await fetchBotResponse(updatedMessages)
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="bg-gray-100 p-4 text-center">
        <h2 className="text-xl font-semibold">Support Client</h2>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div key={index} className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-3/4 p-3 rounded-lg ${message.isUser ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
              {message.text}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-3/4 p-3 rounded-lg bg-gray-200">
              Typing...
            </div>
          </div>
        )}
      </div>
      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Tapez votre message..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <Button type="submit" disabled={isLoading}>
            {isLoading ? 'Envoi...' : 'Envoyer'}
          </Button>
        </div>
      </form>
    </div>
  )
}
