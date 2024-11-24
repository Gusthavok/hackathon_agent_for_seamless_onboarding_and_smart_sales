'use client'; // Cette ligne indique que ce fichier est un Client Component

import React, { useState } from 'react';
import { Input } from '@/components/ui/input'; // Importation du composant Input de ShadCN
import { Button } from '@/components/ui/button'; // Importation du composant Button de ShadCN
import { useRouter } from 'next/navigation';
import '../globals.css'; // Importation du fichier CSS global
import { API_URL } from '../api';
import { saveToLocalStorage } from '@/utils/localStorageHelper'; // Importation du helper pour le localStorage

function LoginPage() {
    const [username, setUsername] = useState('');
    const router = useRouter(); // Hook pour la redirection
    const [loading, setLoading] = useState(false); // Gérer l'état de chargement
  
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setUsername(event.target.value);
    };
  
    const handleLogin = async () => {
      if (!username) {
        alert('Veuillez entrer un nom d\'utilisateur.');
        return;
      }
  
      setLoading(true); // On démarre le chargement avant d'effectuer la requête
  
      try {
        // Envoie une requête POST au backend pour vérifier l'utilisateur
        const response = await fetch(API_URL+'/api/connexion', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username }),
        });
        saveToLocalStorage('username', username); 

        const data = await response.json();
  
        // Si la réponse du backend est true, on redirige vers la page d'accueil
        if (data.exists) {
          router.push('/'); // Rediriger vers la page d'accueil
        } else {
          // Si l'utilisateur n'existe pas, on redirige vers la page de questions
          router.push('/form/step1'); // Rediriger vers la page de questions
        }
      } catch (error) {
        console.error('Erreur lors de la connexion:', error);
        alert('Une erreur est survenue, veuillez réessayer.');
      } finally {
        setLoading(false); // On arrête le chargement une fois la requête terminée
      }
    };
  
    return (
      <div className="flex justify-center items-center h-screen bg-gray-100">
        <div className="bg-white p-8 rounded-xl shadow-lg w-full sm:w-96">
          <h2 className="text-2xl font-semibold text-center mb-4">Connexion</h2>
          <label htmlFor="username" className="block text-lg font-medium mb-2">
            Nom d'utilisateur:
          </label>
          <Input
            id="username"
            type="text"
            value={username}
            onChange={handleInputChange}
            placeholder="Entrez votre nom d'utilisateur"
            className="mb-4 p-2 border border-gray-300 rounded-md w-full"
          />
          <Button
            onClick={handleLogin}
            className="w-full py-2 bg-green-500 text-white rounded-md hover:bg-green-600"
            disabled={loading} // Désactive le bouton pendant le chargement
          >
            {loading ? 'Chargement...' : 'Se connecter'}
          </Button>
        </div>
      </div>
    );
  }
  
  export default LoginPage;
