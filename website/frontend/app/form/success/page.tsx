'use client'; // Indique que ce fichier est un composant côté client

import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation'; // Importation du hook useRouter
import { API_URL } from '@/app/api';
import { getFromLocalStorage } from '@/utils/localStorageHelper'; // Importer le helper pour localStorage

const Success = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Récupérer les données depuis le localStorage
  const username = getFromLocalStorage('username');
  const name = getFromLocalStorage('name');
  const email = getFromLocalStorage('email');
  const phone = getFromLocalStorage('phone');

  const handleBackToHome = () => {
    router.push('/');
  };

  // Fonction pour envoyer les données au backend
  const sendDataToBackend = async () => {
    // Vérifier si toutes les données nécessaires sont présentes
    if (!username || !name || !email || !phone) {
      setError('Les données du formulaire sont incomplètes.');
      console.log("username", username, "name", name, "email", email, "phone", phone)
      return;
    }

    setLoading(true);
    setError(null); // Réinitialiser l'erreur avant d'envoyer les données

    try {
      const response = await fetch(`${API_URL}/api/createUser`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username, 
          name,
          email,
          phone,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        console.log('Données sauvegardées avec succès:', data);
        // Redirection vers l'accueil ou une autre page après succès
        router.push('/'); 
      } else {
        throw new Error(data.message || 'Erreur lors de l\'enregistrement des données');
      }
    } catch (error) {
      console.error('Erreur:', error);
      setError('Une erreur est survenue lors de l\'enregistrement des données.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Vérification initiale si les données sont présentes
    if (!username || !name || !email || !phone) {
      setError('Les données du formulaire sont incomplètes.');
    }
  }, [username, name, email, phone]);

  return (
    <div className="max-w-md mx-auto p-4 text-center">
      <h1 className="text-3xl font-bold mb-6">Félicitations, vous avez terminé !</h1>
      <p className="text-lg mb-6">Merci d'avoir complété le formulaire. Vos informations sont prêtes à être sauvegardées.</p>

      {error && <div className="text-red-500 mb-4">{error}</div>}
      
      <Button onClick={sendDataToBackend} className="w-full" disabled={loading}>
        {loading ? 'Enregistrement...' : 'Enregistrer les données'}
      </Button>

      <Button onClick={handleBackToHome} className="w-full mt-4">Retour à l'accueil</Button>
    </div>
  );
};

export default Success;
